"""Google Autocomplete: gratis zoekwoordideeën (zonder volumes)."""

from __future__ import annotations

import string
import time

import requests

API = "https://suggestqueries.google.com/complete/search"

QUESTION_PREFIXES = {
    "nl": ["wat", "hoe", "waarom", "welke", "wanneer", "waar", "wie", "kan", "is", "beste", "kosten", "vs"],
    "en": ["what", "how", "why", "which", "when", "where", "who", "can", "is", "best", "cost", "vs"],
}


def fetch(q: str, lang: str = "nl", country: str = "nl") -> list[str]:
    resp = requests.get(
        API,
        params={"client": "firefox", "q": q, "hl": lang, "gl": country},
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    resp.raise_for_status()
    data = resp.json()
    return data[1] if len(data) > 1 else []


def expand(seed: str, lang: str = "nl", country: str = "nl", deep: bool = True, delay: float = 0.3) -> list[dict]:
    """Seed + a-z + vraagwoorden. Geeft rijen {seed, bron, suggestie}."""
    queries = [(seed, "seed")]
    if deep:
        queries += [(f"{seed} {c}", f"seed+{c}") for c in string.ascii_lowercase]
        queries += [(f"{p} {seed}", f"vraag:{p}") for p in QUESTION_PREFIXES.get(lang, QUESTION_PREFIXES["en"])]
    seen: set[str] = set()
    rows = []
    for q, source in queries:
        try:
            suggestions = fetch(q, lang, country)
        except requests.RequestException:
            continue
        for s in suggestions:
            s = s.strip().lower()
            if s and s not in seen:
                seen.add(s)
                rows.append({"seed": seed, "bron": source, "suggestie": s})
        time.sleep(delay)
    return rows
