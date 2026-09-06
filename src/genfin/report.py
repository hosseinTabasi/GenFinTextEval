"""Build reports/RESULTS.md strictly from JSON artifacts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_results(root: Path | str) -> Path:
    root = Path(root)
    art = root / "artifacts"
    summary = _load(art / "summary.json")
    layer_a = _load(art / "layer_a.json")
    belief = _load(art / "belief.json")
    contamination = _load(art / "contamination.json")
    amp = _load(art / "amplification.json")

    m = summary["means"]
    f = summary["falsification"]
    lines: list[str] = []
    lines.append("# GenFinTextEval Results")
    lines.append("")
    lines.append(f"**Study ID:** `{summary['study_id']}`")
    lines.append(f"**Generated (UTC):** {summary['timestamp_utc']}")
    lines.append("")
    lines.append("All numbers below are read from `artifacts/*.json`. No invented values.")
    lines.append("")
    lines.append("## Study size")
    lines.append("")
    lines.append(f"- Events: **{summary['n_events']}**")
    lines.append(f"- Variants: **{summary['n_variants']}**")
    lines.append(f"- Personas: **{summary['n_personas']}**")
    lines.append(f"- Seeds: **{summary['n_seeds']}**")
    lines.append(f"- Belief cells (persona × event × variant × seed): **{summary['n_belief_cells']}**")
    lines.append(f"- Text cells (event × variant × seed): **{summary['n_text_cells']}**")
    lines.append("")
    lines.append("## RQ falsification (pre-registered)")
    lines.append("")
    lines.append(f"- Rule: {f['rule']}")
    lines.append(f"- `margin_belief` = {f['margin_belief']}")
    lines.append(f"- `slope_flat` = {f['slope_flat']}")
    lines.append(f"- Belief lift (persuade − anchored) mean |Δμ|: **{f['belief_lift']}** → belief_effect={f['belief_effect']}")
    lines.append(f"- |contamination slope| (persuade mix): **{f['abs_contamination_slope']}** → contamination_effect={f['contamination_effect']}")
    lines.append(f"- **Claim passes:** `{f['claim_passes']}`")
    lines.append(f"- **Claim fails:** `{f['claim_fails']}`")
    lines.append("")
    lines.append("## Layer A — text")
    lines.append("")
    lines.append("| Variant | Faithfulness | Fabrication (mean count) | Certainty | Hedge |")
    lines.append("|---|---:|---:|---:|---:|")
    for v, faith in m["mean_faithfulness_by_variant"].items():
        lines.append(
            f"| {v} | {faith} | {m['mean_fabrication_by_variant'][v]} | "
            f"{m['mean_certainty_by_variant'][v]} | {m['mean_hedge_by_variant'][v]} |"
        )
    lines.append("")
    lines.append(
        f"- Mean frame stability (Jaccard, paraphrase vs anchored): "
        f"**{m['mean_frame_stability_anchored_vs_paraphrase']}**"
    )
    lines.append("")
    lines.append("## Layer B — belief")
    lines.append("")
    lines.append(f"- Mean |Δμ| anchored: **{m['abs_delta_mu_anchored']}**")
    lines.append(f"- Mean |Δμ| persuade_bull: **{m['abs_delta_mu_persuade_bull']}**")
    lines.append(f"- Mean |Δμ| persuade_bear: **{m['abs_delta_mu_persuade_bear']}**")
    lines.append(f"- Mean |Δμ| persuade (pooled): **{m['abs_delta_mu_persuade']}**")
    lines.append("")
    lines.append("| Variant | Cross-persona disagreement (mean) | Willingness-to-act rate |")
    lines.append("|---|---:|---:|")
    for v, d in m["mean_disagreement_by_variant"].items():
        lines.append(f"| {v} | {d} | {m['willingness_rate_by_variant'][v]} |")
    lines.append("")
    lines.append("## Layer C — system")
    lines.append("")
    lines.append(f"- Mean persuade contamination slope (bias vs ρ): **{m['mean_persuade_contamination_slope']}**")
    lines.append("")
    lines.append("### Contamination sweep (persuade contaminant)")
    lines.append("")
    lines.append("| Seed | ρ | Sentiment index | Bias vs ρ=0 | Slope |")
    lines.append("|---:|---:|---:|---:|---:|")
    for row in contamination:
        if row["contaminant"] != "persuade":
            continue
        lines.append(
            f"| {row['seed']} | {row['rho']} | {row['sentiment_index']} | "
            f"{row['bias_vs_rho0']} | {row['slope_bias_vs_rho']} |"
        )
    lines.append("")
    lines.append("### Amplification / tail language")
    lines.append("")
    lines.append("| Seed | Mean reuse | Max reuse | Herfindahl | Tail frac (all) |")
    lines.append("|---:|---:|---:|---:|---:|")
    for row in amp:
        lines.append(
            f"| {row['seed']} | {row['mean_reuse']} | {row['max_reuse']} | "
            f"{row['reuse_herfindahl']} | {row['tail_language_fraction']} |"
        )
    lines.append("")
    lines.append("Tail language fraction by variant (mean across seeds):")
    lines.append("")
    for v, t in m["mean_tail_frac_by_variant"].items():
        lines.append(f"- `{v}`: **{t}**")
    lines.append("")
    lines.append("## Artifact paths")
    lines.append("")
    lines.append("- `artifacts/summary.json`")
    lines.append("- `artifacts/texts.json`")
    lines.append("- `artifacts/layer_a.json`")
    lines.append("- `artifacts/belief.json`")
    lines.append("- `artifacts/contamination.json`")
    lines.append("- `artifacts/amplification.json`")
    lines.append("")
    lines.append(f"_Belief row count check: {len(belief)}; Layer A row count: {len(layer_a)}._")
    lines.append("")

    out = root / "reports" / "RESULTS.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
