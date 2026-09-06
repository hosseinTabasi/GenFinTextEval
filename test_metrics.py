from pathlib import Path
from genfin.factcard import load_all_events
from genfin.generate import generate_variant
from genfin.metrics_text import layer_a_metrics, frame_stability
from genfin.metrics_belief import load_personas, update_belief, text_polarity, authority_cue, disagreement
from genfin.metrics_system import contamination_sweep, contamination_slope, build_baseline_corpus

ROOT = Path(__file__).resolve().parents[1]
LEX = ROOT / "data" / "lexicons"


def test_layer_a_anchored_faithfulness_high():
    card = load_all_events(ROOT / "data" / "events")[0]
    text = generate_variant(card, "anchored", 20260311)
    a = layer_a_metrics(text, card, LEX)
    assert a["numerical_faithfulness"] >= 0.5
    assert a["source_fabrication_count"] == 0


def test_frame_stability_self():
    assert frame_stability("peg held near par", "peg held near par") == 1.0


def test_belief_update_runs():
    card = load_all_events(ROOT / "data" / "events")[0]
    personas = load_personas(ROOT / "data" / "personas.yaml")
    text = generate_variant(card, "persuade_bear", 20260311)
    a = layer_a_metrics(text, card, LEX)
    pol = text_polarity(text, LEX)
    auth = authority_cue(text, LEX, int(a["source_fabrication_count"]))
    outs = [update_belief(p, a, pol, auth) for p in personas]
    assert len(outs) == 4
    d = disagreement([o["mu1"] for o in outs])
    assert d >= 0.0


def test_contamination_slope_defined():
    bull = {"recovery", "surplus"}
    bear = {"depeg", "risk"}
    base = build_baseline_corpus(1, 50, bull, bear)
    synth = ["depeg crash contagion risk risk risk"] * 10
    sweep = contamination_sweep(base, synth, [0.0, 0.5, 1.0], bull, bear, seed=1)
    slope = contamination_slope(sweep)
    assert isinstance(slope, float)
