"""PageSpeed Insights: Core Web Vitals (velddata via CrUX) en labdata."""

from __future__ import annotations

import os

import requests

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# Drempels volgens web.dev (goed / verbetering nodig / slecht), p75
THRESHOLDS = {
    "LCP": (2500, 4000),          # ms
    "INP": (200, 500),            # ms
    "CLS": (0.1, 0.25),           # unitless
    "FCP": (1800, 3000),          # ms
    "TTFB": (800, 1800),          # ms
}

FIELD_KEYS = {
    "LARGEST_CONTENTFUL_PAINT_MS": "LCP",
    "INTERACTION_TO_NEXT_PAINT": "INP",
    "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS",
    "FIRST_CONTENTFUL_PAINT_MS": "FCP",
    "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "TTFB",
}


def rate(metric: str, value: float) -> str:
    good, poor = THRESHOLDS[metric]
    if value <= good:
        return "goed"
    if value <= poor:
        return "verbetering nodig"
    return "slecht"


def run(url: str, strategy: str = "mobile", locale: str = "nl") -> dict:
    params = {"url": url, "strategy": strategy, "locale": locale, "category": ["performance", "seo"]}
    key = os.environ.get("PAGESPEED_API_KEY")
    if key:
        params["key"] = key
    resp = requests.get(API, params=params, timeout=120)
    if resp.status_code == 429:
        raise SystemExit("PageSpeed-limiet bereikt. Zet PAGESPEED_API_KEY in .env (gratis aan te maken).")
    resp.raise_for_status()
    return summarise(resp.json(), strategy)


def summarise(data: dict, strategy: str) -> dict:
    out: dict = {"url": data.get("id"), "strategy": strategy}

    def field(block: dict | None) -> dict:
        res = {}
        for k, v in (block or {}).get("metrics", {}).items():
            name = FIELD_KEYS.get(k)
            if not name:
                continue
            p = v.get("percentile")
            if name == "CLS" and p is not None:
                p = p / 100  # API geeft CLS x100
            res[name] = {"p75": p, "oordeel": rate(name, p) if p is not None else None}
        return res

    out["velddata_pagina"] = field(data.get("loadingExperience")) or "Geen CrUX-velddata voor deze URL"
    out["velddata_origin"] = field(data.get("originLoadingExperience")) or "Geen CrUX-velddata voor dit domein"

    lh = data.get("lighthouseResult", {})
    cats = lh.get("categories", {})
    out["lighthouse_scores"] = {k: round((v.get("score") or 0) * 100) for k, v in cats.items()}
    audits = lh.get("audits", {})
    out["labdata"] = {
        name: audits[a].get("displayValue")
        for name, a in [
            ("LCP", "largest-contentful-paint"),
            ("CLS", "cumulative-layout-shift"),
            ("TBT", "total-blocking-time"),
            ("FCP", "first-contentful-paint"),
            ("Speed Index", "speed-index"),
        ]
        if a in audits
    }
    opps = []
    for a in audits.values():
        details = a.get("details") or {}
        score = a.get("score")
        if details.get("type") == "opportunity" and score is not None and score < 0.9:
            opps.append({
                "audit": a.get("title"),
                "besparing_ms": round(details.get("overallSavingsMs") or 0),
                "toelichting": a.get("displayValue"),
            })
    out["kansen"] = sorted(opps, key=lambda o: -o["besparing_ms"])[:10]
    failed_seo = [
        a.get("title") for k in cats.get("seo", {}).get("auditRefs", [])
        if (a := audits.get(k["id"])) and a.get("score") == 0
    ]
    out["seo_audits_gefaald"] = failed_seo
    return out
