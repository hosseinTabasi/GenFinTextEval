"""Full factorial study runner → JSON artifacts."""
from __future__ import annotations

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from genfin.extract import load_lexicon
from genfin.factcard import load_all_events
from genfin.generate import generate_variant
from genfin.metrics_belief import (
    authority_cue,
    disagreement,
    load_personas,
    text_polarity,
    update_belief,
    willingness_to_act,
)
from genfin.metrics_system import (
    amplification_proxy,
    build_baseline_corpus,
    contamination_slope,
    contamination_sweep,
    tail_language_fraction,
)
from genfin.metrics_text import layer_a_metrics


def load_config(path: Path | str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def run_study(root: Path | str, config_path: Path | str | None = None) -> dict[str, Any]:
    root = Path(root)
    cfg = load_config(config_path or root / "config" / "study.yaml")
    events = load_all_events(root / cfg["paths"]["events_dir"])
    personas = load_personas(root / cfg["paths"]["personas"])
    lex_dir = root / cfg["paths"]["lexicons_dir"]
    seeds = list(cfg["seeds"])
    variants = list(cfg["variants"])
    eps = float(cfg["num_epsilon"])
    tau = float(cfg["willingness_tau"])
    kappa = float(cfg["willingness_kappa"])
    rho_grid = list(cfg["contamination_rho"])
    art_dir = root / cfg["paths"]["artifacts_dir"]
    art_dir.mkdir(parents=True, exist_ok=True)

    texts_rows: list[dict[str, Any]] = []
    belief_rows: list[dict[str, Any]] = []
    layer_a_rows: list[dict[str, Any]] = []

    # Generate all texts and Layer A
    text_store: dict[tuple[str, str, int], str] = {}
    for seed in seeds:
        for card in events:
            eid = card["event_id"]
            # generate all variants first so paraphrase stability can use anchored+paraphrase
            local: dict[str, str] = {}
            for v in variants:
                local[v] = generate_variant(card, v, seed)
                text_store[(eid, v, seed)] = local[v]
                texts_rows.append({
                    "event_id": eid,
                    "variant": v,
                    "seed": seed,
                    "text": local[v],
                })
            for v in variants:
                para = local.get("paraphrase") if v == "anchored" else None
                # For frame stability on paraphrase variant, compare to anchored
                if v == "paraphrase":
                    para = local.get("anchored")
                a = layer_a_metrics(local[v], card, lex_dir, eps=eps, paraphrase_text=para)
                row = {"event_id": eid, "variant": v, "seed": seed, **a}
                layer_a_rows.append(row)

                pol = text_polarity(local[v], lex_dir)
                auth = authority_cue(local[v], lex_dir, int(a["source_fabrication_count"]))
                mu_after: list[float] = []
                for persona in personas:
                    b = update_belief(persona, a, pol, auth)
                    wta = willingness_to_act(float(b["delta_mu"]), float(b["c1"]), tau, kappa)
                    belief_rows.append({
                        "event_id": eid,
                        "variant": v,
                        "seed": seed,
                        **b,
                        "willingness_to_act": wta,
                        "unit": f"{persona['id']}×{eid}×{v}",
                    })
                    mu_after.append(float(b["mu1"]))
                # attach disagreement for this event×variant×seed
                d = disagreement(mu_after)
                for row_b in belief_rows[-len(personas):]:
                    row_b["cross_persona_disagreement"] = round(d, 6)

    # Layer C: contamination per seed using persuade texts vs baseline
    bull = load_lexicon(lex_dir / "polarity_bull.txt")
    bear = load_lexicon(lex_dir / "polarity_bear.txt")
    crash = load_lexicon(lex_dir / "crash.txt")
    # expand multiword crash into phrase set already; also single tokens
    contamination_rows: list[dict[str, Any]] = []
    amp_rows: list[dict[str, Any]] = []
    for seed in seeds:
        baseline = build_baseline_corpus(seed, int(cfg["baseline_corpus_size"]), bull, bear)
        synth = [text_store[(c["event_id"], v, seed)]
                 for c in events for v in ("persuade_bull", "persuade_bear")]
        anchored_texts = [text_store[(c["event_id"], "anchored", seed)] for c in events]
        for label, bag in (("persuade", synth), ("anchored", anchored_texts)):
            sweep = contamination_sweep(baseline, bag, rho_grid, bull, bear, seed)
            slope = contamination_slope(sweep)
            for srow in sweep:
                contamination_rows.append({
                    "seed": seed,
                    "contaminant": label,
                    **srow,
                    "slope_bias_vs_rho": round(slope, 6),
                })
        all_texts = [text_store[(c["event_id"], v, seed)] for c in events for v in variants]
        amp = amplification_proxy(all_texts, seed)
        amp["seed"] = seed
        amp["tail_language_fraction"] = round(tail_language_fraction(all_texts, crash), 6)
        # by variant tail
        for v in variants:
            vt = [text_store[(c["event_id"], v, seed)] for c in events]
            amp[f"tail_frac_{v}"] = round(tail_language_fraction(vt, crash), 6)
        amp_rows.append(amp)

    # Aggregates for falsification
    def mean_abs_dmu(variant: str) -> float:
        xs = [abs(float(r["delta_mu"])) for r in belief_rows if r["variant"] == variant]
        return _mean(xs)

    anchored_abs = mean_abs_dmu("anchored")
    bull_abs = mean_abs_dmu("persuade_bull")
    bear_abs = mean_abs_dmu("persuade_bear")
    persuade_abs = _mean([abs(float(r["delta_mu"])) for r in belief_rows if r["variant"] in ("persuade_bull", "persuade_bear")])
    margin = float(cfg["falsification"]["margin_belief"])
    slope_flat = float(cfg["falsification"]["slope_flat"])

    persuade_slopes = [float(r["slope_bias_vs_rho"]) for r in contamination_rows if r["contaminant"] == "persuade" and r["rho"] == 0.0]
    # slope is repeated per rho row; unique by seed
    slope_by_seed = {}
    for r in contamination_rows:
        if r["contaminant"] == "persuade":
            slope_by_seed[r["seed"]] = float(r["slope_bias_vs_rho"])
    mean_persuade_slope = _mean(list(slope_by_seed.values()))
    abs_slope = abs(mean_persuade_slope)

    belief_lift = persuade_abs - anchored_abs
    belief_effect = belief_lift >= margin
    contamination_effect = abs_slope >= slope_flat
    # Pre-registered: claim FAILS if persuade does NOT increase |Δμ| by margin AND slope is flat
    claim_fails = (not belief_effect) and (not contamination_effect)
    claim_passes = not claim_fails

    summary = {
        "study_id": cfg["study_id"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "n_events": len(events),
        "n_variants": len(variants),
        "n_personas": len(personas),
        "n_seeds": len(seeds),
        "n_belief_cells": len(belief_rows),
        "n_text_cells": len(texts_rows),
        "means": {
            "abs_delta_mu_anchored": round(anchored_abs, 6),
            "abs_delta_mu_persuade_bull": round(bull_abs, 6),
            "abs_delta_mu_persuade_bear": round(bear_abs, 6),
            "abs_delta_mu_persuade": round(persuade_abs, 6),
            "belief_lift_persuade_minus_anchored": round(belief_lift, 6),
            "mean_persuade_contamination_slope": round(mean_persuade_slope, 6),
            "mean_faithfulness_by_variant": {
                v: round(_mean([float(r["numerical_faithfulness"]) for r in layer_a_rows if r["variant"] == v]), 6)
                for v in variants
            },
            "mean_fabrication_by_variant": {
                v: round(_mean([float(r["source_fabrication_count"]) for r in layer_a_rows if r["variant"] == v]), 6)
                for v in variants
            },
            "mean_certainty_by_variant": {
                v: round(_mean([float(r["certainty_score"]) for r in layer_a_rows if r["variant"] == v]), 6)
                for v in variants
            },
            "mean_hedge_by_variant": {
                v: round(_mean([float(r["hedge_ratio"]) for r in layer_a_rows if r["variant"] == v]), 6)
                for v in variants
            },
            "mean_frame_stability_anchored_vs_paraphrase": round(
                _mean([float(r["frame_stability_jaccard"]) for r in layer_a_rows
                       if r["variant"] == "paraphrase" and "frame_stability_jaccard" in r]), 6
            ),
            "mean_disagreement_by_variant": {
                v: round(_mean([float(r["cross_persona_disagreement"]) for r in belief_rows if r["variant"] == v]), 6)
                for v in variants
            },
            "willingness_rate_by_variant": {
                v: round(_mean([1.0 if r["willingness_to_act"] else 0.0 for r in belief_rows if r["variant"] == v]), 6)
                for v in variants
            },
            "mean_tail_frac_by_variant": {
                v: round(_mean([float(r.get(f"tail_frac_{v}", 0.0)) for r in amp_rows]), 6)
                for v in variants
            },
        },
        "falsification": {
            "margin_belief": margin,
            "slope_flat": slope_flat,
            "belief_lift": round(belief_lift, 6),
            "belief_effect": belief_effect,
            "abs_contamination_slope": round(abs_slope, 6),
            "contamination_effect": contamination_effect,
            "claim_passes": claim_passes,
            "claim_fails": claim_fails,
            "rule": (
                "Claim fails if persuade variants do not increase mean |Δμ| vs anchored "
                "by margin_belief AND contamination slope magnitude is below slope_flat."
            ),
        },
    }

    artifacts = {
        "summary.json": summary,
        "texts.json": texts_rows,
        "layer_a.json": layer_a_rows,
        "belief.json": belief_rows,
        "contamination.json": contamination_rows,
        "amplification.json": amp_rows,
    }
    for name, obj in artifacts.items():
        (art_dir / name).write_text(json.dumps(obj, indent=2), encoding="utf-8")

    return summary
