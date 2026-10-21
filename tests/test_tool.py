from unittest.mock import MagicMock, patch

from seo_tool import gsc, page, pagespeed
from seo_tool.clients import load_client


def test_previous_range_same_length():
    assert gsc.previous_range("2026-09-01", "2026-09-30") == ("2026-08-02", "2026-08-31")


def test_compare_includes_lost_rows_and_sorts_by_drop():
    cur = [{"query": "a", "clicks": 5, "impressions": 50, "ctr": 0.1, "position": 3.0}]
    prev = [
        {"query": "a", "clicks": 10, "impressions": 60, "ctr": 0.16, "position": 2.0},
        {"query": "b", "clicks": 20, "impressions": 100, "ctr": 0.2, "position": 1.5},
    ]
    rows = gsc.compare(cur, prev, ["query"])
    assert [r["query"] for r in rows] == ["b", "a"]
    assert rows[0]["clicks"] == 0 and rows[0]["clicks_diff"] == -20
    assert rows[1]["position_diff"] == 1.0


def test_pagespeed_rating_and_cls_scaling():
    data = {
        "id": "https://x.nl/",
        "loadingExperience": {"metrics": {
            "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 3000},
            "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 5},
            "INTERACTION_TO_NEXT_PAINT": {"percentile": 600},
        }},
        "lighthouseResult": {
            "categories": {"performance": {"score": 0.42, "auditRefs": []}, "seo": {"score": 0.9, "auditRefs": [{"id": "meta-description"}]}},
            "audits": {
                "meta-description": {"title": "Geen meta description", "score": 0},
                "render-blocking-resources": {"title": "Render-blocking", "score": 0, "details": {"type": "opportunity", "overallSavingsMs": 900}},
            },
        },
    }
    out = pagespeed.summarise(data, "mobile")
    f = out["velddata_pagina"]
    assert f["LCP"]["oordeel"] == "verbetering nodig"
    assert f["CLS"] == {"p75": 0.05, "oordeel": "goed"}
    assert f["INP"]["oordeel"] == "slecht"
    assert out["lighthouse_scores"]["performance"] == 42
    assert out["kansen"][0]["besparing_ms"] == 900
    assert out["seo_audits_gefaald"] == ["Geen meta description"]
    assert isinstance(out["velddata_origin"], str)


HTML = """<html lang="nl"><head><title>Bakker in Utrecht | Jansen</title>
<meta name="description" content="Vers brood"><link rel="canonical" href="https://jansen.nl/">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Bakery"},{"@type":"WebSite"}]}</script>
</head><body><nav>menu</nav><h1>Welkom</h1><h2>Brood</h2><img src="a.jpg"><img src="b.jpg" alt="taart">
<a href="/contact">Contact</a><a href="https://elders.nl">Elders</a><p>Wij bakken elke dag vers brood.</p></body></html>"""


def test_page_analyse_extracts_elements():
    resp = MagicMock(status_code=200, url="https://jansen.nl/", text=HTML, history=[],
                     headers={"Content-Type": "text/html; charset=utf-8"})
    with patch.object(page, "_get", return_value=resp):
        out = page.analyse("https://jansen.nl/")
    assert out["title_lengte"] == len("Bakker in Utrecht | Jansen")
    assert out["canonical"] == "https://jansen.nl/"
    assert out["lang"] == "nl"
    assert out["headings"]["h1"] == ["Welkom"]
    assert out["schema_types"] == ["Bakery", "WebSite"]
    assert out["afbeeldingen_zonder_alt"] == ["a.jpg"]
    assert out["interne_links"] == 1 and out["externe_links"] == 1
    assert "menu" not in out["tekst"]


def test_load_client(tmp_path, monkeypatch):
    from seo_tool import clients

    d = tmp_path / "jansen"
    d.mkdir()
    (d / "client.toml").write_text(
        '[klant]\nnaam="Jansen"\ndomein="jansen.nl"\n[koppelingen]\ngsc_property="sc-domain:jansen.nl"\nga4_property_id=123\n'
    )
    monkeypatch.setattr(clients, "CLIENTS_DIR", tmp_path)
    c = load_client("jansen")
    assert c.base_url == "https://jansen.nl"
    assert c.ga4_property_id == "123"
    assert clients.list_clients() == ["jansen"]
