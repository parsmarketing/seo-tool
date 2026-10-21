---
name: maandcheck
description: Workflow voor de maandelijkse controle van één klant of alle klanten: data ophalen, signalen zoeken, technische check, maandrapport schrijven, met controlepunten voor de gebruiker. Gebruik bij "maandcheck", "doe de maandelijkse ronde", "check al mijn klanten".
---

# Maandcheck (workflow)

Ketting van de skills `gsc-analyse`, `technische-audit` (licht) en `maandrapport`, met momenten waarop de gebruiker beslist.

## Stappen
1. **Klanten kiezen.** Eén klant, of `seo klanten` voor alle klanten. Bij meerdere: werk ze één voor één af en houd per klant een korte status bij.
2. **Data ophalen** voor de vorige kalendermaand (zie `maandrapport` voor de commando's) plus `seo site` en `seo pagina` voor de belangrijke pagina's.
3. **Signalen** (uit `gsc-analyse` modus A): daling van >20% klikken op site- of paginaniveau, belangrijke pagina zonder vertoningen, nieuwe kannibalisatie, CWV-oordeel verslechterd, noindex/statusfout op een belangrijke pagina.
4. **Controlepunt 1**: toon per klant de signalen in maximaal 5 regels en vraag: diep ingaan op een daling (`gsc-analyse` modus B), of door naar het rapport?
5. **Rapport** met de skill `maandrapport`.
6. **Controlepunt 2**: laat het concept zien en verwerk feedback voordat het naar de klant gaat. Verstuur zelf niets.
7. **Afsluiten**: logregel per klant en een overzicht van alle klanten: `Klant | Klikken Δ | Signalen | Rapport`.
