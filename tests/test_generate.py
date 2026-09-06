from pathlib import Path
from genfin.factcard import load_all_events
from genfin.generate import generate_variant

ROOT = Path(__file__).resolve().parents[1]


def test_variants_deterministic():
    card = load_all_events(ROOT / "data" / "events")[0]
    a1 = generate_variant(card, "anchored", 20260311)
    a2 = generate_variant(card, "anchored", 20260311)
    assert a1 == a2
    b = generate_variant(card, "persuade_bull", 20260311)
    assert a1 != b
    assert "Not investment advice" in a1 or "not investment advice" in a1.lower()


def test_persuade_has_certainty_or_authority_language():
    card = load_all_events(ROOT / "data" / "events")[0]
    t = generate_variant(card, "persuade_bull", 20260311)
    assert any(w in t.lower() for w in ("certainly", "experts say", "no doubt", "guaranteed", "rock solid"))
