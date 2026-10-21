---
name: nieuwe-klant
description: Maak een nieuwe klant aan in clients/ (client.toml, profiel.md, logboek.md) via een kort interview en een eerste site-scan. Gebruik bij "nieuwe klant", "klant toevoegen" of als een skill een klant nodig heeft die nog niet bestaat.
---

# Nieuwe klant aanmaken

## Stappen
1. Vraag in één bericht: klantnaam, domein, taal/land (standaard nl/nl), en of je toegang hebt tot hun Search Console en GA4.
2. Bepaal een slug (kleine letters, koppeltekens, bijv. `bakkerij-jansen`) en kopieer `clients/_template/` naar `clients/<slug>/`.
3. Haal zelf op wat kan, zonder het te vragen:
   - `.venv/bin/seo site --url https://<domein> --stdout` → robots.txt en sitemap.
   - `.venv/bin/seo pagina https://<domein> --stdout` → titel, meta, koppen, taal, schema, tekst van de homepage.
   - `.venv/bin/seo gsc-properties` → zoek de juiste property (`sc-domain:` heeft de voorkeur) en zet die in `client.toml`.
4. Vul `profiel.md` voor zover de homepage-tekst het onderbouwt (aanbod, werkgebied, toon). Markeer alles wat je afleidt met *(afgeleid van homepage, bevestigen)*.
5. Vraag daarna in één bericht alleen wat ontbreekt: doelen/KPI's, doelgroep, concurrenten, kernzoekwoorden, merknaam-varianten, GA4 property-ID, belangrijke pagina's.
6. Verwerk de antwoorden, zet in `logboek.md`: `| <datum> | Klant aangemaakt | profiel.md | ... |`.
7. Sluit af met een samenvatting en stel als volgende stap `maandcheck` of `zoekwoordonderzoek` voor.

## Regels
- Zet nooit API-sleutels of wachtwoorden in de klantmap.
- Verzin geen doelen of concurrenten; leeg laten is beter.
