# GenFinTextEval Experimental Protocol

**Project:** GenFinTextEval — a methods-grade evaluation framework for generative financial text that treats generation as interesting only when it changes an identifiable object: beliefs, disagreement, attention, credibility, or a market/platform outcome.

**Author:** Hossein Tabasi, M.Tech Computer Science and Engineering, Shoolini University. GitHub: `hosseinTabasi`.

**License:** MIT.

**Assets in scope:** USD Tether (USDT) and USD Coin (USDC), plus clearly labeled lab fixtures when used.

**Version:** 1.0 (deterministic template / rule generation; offline; seedable).

**Related work by the same author (do not conflate claims):** SynthOpinion (fact-card synthetic opinion; belief-direction alignment) and EchoMarket (multi-agent cascade shapes). This project is a **new** evaluation stack (Text / Belief / System layers) with its own generators, metrics, and falsifiers.

**Intellectual mandate.** Reject BLEU / ROUGE / perplexity as primary claims. Distinguish **surface** generation (fluency), **epistemic** generation (belief update), **strategic** generation (persuasion under fixed facts), and **ecological** generation (corpus contamination / amplification). Evaluation **must** include layers A+B+C. A-only is too weak; C without A+B is sloppy.

**Generator name.** The writer is a **deterministic template generator** with controlled corruptions (number drift, fabricated source strings, hedge/certainty lexicon). Optional paraphrase uses synonym tables and sentence shuffle. No paid external decoder is required for the confirmatory study.

No output is investment advice. No module places live posts or executes trades.

---

## Claim taxonomy (label every claim)

| Label | Meaning |
|-------|---------|
| **definitional** | How a construct is named or measured in this protocol |
| **descriptive** | What the offline study observed under locked seeds |
| **causal** | What the design would identify if confounders were bounded |
| **speculative** | Extrapolation beyond the computational personas / bag-of-texts index |

Primary RQ claim type for the Master’s write-up: **causal** *within the computational design*, reported with identification threats; empirical tables are **descriptive** of the seeded study.

---

## Unit of analysis

- **Belief (Layer B):** `investor-persona × event × text-variant` (and seed as replication).
- **System / contamination (Layer C):** `corpus-day / window` operationalized as a bag-of-texts fixture of fixed size with contamination rate ρ.

---

## Counterfactual

Holding the **event fact card** fixed, compare:

1. **fact-anchored rewrite** (`anchored`)
2. **persuasion-steered rewrite** (`persuade_bull` / `persuade_bear`: omission, certainty inflation, authority cues; some facts retained)
3. **paraphrase** of anchored (frame-stability probe)
4. **human/baseline discourse excerpt** (Layer C baseline corpus is a deterministic fixture standing in for baseline desk notes — not claimed as scraped market history)

---

## Identification threats (named and bounded)

1. **Confounding by the underlying news event itself** — event polarity and magnitude can drive belief moves even under anchored text. **Bound:** hold the fact card fixed across variants; report within-event contrasts (persuade − anchored); include events with positive, negative, and unknown peg paths.
2. **Prompt / template sensitivity** — strategic effects may be template artifacts. **Bound:** ≥3 seeds; synonym/shuffle paraphrase; document templates in `src/genfin/generate.py`; falsify if lift is not robust across seeds.
3. **Contamination of outcome by treatment** — if the sentiment index or belief features are computed from the same strings used as treatment without separation of layers, circularity rises. **Bound:** Layer A features are text-intrinsic; Layer B uses a documented formula; Layer C mixes into a separate baseline corpus and reports bias vs ρ=0.

---

## Theoretical tensions

- **Information vs persuasion** — same fact card, different frames.
- **Disagreement vs consensus** — cross-persona σ(μ) after exposure.
- **Authenticity vs polish** — anchored faithfulness vs certainty-inflated prose.
- **Contamination** — synthetic share ρ in a sentiment index.
- **Digital-money specificity** — peg, solvency/reserves, regulation, social-proof / venue access for USDT/USDC.

---

## 1. Sharpened question

**RQ:** Relative to a fact-card-constrained baseline, do strategically framed generative financial texts (omission / certainty inflation / authority cues) produce larger persona belief updates and greater contamination bias in a bag-of-texts sentiment index, holding the event fact card fixed?

Claim labels: the RQ is posed as a **causal** question inside a computational design; the offline run reports **descriptive** pass/fail against pre-registered thresholds.

---

## 2. Why it is not trivial

Surface fluency metrics do not tell whether a rewrite changes **beliefs**, **disagreement**, or **index contamination**. Strategic framing can move computational personas while degrading numerical faithfulness — a tradeoff invisible to BLEU/ROUGE. Conversely, a contaminated sentiment index can shift under high ρ even when Layer A looks “fine.” The non-trivial object is the **joint** A+B+C profile under a fixed fact card.

---

## 3. Construct and outcome

| Layer | Construct | Primary outcomes |
|-------|-----------|------------------|
| A Text | Faithfulness & rhetoric | numerical faithfulness; source fabrication count; hedge ratio; certainty score; frame stability (Jaccard) |
| B Belief | Epistemic update | Δμ; Δconfidence; cross-persona disagreement; willingness-to-act proxy (formula in `metrics_belief.py`: tanh(s)×scale×strategic; strategic = 1 + 1.25·certainty·|polarity| + 0.85·authority) |
| C System | Ecological bias | sentiment-index bias vs ρ; contamination slope; amplification reuse; crash/depeg tail-language fraction |

Personas are **computational** (documented priors and weights). No invented human subjects.

---

## 4. Design / identification

- **Events:** ten sourced USDT/USDC events E01–E10 (fact cards aligned with prior SynthOpinion/EchoMarket verified cards). Split: E01–E08 dev; E09–E10 held-out for descriptive reporting (same generator; no fitting).
- **Variants:** `anchored`, `persuade_bull`, `persuade_bear`, `paraphrase`.
- **Personas:** ≥4 (`risk_officer`, `retail_momentum`, `skeptical_analyst`, `macro_allocator`).
- **Seeds:** `[20260311, 20260813, 20260101]`.
- **Factorial:** events × variants × personas × seeds → target **≥ 200** belief cells (design N = 10 × 4 × 4 × 3 = **480**).
- **Identification:** within-event contrast of persuade vs anchored holds the fact card fixed; contamination sweep varies only ρ.

---

## 5. Data and generation protocol

1. Load fact cards from `data/events/*.yaml` (typed numbers + source allowlist).
2. Generate texts with `src/genfin/generate.py` (deterministic RNG keyed by `seed:event:variant`).
3. `anchored`: all fact bullets; allowlisted attribution; no fabricated orgs.
4. `persuade_*`: omit a seeded fraction of facts; inflate certainty / crash lexicon; inject fabricated “according to …” authority strings; optional mild number drift.
5. `paraphrase`: shuffle middle sentences + synonym table on the anchored text.
6. Measure Layer A → B → C; write `artifacts/*.json`; `reports/RESULTS.md` **only** from JSON.

---

## 6. Principal confound and how you would bound it

**Principal confound:** the **underlying news event** (e.g., a real depeg day) can dominate Δμ regardless of framing.

**Bounds in this protocol:**

- within-event persuade − anchored contrasts;
- mix of event polarities and unknown peg-path events;
- report Layer A degradation (faithfulness ↓, fabrication ↑) as a manipulation check that framing is not “free”;
- multi-seed replication;
- pre-registered falsification thresholds (Section 7).

Residual threats (template family; lexicon-based polarity) remain and are listed as Master’s limitations.

---

## 7. What result would falsify the claim

Pre-registered in `config/study.yaml`:

- `margin_belief = 0.03`
- `slope_flat = 0.005`

**Claim fails if** (i) mean `|Δμ|` for persuade variants does **not** exceed anchored by at least `margin_belief` **AND** (ii) absolute contamination slope (persuade mix) is **below** `slope_flat`.

Otherwise the claim **passes** the pre-registered bar (still subject to identification caveats in Section 6). Pass/fail is written from `artifacts/summary.json` into `reports/RESULTS.md`.

---

## 8. What a Master’s thesis can realistically deliver vs limitations

**Deliverable:** a complete offline evaluation framework with locked protocol, deterministic generators, A/B/C metrics, 480 belief cells, contamination sweep, falsification table, and thesis notes linking to SynthOpinion/EchoMarket as related work.

**Not delivered here:** human-subject belief elicitation; live market causal estimates; trained sequence models; publisher-scale ecological experiments; proof that computational personas equal investors.

See `reports/THESIS_NOTES.md`.

---

## Generation typology (definitional)

| Type | Question |
|------|----------|
| Surface | Is the text fluent / diverse? (secondary only) |
| Epistemic | Does exposure change μ, confidence, disagreement? |
| Strategic | Does persuasion steering change outcomes under fixed facts? |
| Ecological | Does mixing synthetic text bias an index or amplify tails? |
