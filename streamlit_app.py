"""Browse events and Layer A/B scores (optional UI)."""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="GenFinTextEval", layout="wide")
st.title("GenFinTextEval")
st.caption("Hossein Tabasi — offline evaluation of generative financial text (Layers A/B/C). Not investment advice.")

from genfin.factcard import load_all_events
from genfin.generate import generate_variant
from genfin.metrics_text import layer_a_metrics
from genfin.metrics_belief import load_personas, update_belief, text_polarity, authority_cue

events = load_all_events(ROOT / "data" / "events")
ids = [e["event_id"] for e in events]
eid = st.sidebar.selectbox("Event", ids)
variant = st.sidebar.selectbox("Variant", ["anchored", "persuade_bull", "persuade_bear", "paraphrase"])
seed = st.sidebar.number_input("Seed", value=20260311, step=1)

card = next(e for e in events if e["event_id"] == eid)
text = generate_variant(card, variant, int(seed))
st.subheader(card["title"])
st.write(text)

a = layer_a_metrics(text, card, ROOT / "data" / "lexicons")
st.subheader("Layer A")
st.json(a)

personas = load_personas(ROOT / "data" / "personas.yaml")
pol = text_polarity(text, ROOT / "data" / "lexicons")
auth = authority_cue(text, ROOT / "data" / "lexicons", int(a["source_fabrication_count"]))
st.subheader("Layer B (computational personas)")
rows = [update_belief(p, a, pol, auth) for p in personas]
st.dataframe(rows)

art = ROOT / "artifacts" / "summary.json"
if art.exists():
    st.subheader("Last study summary")
    st.json(json.loads(art.read_text())["falsification"])
