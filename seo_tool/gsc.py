"""Google Search Console: zoekprestaties ophalen."""

from __future__ import annotations

from datetime import date, timedelta

from .google_auth import get_credentials

MAX_ROWS = 25000  # maximum per request volgens de API


def default_range(days: int) -> tuple[str, str]:
    # GSC-data loopt ongeveer 2-3 dagen achter
    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def previous_range(start: str, end: str) -> tuple[str, str]:
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    length = (e - s).days + 1
    prev_end = s - timedelta(days=1)
    return (prev_end - timedelta(days=length - 1)).isoformat(), prev_end.isoformat()


def _service():
    from googleapiclient.discovery import build

    return build("searchconsole", "v1", credentials=get_credentials(), cache_discovery=False)


def list_properties() -> list[dict]:
    resp = _service().sites().list().execute()
    return resp.get("siteEntry", [])


def query(
    site: str,
    start: str,
    end: str,
    dimensions: list[str],
    limit: int = MAX_ROWS,
    search_type: str = "web",
) -> list[dict]:
    """Haal rijen op, met paginering tot `limit`."""
    svc = _service()
    rows: list[dict] = []
    start_row = 0
    while len(rows) < limit:
        body = {
            "startDate": start,
            "endDate": end,
            "dimensions": dimensions,
            "type": search_type,
            "rowLimit": min(MAX_ROWS, limit - len(rows)),
            "startRow": start_row,
            "dataState": "final",
        }
        resp = svc.searchanalytics().query(siteUrl=site, body=body).execute()
        batch = resp.get("rows", [])
        if not batch:
            break
        for r in batch:
            row = dict(zip(dimensions, r.get("keys", [])))
            row.update(
                clicks=r["clicks"],
                impressions=r["impressions"],
                ctr=round(r["ctr"], 4),
                position=round(r["position"], 1),
            )
            rows.append(row)
        if len(batch) < body["rowLimit"]:
            break
        start_row += len(batch)
    return rows


def compare(current: list[dict], previous: list[dict], key_dims: list[str]) -> list[dict]:
    """Voeg twee perioden samen per sleutel en bereken verschillen."""
    def key(r):
        return tuple(r.get(d) for d in key_dims)

    prev = {key(r): r for r in previous}
    out = []
    seen = set()
    for r in current:
        k = key(r)
        seen.add(k)
        p = prev.get(k, {})
        out.append(_merge(r, p, key_dims))
    for k, p in prev.items():
        if k not in seen:
            out.append(_merge({d: p.get(d) for d in key_dims}, p, key_dims))
    out.sort(key=lambda r: r["clicks_diff"])
    return out


def _merge(cur: dict, prev: dict, key_dims: list[str]) -> dict:
    row = {d: cur.get(d) for d in key_dims}
    for m in ("clicks", "impressions", "ctr", "position"):
        c, p = cur.get(m), prev.get(m)
        row[m] = c if c is not None else 0
        row[f"{m}_prev"] = p if p is not None else 0
    row["clicks_diff"] = row["clicks"] - row["clicks_prev"]
    row["impressions_diff"] = row["impressions"] - row["impressions_prev"]
    if cur.get("position") is not None and prev.get("position") is not None:
        row["position_diff"] = round(cur["position"] - prev["position"], 1)
    else:
        row["position_diff"] = ""
    return row
