# Thesis notes — Master’s deliverable vs limitations

**Author:** Hossein Tabasi  
**Project:** GenFinTextEval

## Intellectual mandate (enforce in write-up)

Financial text generation is interesting only if it changes an identifiable object: beliefs, disagreement, attention, credibility, or a market/platform outcome. Do not lead with BLEU/ROUGE/perplexity. Distinguish surface / epistemic / strategic / ecological generation. Always report Layers A+B+C.

Label claims: **definitional / descriptive / causal / speculative**.

## What a Master’s thesis can realistically deliver

1. **Locked protocol** with sharpened RQ, constructs, identification threats, and pre-registered falsifiers (`PROTOCOL.md`).
2. **Fact-card library** for ten USDT/USDC events with typed numbers and source allowlists (aligned with verified cards from prior work by the same author).
3. **Deterministic generators** for anchored vs persuasion-steered vs paraphrase variants (seedable, offline).
4. **Measured A/B/C tables** from JSON artifacts (≥200 belief cells; design N=480).
5. **Falsification outcome** against pre-registered margins (belief lift and contamination slope).
6. **Positioning** relative to SynthOpinion (opinion quality / belief direction) and EchoMarket (cascade ecology) without conflating claims.
7. **Ethics / security** section on synthetic discourse and non-use for manipulation.

## Limitations (state explicitly)

- Computational personas ≠ human investors (**definitional** boundary).
- Bag-of-texts sentiment index ≠ live trading venue index.
- Template generators bound internal validity; external validity to large neural decoders is **speculative** until replicated with held-out decoders.
- Event confounding can never be fully eliminated; within-event contrasts only **bound** it.
- No human-subjects IRB study in this repository.
- Held-out events E09–E10 are reported descriptively under the same generator; they are not a separate fitted model test.

## Suggested chapter map

1. Motivation: persuasion under fixed facts in digital-money narratives (peg, solvency, regulation, social proof).
2. Related work and claim hygiene (taxonomy).
3. Protocol and identification.
4. Implementation (deterministic stack).
5. Results (A/B/C + falsification) — numbers only from `reports/RESULTS.md`.
6. Limitations and PhD-scale extensions (human elicitation; platform contamination field studies; calibrated automatic judge as secondary audit).

## PhD-scale extensions (out of scope for Master’s delivery)

- Human belief elicitation with pre-registered personas matched to computational ones.
- Field or quasi-experimental contamination of public sentiment dashboards.
- Strategic decoder families beyond templates, still fact-card locked.
- Formal bounds on event confounding (e.g., synthetic lab events with randomized “true” polarity).
