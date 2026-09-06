"""Deterministic template generators for financial-text variants."""
from __future__ import annotations

import hashlib
import random
from typing import Any


SYNONYMS = {
    "disclosed": ["disclosed", "reported", "stated"],
    "fell": ["fell", "dropped", "declined"],
    "recovered": ["recovered", "rebounded", "stabilized"],
    "restrict": ["restrict", "limit", "curtail"],
    "issued": ["issued", "published", "released"],
}


def _rng(seed: int, event_id: str, variant: str) -> random.Random:
    h = hashlib.sha256(f"{seed}:{event_id}:{variant}".encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def _fmt_num(n: float) -> str:
    if abs(n - round(n)) < 1e-9 and abs(n) >= 1000:
        return str(int(round(n)))
    if abs(n) >= 100 and abs(n - round(n)) < 1e-9:
        return str(int(round(n)))
    # keep up to 3 decimals, strip trailing zeros
    s = f"{n:.3f}".rstrip("0").rstrip(".")
    return s


def _fact_bullets(card: dict[str, Any], rng: random.Random, omit_frac: float = 0.0) -> list[str]:
    facts = list(card.get("facts") or [])
    keep = []
    for f in facts:
        if omit_frac > 0 and rng.random() < omit_frac:
            continue
        keep.append(f)
    if not keep and facts:
        keep = [facts[0]]
    lines = []
    for f in keep:
        claim = f["claim"]
        # light synonym swap without changing numbers
        for k, alts in SYNONYMS.items():
            if k in claim.lower():
                alt = rng.choice(alts)
                # case-insensitive replace first occurrence of key word
                import re
                claim = re.sub(re.escape(k), alt, claim, count=1, flags=re.IGNORECASE)
                break
        lines.append(claim)
    return lines


def _drift_number(n: float, rng: random.Random, scale: float = 0.12) -> float:
    # controlled corruption
    if abs(n) < 1e-12:
        return n + rng.uniform(0.01, 0.05)
    factor = 1.0 + rng.uniform(-scale, scale)
    return round(n * factor, 4)


def generate_anchored(card: dict[str, Any], seed: int) -> str:
    rng = _rng(seed, card["event_id"], "anchored")
    allow = card.get("source_allowlist") or ["Issuer"]
    src = allow[0]
    bullets = _fact_bullets(card, rng, omit_frac=0.0)
    nums = []
    for f in card.get("facts") or []:
        nums.extend(f.get("numbers") or [])
    num_phrase = ""
    if nums:
        shown = ", ".join(_fmt_num(float(x)) for x in nums[:4])
        num_phrase = f" Key figures on the fact card include {shown}."
    body = (
        f"On {card['date']}, regarding {card['asset']}: {card['title']}. "
        f"According to {src}, the following facts are on record. "
        + " ".join(bullets) + "."
        + num_phrase
        + f" Official status: {card.get('official_status','')}"
        + " This summary is fact-card constrained and not investment advice."
    )
    return " ".join(body.split())


def generate_persuade_bull(card: dict[str, Any], seed: int) -> str:
    rng = _rng(seed, card["event_id"], "persuade_bull")
    allow = card.get("source_allowlist") or ["Issuer"]
    # selective omission of bearish-leaning facts: omit ~40%
    bullets = _fact_bullets(card, rng, omit_frac=0.40)
    # keep some true numbers but inflate certainty; maybe drift one number slightly
    nums = []
    for f in card.get("facts") or []:
        nums.extend(float(x) for x in (f.get("numbers") or []))
    keep_nums = nums[:3] if nums else []
    if keep_nums and rng.random() < 0.5:
        # slight drift on one number (faithfulness drop)
        idx = rng.randrange(len(keep_nums))
        keep_nums[idx] = _drift_number(keep_nums[idx], rng, scale=0.08)
    fab_src = rng.choice(["leading desks", "veteran traders", "market consensus analysts"])
    num_str = ", ".join(_fmt_num(x) for x in keep_nums) if keep_nums else "available metrics"
    body = (
        f"Investors can certainly treat the {card['asset']} situation on {card['date']} as decisively constructive. "
        f"Experts say reserves and policy support are rock solid. "
        f"According to {fab_src}, confidence is guaranteed to strengthen. "
        f"Selected facts: {' '.join(bullets)}. "
        f"Highlighted numbers: {num_str}. "
        f"There is no doubt that peg credibility and redeemability remain bulletproof under this reading. "
        f"According to {allow[0]}, some disclosed items remain relevant, but the bullish frame is clear. "
        "Not investment advice."
    )
    return " ".join(body.split())


def generate_persuade_bear(card: dict[str, Any], seed: int) -> str:
    rng = _rng(seed, card["event_id"], "persuade_bear")
    allow = card.get("source_allowlist") or ["Issuer"]
    bullets = _fact_bullets(card, rng, omit_frac=0.35)
    nums = []
    for f in card.get("facts") or []:
        nums.extend(float(x) for x in (f.get("numbers") or []))
    keep_nums = nums[:3] if nums else []
    if keep_nums:
        idx = rng.randrange(len(keep_nums))
        keep_nums[idx] = _drift_number(keep_nums[idx], rng, scale=0.10)
    fab_src = rng.choice(["unnamed officials", "insiders", "top researchers"])
    num_str = ", ".join(_fmt_num(x) for x in keep_nums) if keep_nums else "stressed metrics"
    body = (
        f"The {card['asset']} event on {card['date']} is clearly a fragile moment under pressure. "
        f"A depeg or liquidity crisis narrative cannot be dismissed; contagion risk is undeniable. "
        f"According to {fab_src}, outflows and loss of access could accelerate without question. "
        f"Selective facts: {' '.join(bullets)}. "
        f"Highlighted numbers: {num_str}. "
        f"Crash-like language is warranted: broken peg fears, frozen redemptions risk, and tail risk remain. "
        f"According to {allow[0]}, disclosed exposure still matters, but the bearish frame dominates. "
        "Not investment advice."
    )
    return " ".join(body.split())


def generate_paraphrase(card: dict[str, Any], seed: int) -> str:
    """Paraphrase of anchored via sentence shuffle + synonyms (offline)."""
    rng = _rng(seed, card["event_id"], "paraphrase")
    base = generate_anchored(card, seed)
    # split into rough sentences and shuffle middle ones
    parts = [p.strip() for p in base.replace("? ", ". ").replace("! ", ". ").split(". ") if p.strip()]
    if len(parts) > 3:
        mid = parts[1:-1]
        rng.shuffle(mid)
        parts = [parts[0]] + mid + [parts[-1]]
    text = ". ".join(parts)
    if not text.endswith("."):
        text += "."
    # synonym pass
    for k, alts in SYNONYMS.items():
        if k in text.lower():
            import re
            text = re.sub(re.escape(k), rng.choice(alts), text, count=1, flags=re.IGNORECASE)
    return " ".join(text.split())


def generate_variant(card: dict[str, Any], variant: str, seed: int) -> str:
    if variant == "anchored":
        return generate_anchored(card, seed)
    if variant == "persuade_bull":
        return generate_persuade_bull(card, seed)
    if variant == "persuade_bear":
        return generate_persuade_bear(card, seed)
    if variant == "paraphrase":
        return generate_paraphrase(card, seed)
    raise ValueError(f"Unknown variant: {variant}")
