---
name: maandrapport
description: Schrijf een SEO-maandrapport voor een klant op basis van Search Console, GA4 en PageSpeed, gericht op de KPI's uit het klantprofiel (guide SP40, rapportage). Gebruik bij "maandrapport", "rapportage", "rapport voor de klant".
---

# Maandrapport (SP40)

## Input
- **Verplicht:** klant. Maand (standaard de vorige kalendermaand).
- **Optioneel:** ontvanger (directie, marketing), extra context van de gebruiker.

## Data ophalen
Bepaal start en eind van de maand (`--start JJJJ-MM-01 --eind JJJJ-MM-<laatste>`), dan:
1. `.venv/bin/seo gsc --klant <slug> --start ... --eind ... --dimensies query --vergelijk`
2. `.venv/bin/seo gsc --klant <slug> --start ... --eind ... --dimensies page --vergelijk`
3. `.venv/bin/seo ga4 --klant <slug> --start ... --eind ...` (als `ga4_property_id` is ingevuld)
4. `.venv/bin/seo psi --klant <slug>` (homepage, mobiel)
5. `logboek.md`: wat is er deze maand gedaan?
Let op: `--vergelijk` vergelijkt met de periode van dezelfde lengte direct ervoor. Een jaar-op-jaar-vergelijking vraagt een tweede run met de data van vorig jaar.

## Rapport (sla op als `rapporten/<JJJJ-MM>-maandrapport.md`)
Schrijf voor de ontvanger, in de merktoon van de klant, zonder jargon.
1. **In één oogopslag**: 3-5 bullets met de belangrijkste ontwikkeling en wat het betekent.
2. **KPI's**: tabel met de KPI's uit `profiel.md` (nu, vorige periode, verschil). Een KPI zonder bron: "Onvoldoende bewijs".
3. **Zoekprestaties**: klikken, vertoningen, CTR, positie; branded vs. non-branded.
4. **Pagina's**: top 5 stijgers en dalers, met mogelijke verklaring als *hypothese*.
5. **Zoektermen**: nieuwe en gegroeide termen; kansen (positie 4-20).
6. **Conversies uit organisch** (GA4), als beschikbaar.
7. **Techniek**: Core Web Vitals-oordeel.
8. **Wat we deden** (uit het logboek) en **plan voor volgende maand** (3-5 acties met reden).
9. Bronnen en perioden.

Geen voorspellingen in cijfers. Log in `logboek.md`.
