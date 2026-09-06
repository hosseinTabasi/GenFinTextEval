# GenFinTextEval Results

**Study ID:** `genfin_v1`
**Generated (UTC):** 2026-09-06T15:47:45.867071+00:00

All numbers below are read from `artifacts/*.json`. No invented values.

## Study size

- Events: **10**
- Variants: **4**
- Personas: **4**
- Seeds: **3**
- Belief cells (persona × event × variant × seed): **480**
- Text cells (event × variant × seed): **120**

## RQ falsification (pre-registered)

- Rule: Claim fails if persuade variants do not increase mean |Δμ| vs anchored by margin_belief AND contamination slope magnitude is below slope_flat.
- `margin_belief` = 0.03
- `slope_flat` = 0.005
- Belief lift (persuade − anchored) mean |Δμ|: **0.107955** → belief_effect=True
- |contamination slope| (persuade mix): **0.169565** → contamination_effect=True
- **Claim passes:** `True`
- **Claim fails:** `False`

## Layer A — text

| Variant | Faithfulness | Fabrication (mean count) | Certainty | Hedge |
|---|---:|---:|---:|---:|
| anchored | 0.975 | 0.0 | 0.014286 | 0.077638 |
| persuade_bull | 0.851984 | 1.0 | 0.481624 | 0.036152 |
| persuade_bear | 0.802897 | 1.0 | 0.191739 | 0.1353 |
| paraphrase | 0.975 | 0.0 | 0.014286 | 0.077638 |

- Mean frame stability (Jaccard, paraphrase vs anchored): **0.991575**

## Layer B — belief

- Mean |Δμ| anchored: **0.111919**
- Mean |Δμ| persuade_bull: **0.295947**
- Mean |Δμ| persuade_bear: **0.1438**
- Mean |Δμ| persuade (pooled): **0.219874**

| Variant | Cross-persona disagreement (mean) | Willingness-to-act rate |
|---|---:|---:|
| anchored | 0.102403 | 0.566667 |
| persuade_bull | 0.06454 | 0.741667 |
| persuade_bear | 0.120107 | 0.458333 |
| paraphrase | 0.102403 | 0.566667 |

## Layer C — system

- Mean persuade contamination slope (bias vs ρ): **-0.169565**

### Contamination sweep (persuade contaminant)

| Seed | ρ | Sentiment index | Bias vs ρ=0 | Slope |
|---:|---:|---:|---:|---:|
| 20260311 | 0.0 | 0.098333 | 0.0 | -0.125383 |
| 20260311 | 0.1 | 0.059028 | -0.039306 | -0.125383 |
| 20260311 | 0.25 | 0.0925 | -0.005833 | -0.125383 |
| 20260311 | 0.5 | 0.016806 | -0.081528 | -0.125383 |
| 20260311 | 0.75 | 0.002639 | -0.095694 | -0.125383 |
| 20260813 | 0.0 | 0.211667 | 0.0 | -0.175994 |
| 20260813 | 0.1 | 0.19125 | -0.020417 | -0.175994 |
| 20260813 | 0.25 | 0.13875 | -0.072917 | -0.175994 |
| 20260813 | 0.5 | 0.09625 | -0.115417 | -0.175994 |
| 20260813 | 0.75 | 0.085 | -0.126667 | -0.175994 |
| 20260101 | 0.0 | 0.17 | 0.0 | -0.207317 |
| 20260101 | 0.1 | 0.152917 | -0.017083 | -0.207317 |
| 20260101 | 0.25 | 0.1525 | -0.0175 | -0.207317 |
| 20260101 | 0.5 | 0.097917 | -0.072083 | -0.207317 |
| 20260101 | 0.75 | 0.00875 | -0.16125 | -0.207317 |

### Amplification / tail language

| Seed | Mean reuse | Max reuse | Herfindahl | Tail frac (all) |
|---:|---:|---:|---:|---:|
| 20260311 | 0.2 | 2.0 | 0.21875 | 0.35 |
| 20260813 | 0.2 | 4.0 | 0.3125 | 0.35 |
| 20260101 | 0.2 | 3.0 | 0.25 | 0.35 |

Tail language fraction by variant (mean across seeds):

- `anchored`: **0.2**
- `persuade_bull`: **0.0**
- `persuade_bear`: **1.0**
- `paraphrase`: **0.2**

## Artifact paths

- `artifacts/summary.json`
- `artifacts/texts.json`
- `artifacts/layer_a.json`
- `artifacts/belief.json`
- `artifacts/contamination.json`
- `artifacts/amplification.json`

_Belief row count check: 480; Layer A row count: 120._
