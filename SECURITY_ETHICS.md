# Security and ethics

**Author:** Hossein Tabasi  
**Project:** GenFinTextEval

## Purpose

This repository evaluates **synthetic financial discourse** under locked fact cards for research and thesis writing. It is a closed experimental loop.

## Allowed use

- Academic study of faithfulness, belief-update proxies, and corpus contamination.
- Offline, seedable template generation with declared lab or sourced fact cards.
- Teaching demonstrations of evaluation design (Layers A/B/C).

## Prohibited use

- Advising or executing **market manipulation**, wash trading, spoofing, or coordinated deception.
- Publishing fabricated “according to &lt;ORG&gt;” claims as real news.
- Deploying persuasion-steered variants to social platforms as authentic human or official speech.
- Treating computational persona outputs as investment advice or as evidence about named living persons.

## Design mitigations

- Persuasion variants are labeled in metadata (`persuade_bull` / `persuade_bear`).
- Fabricated sources are **metrics targets** (Layer A fabrication count), not endorsed attributions.
- Every demo path states texts are not investment advice.
- Lab fixtures, if any, must be marked `lab_fixture` / “not market history.”
- No live posting, brokerage, or order-routing modules exist in this repo.

## Data

Event numbers are copied from previously verified public fact cards used in the author’s SynthOpinion / EchoMarket protocols, or declared as lab fixtures. Do not invent new ticker events or statistics without sourcing or an explicit lab label.

## Contact

Repository author: Hossein Tabasi (`hosseinTabasi` on GitHub).
