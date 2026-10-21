# SEO-tool

Een SEO-werkplek in Claude Code voor meerdere klanten. De werkwijze komt uit
*The Complete Claude SEO Guide 2026* (EfficusAI): elke prompt werkt alleen met aangeleverde data en verzint geen cijfers.
Deze tool levert die data automatisch aan uit Search Console, GA4, PageSpeed, Google Autocomplete en de pagina zelf.

## Installeren
```bash
git clone https://github.com/parsmarketing/seo-tool.git && cd seo-tool
uv venv && uv pip install -e .        # of: python -m venv .venv && .venv/bin/pip install -e .
cp .env.example .env
```
Koppel daarna Google: zie [docs/google-koppelen.md](docs/google-koppelen.md).

## Gebruiken
Open de map in Claude Code en vraag het gewoon, bijvoorbeeld:

| Vraag | Skill |
|---|---|
| "Voeg klant Bakkerij Jansen toe, domein bakkerijjansen.nl" | `nieuwe-klant` |
| "Doe zoekwoordonderzoek voor jansen rond 'zuurdesembrood'" | `zoekwoordonderzoek` (SP06-SP09) |
| "Maak een brief voor 'glutenvrij brood bestellen'" | `content-brief` (SP19-SP20) |
| "Optimaliseer jansen.nl/taarten" | `onpage-optimalisatie` (SP23-SP25) |
| "Waarom heeft jansen minder klikken dan vorige maand?" | `gsc-analyse` (SP38-SP39) |
| "Technische audit voor jansen" | `technische-audit` (SP31-SP33) |
| "Maandrapport september voor jansen" | `maandrapport` (SP40) |
| "Doe de maandcheck voor al mijn klanten" | `maandcheck` (workflow) |

Rapporten komen in `clients/<klant>/rapporten/`, ruwe data in `clients/<klant>/data/` (niet in git).

## Data-commando's
De skills roepen deze zelf aan; je kunt ze ook direct gebruiken.
```bash
seo klanten
seo gsc-properties
seo gsc --klant jansen --dimensies query,page --dagen 28 --vergelijk
seo ga4 --klant jansen --dagen 28
seo psi --klant jansen --strategie mobile,desktop
seo suggest --klant jansen "zuurdesembrood" "taart bestellen"
seo pagina --klant jansen /taarten
seo site --klant jansen
```

## Klantdata
Per klant een map `clients/<slug>/` met `client.toml` (koppelingen), `profiel.md` (context) en `logboek.md`.
Start vanuit `clients/_template/` of laat de skill `nieuwe-klant` het doen. De skills zelf bevatten geen klantdata.

## Bewust niet (nog)
- **Zoekvolumes en moeilijkheid**: vereisen een betaalde bron. DataForSEO kan later als extra commando.
- **Volledige crawl**: lever een Screaming Frog-export aan; de tool checkt zelf alleen opgegeven pagina's.
- **AI Overviews / AI Mode-zichtbaarheid**: niet meetbaar zonder monitoringtool, dus alleen als hypothese.

## Tests
```bash
uv pip install -e '.[dev]' && .venv/bin/pytest
```
