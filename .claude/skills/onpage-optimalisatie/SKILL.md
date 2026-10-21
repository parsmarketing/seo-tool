---
name: onpage-optimalisatie
description: Optimaliseer een bestaande pagina van een klant: titel, koppen, meta title/description en dekking van entiteiten en subonderwerpen (guide SP23-SP25), onderbouwd met Search Console-data voor die URL. Gebruik bij "optimaliseer deze pagina", "meta's schrijven", "on-page check".
---

# On-page optimalisatie (SP23-SP25)

## Input
- **Verplicht:** klant, URL (of pad) van de pagina.
- **Optioneel:** doelzoekwoord (anders afleiden uit GSC), lijst entiteiten/subonderwerpen.

## Data ophalen
1. `.venv/bin/seo pagina --klant <slug> <url>` → titel, meta, H1-H3, woorden, schema, tekst.
2. `.venv/bin/seo gsc --klant <slug> --dagen 90 --dimensies query,page --stdout` → filter op deze URL: welke zoektermen, vertoningen, CTR en positie.
3. Kies het doelzoekwoord: opgegeven door de gebruiker, of de term met de meeste vertoningen voor deze URL (zeg welke en waarom).

## Output (sla op als `rapporten/<datum>-onpage-<pad>.md`)
1. **Huidige situatie**: tabel met titel (lengte), meta description (lengte), H1, aantal H2's, woorden, schema-types. Plus de top-10 zoektermen uit GSC voor deze URL met periode.
2. **Titel en koppen (SP23)**: per huidige titel/kop het origineel, 2-3 alternatieven, en per alternatief één regel waarom (duidelijkheid, zoekwoordrelevantie of klikwaarde). Geen voorspelde CTR- of ranking-winst.
3. **Metadata (SP24)**: 3 meta titles (≤60 tekens) en 3 descriptions (≤155 tekens) met tekenaantal. Elke bewering moet in de paginatekst staan; geen verzonnen prijzen, awards of features.
4. **Entiteiten en subonderwerpen (SP25)**: tabel `Entiteit/subonderwerp | Status (gedekt / deels / ontbreekt) | Notitie`. Komt de lijst niet van de gebruiker, label het dan als *hypothese uit algemene kennis*.
   Gebruik GSC-zoektermen die wel vertoningen maar geen dekking in de tekst hebben als onderbouwde gaten.
5. **Overige bevindingen**: afbeeldingen zonder alt, canonical, meta robots, ontbrekend schema.
6. **Prioriteiten**: top 5 acties.
7. Controle: redacteur kiest de definitieve tekst en controleert de weergave in de zoekresultaten.

Log in `logboek.md`.
