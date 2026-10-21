---
name: content-brief
description: Maak een SEO-contentbrief en artikeloutline voor één zoekwoord of onderwerp van een klant (guide SP19-SP20). Gebruik bij "brief", "contentbrief", "outline", "artikel schrijven over".
---

# Contentbrief en outline (SP19-SP20)

## Input
- **Verplicht:** klant, doelzoekwoord of onderwerp.
- **Optioneel:** persona, doel/funnelfase, concurrent-URL's die goed ranken, gewenste lengte, stijlgids.

## Data ophalen
1. `profiel.md` voor doelgroep, toon en USP's.
2. `.venv/bin/seo gsc --klant <slug> --dagen 90 --dimensies query,page --stdout` en filter op termen rond het onderwerp: bestaat er al een pagina die erop rankt? (risico op kannibalisatie)
3. `.venv/bin/seo suggest --klant <slug> "<zoekwoord>"` voor vragen en varianten.
4. Concurrent-URL's die de gebruiker geeft: `.venv/bin/seo pagina <url> --stdout` voor hun koppenstructuur en lengte. Zonder URL's: zeg dat de SERP-analyse ontbreekt.
5. Interne links: kies alleen uit URL's die in GSC-data of `interne_links_lijst` van de eigen site voorkomen.

## Output (sla op als `rapporten/<datum>-brief-<onderwerp>.md`)
1. **Werktitels** (3 opties).
2. **Zoekwoord en intentie**: hoofdzoekwoord, varianten, intentie, funnelfase. Bestaande pagina in GSC? Zo ja: advies om die te verbeteren in plaats van een nieuwe te maken.
3. **Doelgroep** in 3 regels.
4. **Structuur**: H1, H2/H3 genest, met per kop één regel wat erin moet. Geef aan waar het zoekwoord en varianten horen. Markeer koppen die bewijs nodig hebben dat nog niet is aangeleverd met *[bron nodig]*.
5. **Entiteiten en subonderwerpen** die gedekt moeten worden.
6. **Vragen om te beantwoorden** (uit Autocomplete; label: geen volume).
7. **Interne links**: van en naar welke bestaande URL's, met ankertekst.
8. **Lengte**: richtlijn op basis van concurrenten als die zijn aangeleverd, anders "Onvoldoende bewijs".
9. **Meta title (≤60) en description (≤155)**, met tekenaantal.
10. **Bewijsgaten**: wat ontbreekt en welke input het oplost.
11. Controle door een redacteur voordat de schrijver begint.

Geen statistieken, rankings of concurrentprestaties die niet zijn aangeleverd. Log in `logboek.md`.
