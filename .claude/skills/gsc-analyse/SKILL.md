---
name: gsc-analyse
description: Analyseer Search Console-data van een klant op patronen en kansen, of diagnoseer een verkeersdaling met gerangschikte hypotheses (guide SP38-SP39). Gebruik bij "Search Console", "GSC", "verkeer gedaald", "waarom minder klikken", "quick wins".
---

# Search Console-analyse en verkeersdaling (SP38-SP39)

## Input
- **Verplicht:** klant. Periode (standaard laatste 28 dagen vs. de 28 dagen daarvoor).
- **Optioneel:** specifieke vraag, datum en omvang van een daling, bekende wijzigingen (migratie, redesign, Google-update).

## Data ophalen
1. `.venv/bin/seo gsc --klant <slug> --dimensies query --vergelijk`
2. `.venv/bin/seo gsc --klant <slug> --dimensies page --vergelijk`
3. `.venv/bin/seo gsc --klant <slug> --dimensies date --dagen 90` voor de trendlijn.
4. Bij een daling ook: `--dimensies device --vergelijk` en `--dimensies country --vergelijk`.
5. Optioneel GA4: `.venv/bin/seo ga4 --klant <slug>` om te zien of de daling conversies raakt.
6. Kijk in `logboek.md` naar eerdere wijzigingen rond de datum van de daling.

## Modus A: patronen en kansen (SP38)
1. **Kernpatronen**: totaal klikken/vertoningen/CTR/positie nu vs. vorige periode; branded vs. non-branded (merknaam-varianten uit `profiel.md`).
2. **Kansen per zoekterm**: positie 4-20 met veel vertoningen (striking distance); hoge vertoningen met lage CTR (titel/meta verbeteren).
3. **Kansen per pagina**: grootste stijgers en dalers; pagina's die op dezelfde term concurreren (kannibalisatie: één query, meerdere pagina's).
4. **Beperkingen van de dataset**: anonieme zoektermen ontbreken, rijlimiet, periode.

## Modus B: verkeersdaling (SP39)
Een **gerangschikte lijst van hypotheses**, geen diagnose. Per hypothese:
- wat in de data erop wijst (met cijfers en bestand),
- wat nodig is om het te bevestigen of uit te sluiten,
- label *past bij de data* of *speculatief*.
Denk aan: seizoen, Google-update, technische fout (noindex, robots, redirects; check met `seo pagina` en `seo site`), verlies van één groot zoekwoord, device- of landverschuiving, SERP-wijziging (AI Overviews, alleen als hypothese).

## Output
Sla op als `rapporten/<datum>-gsc-analyse.md`. Elk cijfer met bron en periode. Sluit af met: "Controleer bevindingen in de live Search Console-property voordat je actie neemt." Log in `logboek.md`.
