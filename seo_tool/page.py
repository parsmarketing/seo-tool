"""Paginacheck: on-page en technische basiselementen van één URL, plus robots.txt en sitemap."""

from __future__ import annotations

import json
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; SEO-Tool/0.1; +https://github.com/parsmarketing/seo-tool)"


def _get(url: str, **kw) -> requests.Response:
    return requests.get(url, headers={"User-Agent": UA}, timeout=30, **kw)


def analyse(url: str) -> dict:
    resp = _get(url, allow_redirects=True)
    redirects = [{"url": r.url, "status": r.status_code} for r in resp.history]
    out: dict = {
        "gevraagde_url": url,
        "eind_url": resp.url,
        "status": resp.status_code,
        "redirects": redirects,
        "x_robots_tag": resp.headers.get("X-Robots-Tag"),
        "content_type": resp.headers.get("Content-Type"),
    }
    if "html" not in (resp.headers.get("Content-Type") or ""):
        return out
    soup = BeautifulSoup(resp.text, "html.parser")
    host = urlparse(resp.url).netloc

    def meta(name: str) -> str | None:
        tag = soup.find("meta", attrs={"name": re.compile(f"^{name}$", re.I)})
        return tag.get("content") if tag else None

    title = soup.title.get_text(strip=True) if soup.title else None
    desc = meta("description")
    canonical = soup.find("link", rel=lambda v: v and "canonical" in v)
    out.update(
        title=title,
        title_lengte=len(title) if title else 0,
        meta_description=desc,
        meta_description_lengte=len(desc) if desc else 0,
        meta_robots=meta("robots"),
        canonical=canonical.get("href") if canonical else None,
        lang=(soup.html.get("lang") if soup.html else None),
        hreflang=[
            {"lang": l.get("hreflang"), "href": l.get("href")}
            for l in soup.find_all("link", rel=lambda v: v and "alternate" in v)
            if l.get("hreflang")
        ],
        headings={
            f"h{i}": [h.get_text(" ", strip=True) for h in soup.find_all(f"h{i}")]
            for i in range(1, 4)
        },
        og={
            m.get("property"): m.get("content")
            for m in soup.find_all("meta", property=re.compile(r"^og:"))
        },
    )

    schema_types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except (json.JSONDecodeError, TypeError):
            schema_types.append("ONGELDIGE JSON-LD")
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data])
        for it in items:
            if isinstance(it, dict):
                t = it.get("@type")
                schema_types.extend(t if isinstance(t, list) else [t])
    out["schema_types"] = [t for t in schema_types if t]

    imgs = soup.find_all("img")
    out["afbeeldingen"] = len(imgs)
    out["afbeeldingen_zonder_alt"] = [i.get("src") for i in imgs if not (i.get("alt") or "").strip()][:20]

    internal, external = [], []
    for a in soup.find_all("a", href=True):
        href = urljoin(resp.url, a["href"])
        if not href.startswith("http"):
            continue
        item = {"href": href.split("#")[0], "anker": a.get_text(" ", strip=True)[:100]}
        (internal if urlparse(href).netloc == host else external).append(item)
    out["interne_links"] = len(internal)
    out["externe_links"] = len(external)
    out["interne_links_lijst"] = internal[:200]

    for tag in soup(["script", "style", "noscript", "nav", "footer", "header"]):
        tag.decompose()
    body = soup.body or soup
    text = body.get_text(" ", strip=True)
    out["woorden"] = len(text.split())
    out["tekst"] = text[:15000]
    return out


def site_checks(base_url: str) -> dict:
    """robots.txt en sitemap(s) van een domein."""
    base = base_url.rstrip("/")
    out: dict = {}
    try:
        r = _get(f"{base}/robots.txt")
        out["robots_status"] = r.status_code
        robots = r.text if r.ok else ""
        out["robots_txt"] = robots[:5000]
        sitemaps = re.findall(r"(?im)^sitemap:\s*(\S+)", robots)
    except requests.RequestException as e:
        out["robots_fout"] = str(e)
        sitemaps = []
    if not sitemaps:
        sitemaps = [f"{base}/sitemap.xml"]
    out["sitemaps"] = []
    for sm in sitemaps[:5]:
        try:
            r = _get(sm)
            out["sitemaps"].append({
                "url": sm,
                "status": r.status_code,
                "urls": r.text.count("<loc>") if r.ok else 0,
                "is_index": "<sitemapindex" in r.text[:1000],
            })
        except requests.RequestException as e:
            out["sitemaps"].append({"url": sm, "fout": str(e)})
    return out
