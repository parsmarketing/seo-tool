# Google koppelen (Search Console, GA4, PageSpeed)

Eenmalig, ongeveer 15 minuten. Daarna werkt het voor alle klanten.

## Optie A: service account (aanbevolen)
Eén technisch account dat je aan elke klant-property toevoegt. Geen inlogscherm, werkt ook in geplande runs.

1. Ga naar [console.cloud.google.com](https://console.cloud.google.com) en maak een project, bijv. `seo-tool`.
2. **API's inschakelen** (APIs & Services → Library):
   - *Google Search Console API*
   - *Google Analytics Data API*
   - *PageSpeed Insights API*
3. **Service account maken**: IAM & Admin → Service Accounts → Create. Rollen zijn niet nodig.
4. Open het account → Keys → Add key → JSON. Sla het bestand op als `credentials/service-account.json` in deze repo (de map staat in `.gitignore`).
5. Kopieer het e-mailadres van het service account (eindigt op `iam.gserviceaccount.com`).
6. **Per klant toegang geven**:
   - Search Console → Instellingen → Gebruikers en rechten → Gebruiker toevoegen → het service-account-adres, recht *Beperkt*.
   - GA4 → Beheer → Toegangsbeheer property → + → het adres, rol *Kijker*.
7. In `.env`: `GOOGLE_APPLICATION_CREDENTIALS=credentials/service-account.json`.
8. Test: `.venv/bin/seo gsc-properties` toont alle properties waar het account bij kan.

> Lukt stap 4 niet omdat je organisatie sleutels blokkeert? Gebruik optie B.

## Optie B: inloggen als jezelf (OAuth)
Handig als al je klanten-properties al onder jouw Google-account hangen.

1. Stap 1 en 2 hierboven.
2. APIs & Services → OAuth consent screen → *External*, voeg jezelf toe als testgebruiker.
3. Credentials → Create credentials → OAuth client ID → *Desktop app*. Download de JSON als `credentials/client_secret.json`.
4. Laat `GOOGLE_APPLICATION_CREDENTIALS` in `.env` leeg.
5. Draai `.venv/bin/seo gsc-properties`. Er opent een browser om in te loggen; het token wordt bewaard in `credentials/token.json`.

## PageSpeed-sleutel
Zonder sleutel loop je snel tegen een limiet aan. Credentials → Create credentials → API key, beperk hem tot de *PageSpeed Insights API* en zet hem in `.env` als `PAGESPEED_API_KEY`.

## GA4 property-ID vinden
GA4 → Beheer → Property-instellingen → *Property-ID* (alleen cijfers). Zet het in `clients/<slug>/client.toml`.
