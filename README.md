# GenFinTextEval

![python](https://img.shields.io/badge/python-3.11%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![study](https://img.shields.io/badge/study-offline%20deterministic-lightgrey)
![layers](https://img.shields.io/badge/layers-A%20text%20%7C%20B%20belief%20%7C%20C%20system-orange)

**Author:** Hossein Tabasi ([hosseinTabasi](https://github.com/hosseinTabasi))  
**License:** MIT

Methods-grade evaluation framework for **generative financial text** about USD stablecoins (USDT / USDC). Generation is treated as scientifically interesting only when it changes an identifiable object: **beliefs, disagreement, attention, credibility, or a market/platform outcome**. BLEU / ROUGE / perplexity are rejected as primary claims.

## Research question

> Relative to a fact-card-constrained baseline, do strategically framed generative financial texts (omission / certainty inflation / authority cues) produce larger persona belief updates and greater contamination bias in a bag-of-texts sentiment index, holding the event fact card fixed?

Full protocol: [`PROTOCOL.md`](PROTOCOL.md).

## Evaluation stack

| Layer | Focus | Examples |
|-------|--------|----------|
| **A Text** | Faithfulness & rhetoric | numerical faithfulness, source fabrication, hedge/certainty, frame stability |
| **B Belief** | Computational personas | Δμ, confidence, disagreement, willingness-to-act |
| **C System** | Ecological effects | contamination ρ sweep, amplification proxy, crash/depeg tail language |

A-only is too weak; C without A+B is sloppy.

## Related work (same author)

- [SynthOpinion](https://github.com/hosseinTabasi/SynthOpinion) — fact-card synthetic opinion; belief-direction alignment.
- [EchoMarket](https://github.com/hosseinTabasi/EchoMarket) — multi-agent cascade shapes on a follow graph.

GenFinTextEval is a **new** evaluation framework; it may reuse **verified public event facts** from those protocols but regenerates study design, code, and metrics.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

pytest -q
python -m genfin run      # → artifacts/*.json
python -m genfin report   # → reports/RESULTS.md (from JSON only)
python -m genfin demo     # one-event sample texts
```

Optional UI:

```bash
streamlit run app/streamlit_app.py
```

## Study design (locked)

- **10 events** E01–E10 (USDT/USDC; fact cards with typed numbers)
- **4 variants:** `anchored`, `persuade_bull`, `persuade_bear`, `paraphrase`
- **4 computational personas** (not human subjects)
- **3 seeds** → **480 belief cells**
- Deterministic templates + controlled corruptions (offline; no paid APIs)

Pre-registered falsification thresholds live in `config/study.yaml` and `PROTOCOL.md` §7.

## Repository layout

```
GenFinTextEval/
  PROTOCOL.md
  config/study.yaml
  data/events/          # fact cards
  data/personas.yaml
  data/lexicons/
  src/genfin/           # generators + A/B/C metrics + CLI
  artifacts/            # JSON after `python -m genfin run`
  reports/RESULTS.md    # after `python -m genfin report`
  reports/THESIS_NOTES.md
  docs/SECURITY_ETHICS.md
  tests/
  app/streamlit_app.py
```

## Security / ethics

Synthetic discourse for research evaluation only. **Not** market manipulation advice. See [`docs/SECURITY_ETHICS.md`](docs/SECURITY_ETHICS.md).

## Citation

Hossein Tabasi. *GenFinTextEval: Evaluating generative financial text across text, belief, and system layers.* 2026. MIT License.
