# SEO-tool

Herbruikbare SEO-werkplek voor meerdere klanten, gebouwd op de prompts, audits en workflows uit
*The Complete Claude SEO Guide 2026* (EfficusAI). De skills in `.claude/skills/` zijn generiek;
alle klantspecifieke data staat in `clients/<slug>/`.

## Structuur
- `.claude/skills/` — één skill per taak. De code tussen haakjes (SP06, SA01, SW01) verwijst naar de guide.
- `clients/<slug>/client.toml` — domein, taal, GSC- en GA4-koppeling, concurrenten.
- `clients/<slug>/profiel.md` — bedrijf, doelgroep, doelen, zoekwoorden.
- `clients/<slug>/logboek.md` — wat er is gedaan, nieuwste bovenaan.
- `clients/<slug>/rapporten/` — opgeleverde briefs, audits en rapporten (in git).
- `clients/<slug>/data/` — ruwe exports van de `seo`-commando's (niet in git).
- `seo_tool/` — Python-CLI `seo` die data ophaalt. Draai met `.venv/bin/seo` of `uv run seo`.

## Werkwijze voor elke skill
1. **Klant bepalen.** Vraag welke klant als dat niet duidelijk is (`seo klanten`). Lees `client.toml`, `profiel.md`
   en de laatste regels van `logboek.md` voordat je iets anders doet.
2. **Data ophalen in plaats van vragen.** Gebruik eerst de `seo`-commando's. Vraag de gebruiker alleen om wat
   daarna nog ontbreekt, in één keer.
3. **Nooit cijfers verzinnen.** Geen zoekvolumes, moeilijkheid, posities, CTR's, verkeer of concurrentiedata
   die niet uit een bron komen. Autocomplete-suggesties hebben géén volume: zeg dat erbij.
4. **"Onvoldoende bewijs".** Kan een onderdeel niet worden onderbouwd, schrijf dan "Onvoldoende bewijs" en noem
   welke input het gat zou vullen.
5. **Bron per bewering.** Bij elk cijfer: uit welk bestand of welke API het komt en over welke periode.
6. **Hypothese is geen diagnose.** Oorzaken van dalingen, AI-zichtbaarheid en ranking-effecten zijn hypotheses.
7. **Menselijke controle.** Sluit af met wat een mens moet controleren voordat iets live gaat (schema, redirects,
   migraties, juridische claims, alles wat live verkeer raakt).
8. **Opslaan en loggen.** Sla de oplevering op in `clients/<slug>/rapporten/JJJJ-MM-DD-<onderwerp>.md` en voeg
   een regel toe aan `logboek.md`.

## Taal
Schrijf in het Nederlands, tenzij de gebruiker of `client.toml` (`taal`) iets anders aangeeft.
Gebruik de merktoon uit `profiel.md` (je/u).

## Geheimen
API-sleutels staan in `.env` en `credentials/`, nooit in klantbestanden of rapporten.
