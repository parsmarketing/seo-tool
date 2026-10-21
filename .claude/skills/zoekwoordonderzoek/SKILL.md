---
name: zoekwoordonderzoek
description: Zoekwoordonderzoek voor een klant (guide SP06-SP09): seeds uitbreiden met Autocomplete en Search Console, long-tail en vragen vinden, clusteren tot een topic map. Gebruik bij "zoekwoorden", "keyword research", "topic cluster" of "waar moeten we over schrijven".
---

# Zoekwoordonderzoek (SP06-SP09)

## Input
- **Verplicht:** klant, en seed-zoekwoorden (neem `Kernzoekwoorden` uit `profiel.md` als de gebruiker er geen geeft).
- **Optioneel:** focus (dienst, product, regio), persona, concurrent-URL's.

## Data ophalen
1. `.venv/bin/seo suggest --klant <slug> "<seed1>" "<seed2>" ...` → Autocomplete-ideeën (a-z en vraagwoorden). Gebruik `--snel` bij meer dan 5 seeds.
2. `.venv/bin/seo gsc --klant <slug> --dagen 90 --dimensies query,page` → zoektermen waarop de site al vertoningen heeft. Dit is de enige bron met echte cijfers.
3. Lees beide CSV's uit `clients/<slug>/data/`.

## Analyse
1. **Uitbreiden (SP06):** combineer seeds, Autocomplete en GSC-zoektermen. Filter onrelevante termen weg (zie `profiel.md`), en scheid merkzoektermen.
2. **Long-tail en vragen (SP07):** groepeer per patroon: vraag, vergelijking, hoe-te, lokaal, prijs. Stel per groep een contentvorm voor.
3. **Kwalificeren (SP08):** per term de zoekintentie (informatief, commercieel, transactioneel, navigerend) en de fase in de klantreis. Markeer intentie als *ingeschat* tenzij SERP-data is aangeleverd.
4. **Topic map (SP09):** clusters met een pijlerpagina en ondersteunende pagina's. Koppel per cluster aan een bestaande URL uit GSC als die er is, anders "nieuw".

## Output
Sla op als `clients/<slug>/rapporten/<datum>-zoekwoordonderzoek.md`:
1. Samenvatting (5 regels): grootste kansen en waarom.
2. **Kansen uit Search Console** (echte data): termen met veel vertoningen en positie 5-20, met klikken, vertoningen, positie en periode.
3. **Topic map**: tabel `Cluster | Pijler (URL of nieuw) | Ondersteunende onderwerpen | Intentie | Bron`.
4. **Long-tail en vragen** per groep, met voorgestelde contentvorm.
5. Beperkingen: Autocomplete-termen zijn **ongescoord** (geen volume of moeilijkheid). Adviseer validatie met een zoekwoordtool (bijv. DataForSEO, later te koppelen).
6. Wat een mens moet controleren.

Voeg een regel toe aan `logboek.md`. Zie `CLAUDE.md` voor de vaste regels.
