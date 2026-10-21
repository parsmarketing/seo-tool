"""Commandoregel: `seo <commando>`. Elke opdracht schrijft naar clients/<klant>/data/ als --klant is opgegeven."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys

from dotenv import load_dotenv

from .clients import ROOT, Client, list_clients, load_client


def _write(rows_or_obj, client: Client | None, kind: str, to_stdout: bool) -> None:
    is_table = isinstance(rows_or_obj, list) and rows_or_obj and isinstance(rows_or_obj[0], dict)
    if is_table:
        buf = io.StringIO()
        fields = list(dict.fromkeys(k for r in rows_or_obj for k in r))
        w = csv.DictWriter(buf, fieldnames=fields)
        w.writeheader()
        w.writerows(rows_or_obj)
        text, ext = buf.getvalue(), "csv"
    else:
        text, ext = json.dumps(rows_or_obj, ensure_ascii=False, indent=2), "json"

    if to_stdout or client is None:
        sys.stdout.write(text if text.endswith("\n") else text + "\n")
        return
    path = client.data_path(kind, ext)
    path.write_text(text, encoding="utf-8")
    count = f"{len(rows_or_obj)} rijen" if isinstance(rows_or_obj, list) else "1 object"
    print(f"Opgeslagen: {path.relative_to(ROOT)} ({count})")


def _client(args) -> Client | None:
    return load_client(args.klant) if getattr(args, "klant", None) else None


def _dates(args):
    from . import gsc

    if args.start and args.eind:
        return args.start, args.eind
    return gsc.default_range(args.dagen)


def cmd_klanten(args):
    for slug in list_clients():
        c = load_client(slug)
        print(f"{slug:20} {c.name:30} {c.domain}")


def cmd_gsc_properties(args):
    from . import gsc

    for p in gsc.list_properties():
        print(f"{p['siteUrl']:50} {p['permissionLevel']}")


def cmd_gsc(args):
    from . import gsc

    client = _client(args)
    site = args.property or (client and client.gsc_property)
    if not site:
        raise SystemExit("Geen GSC-property. Gebruik --property of vul gsc_property in client.toml.")
    dims = [d.strip() for d in args.dimensies.split(",")]
    start, end = _dates(args)
    rows = gsc.query(site, start, end, dims, limit=args.limit)
    kind = f"gsc-{'-'.join(dims)}-{start}_{end}"
    if args.vergelijk:
        ps, pe = gsc.previous_range(start, end)
        prev = gsc.query(site, ps, pe, dims, limit=args.limit)
        rows = gsc.compare(rows, prev, dims)
        kind = f"gsc-vergelijk-{'-'.join(dims)}-{start}_{end}-vs-{ps}_{pe}"
    _write(rows, client, kind, args.stdout)


def cmd_ga4(args):
    from . import ga4

    client = _client(args)
    prop = args.property or (client and client.ga4_property_id)
    if not prop:
        raise SystemExit("Geen GA4-property. Gebruik --property of vul ga4_property_id in client.toml.")
    start, end = _dates(args)
    rows = ga4.landing_pages(prop, start, end, limit=args.limit, organic_only=not args.alle_kanalen)
    _write(rows, client, f"ga4-landingspaginas-{start}_{end}", args.stdout)


def cmd_psi(args):
    from . import pagespeed

    client = _client(args)
    urls = args.url or ([client.base_url] + client.key_pages if client else [])
    if not urls:
        raise SystemExit("Geef --url of --klant op.")
    results = []
    for u in urls:
        if not u.startswith("http") and client:
            u = client.base_url + "/" + u.lstrip("/")
        for strat in args.strategie.split(","):
            results.append(pagespeed.run(u, strat.strip()))
    _write(results if len(results) > 1 else results[0], client, "pagespeed", args.stdout)


def cmd_suggest(args):
    from . import suggest

    client = _client(args)
    lang = args.taal or (client.language if client else "nl")
    country = args.land or (client.country if client else "nl")
    rows = []
    for seed in args.seeds:
        rows += suggest.expand(seed, lang, country, deep=not args.snel)
    _write(rows, client, "autocomplete", args.stdout)


def cmd_pagina(args):
    from . import page

    client = _client(args)
    url = args.url
    if not url.startswith("http") and client:
        url = client.base_url + "/" + url.lstrip("/")
    result = page.analyse(url)
    slug = url.split("://", 1)[-1].strip("/").replace("/", "_")[:80] or "home"
    _write(result, client, f"pagina-{slug}", args.stdout)


def cmd_site(args):
    from . import page

    client = _client(args)
    base = args.url or (client.base_url if client else None)
    if not base:
        raise SystemExit("Geef --url of --klant op.")
    _write(page.site_checks(base), client, "site-robots-sitemap", args.stdout)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="seo", description="Data ophalen voor de SEO-skills.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, dates=False):
        sp.add_argument("--klant", help="slug van de klant in clients/")
        sp.add_argument("--stdout", action="store_true", help="naar scherm in plaats van bestand")
        if dates:
            sp.add_argument("--dagen", type=int, default=28)
            sp.add_argument("--start", help="YYYY-MM-DD")
            sp.add_argument("--eind", help="YYYY-MM-DD")
            sp.add_argument("--limit", type=int, default=5000)

    sp = sub.add_parser("klanten", help="toon alle klanten")
    sp.set_defaults(func=cmd_klanten)

    sp = sub.add_parser("gsc-properties", help="toon GSC-properties waar je toegang toe hebt")
    sp.set_defaults(func=cmd_gsc_properties)

    sp = sub.add_parser("gsc", help="Search Console-prestaties")
    common(sp, dates=True)
    sp.add_argument("--property", help="bijv. sc-domain:voorbeeld.nl")
    sp.add_argument("--dimensies", default="query,page", help="query,page,date,device,country")
    sp.add_argument("--vergelijk", action="store_true", help="vergelijk met de vorige periode")
    sp.set_defaults(func=cmd_gsc)

    sp = sub.add_parser("ga4", help="GA4 organische landingspagina's")
    common(sp, dates=True)
    sp.add_argument("--property", help="GA4 property-ID (alleen cijfers)")
    sp.add_argument("--alle-kanalen", action="store_true")
    sp.set_defaults(func=cmd_ga4)

    sp = sub.add_parser("psi", help="PageSpeed Insights / Core Web Vitals")
    common(sp)
    sp.add_argument("--url", action="append", help="mag vaker; standaard home + belangrijke pagina's")
    sp.add_argument("--strategie", default="mobile", help="mobile,desktop")
    sp.set_defaults(func=cmd_psi)

    sp = sub.add_parser("suggest", help="Google Autocomplete-ideeën")
    common(sp)
    sp.add_argument("seeds", nargs="+")
    sp.add_argument("--taal")
    sp.add_argument("--land")
    sp.add_argument("--snel", action="store_true", help="alleen de seed, geen a-z en vraagwoorden")
    sp.set_defaults(func=cmd_suggest)

    sp = sub.add_parser("pagina", help="on-page analyse van één URL")
    common(sp)
    sp.add_argument("url", help="volledige URL of pad (met --klant)")
    sp.set_defaults(func=cmd_pagina)

    sp = sub.add_parser("site", help="robots.txt en sitemap")
    common(sp)
    sp.add_argument("--url")
    sp.set_defaults(func=cmd_site)
    return p


def main(argv: list[str] | None = None) -> None:
    load_dotenv(ROOT / ".env")
    args = build_parser().parse_args(argv)
    import requests

    try:
        args.func(args)
    except requests.RequestException as e:
        raise SystemExit(f"Netwerkfout: {e}")


if __name__ == "__main__":
    main()
