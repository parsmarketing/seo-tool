---
name: technische-audit
description: Technische SEO-audit van een klant: indexeerbaarheid, robots/sitemap, redirects, canonicals, structured data en Core Web Vitals, uitgelegd voor niet-technische lezers (guide SP31-SP33 en de technische audit uit hub 15). Gebruik bij "technische audit", "site snelheid", "Core Web Vitals", "schema", "waarom wordt dit niet geïndexeerd".
---

# Technische audit (SP31-SP33)

## Input
- **Verplicht:** klant.
- **Optioneel:** specifieke URL's, een crawl-export (bijv. Screaming Frog CSV) die de gebruiker aanlevert, CMS.

## Data ophalen
1. `.venv/bin/seo site --klant <slug>` → robots.txt en sitemaps.
2. `.venv/bin/seo pagina --klant <slug> /` en voor elke URL in `pagina.belangrijk` uit `client.toml`.
3. `.venv/bin/seo psi --klant <slug> --strategie mobile,desktop` → Core Web Vitals (velddata uit CrUX) en Lighthouse.
4. `.venv/bin/seo gsc --klant <slug> --dimensies page --dagen 28 --stdout` → pagina's met vertoningen (controleer of de belangrijke pagina's erin staan).
5. Een crawl-export, als die is aangeleverd. Zonder crawl: zeg dat de audit alleen de gecontroleerde URL's dekt, niet de hele site.

## Beoordeling
Scoor per onderdeel **In orde / Aandacht / Probleem / Onvoldoende bewijs**:
1. Indexeerbaarheid: statuscode, meta robots, X-Robots-Tag, canonical (naar zichzelf?), robots.txt-blokkades.
2. Sitemap: bereikbaar, aantal URL's, vermeld in robots.txt.
3. Redirects: ketens, http→https, www-varianten.
4. On-page basis: één H1, titel en meta aanwezig, `lang`, hreflang als er meerdere talen zijn.
5. **Structured data (SP32)**: aanwezige types; aanbevolen schema.org-types per paginatype met kern-eigenschappen. Nooit beloven dat schema een rich result oplevert. Reviews/ratings alleen met echte reviewdata.
6. **Core Web Vitals (SP33)**: per metric (LCP, INP, CLS) de p75-waarde en het oordeel uit de data (`goed`, `verbetering nodig`, `slecht`). Leg uit wat elke metric meet. Oorzaken als "vaak veroorzaakt door", niet als diagnose. Geen uitspraken over ranking-effect. Velddata ontbreekt? Zeg dat, en gebruik labdata alleen als indicatie.

## Output (sla op als `rapporten/<datum>-technische-audit.md`)
1. Samenvatting met scoretabel.
2. **Per probleem (SP31)**: uitleg in gewone taal, waarschijnlijke impact (als "doorgaans"), aanpak van de oplossing, gaten.
3. Prioriteitenlijst: impact × moeite.
4. Controle: een developer valideert schema (Rich Results Test), redirects en wijzigingen vóór livegang.

Log in `logboek.md`.
