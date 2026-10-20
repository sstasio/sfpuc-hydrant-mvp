# Hydrant inspection MVP

Step-by-step setup and reference for the SFPUC hydrant inspection MVP: one hosted layer, two apps (ArcGIS Field Maps and ArcGIS Survey123), a staff pilot to pick between them. Target is ArcGIS Enterprise 11.5.

**[Start here: docs/index.md](docs/index.md)**

## Setup, in order

1. [Build and publish the data](docs/setup/01-build-data.md)
2. [Lock down the source and create views](docs/setup/02-views.md)
3. [Build the web map](docs/setup/03-web-map.md)
4. [Set up pop-ups](docs/setup/04-popups.md)
5. [Build the Field Maps form](docs/setup/05-field-maps-form.md)
6. [Publish the Survey123 form](docs/setup/06-survey123.md)
7. [Test before the pilot](docs/setup/07-test.md)
8. [Run the staff pilot](docs/setup/08-pilot.md)

Reference: [schema](docs/reference/schema.md) · [Field Maps vs Survey123](docs/reference/app-comparison.md) · [pilot task cards](docs/reference/task-cards.md) · [offline basemap](docs/reference/offline-basemap.md) · [Esri 11.5 docs](docs/reference/esri-docs.md) · [troubleshooting](docs/reference/troubleshooting.md) · [downloads](docs/downloads.md)

## Latest changes

- **2026-10-20:** Pop-up and form Arcade now use the portal's lower-case field names, fixing "Some expressions failed to evaluate" in Field Maps: [Troubleshooting](docs/reference/troubleshooting.md#pop-up-says-some-expressions-failed-to-evaluate).
- **2026-10-20:** Fix for Field Maps' "Features with true curves cannot currently be edited" warning: [Troubleshooting](docs/reference/troubleshooting.md#features-with-true-curves-cannot-currently-be-edited), plus a publishing tip in [step 1](docs/setup/01-build-data.md).
- **2026-10-20:** Offline basemap for Field Maps: [Offline basemap](docs/reference/offline-basemap.md).

## Reading it

- **On GitHub:** click through the links above. Every page links to the next step.
- **As a website on your own machine:** `pip install -r requirements.txt`, then `mkdocs serve` and open http://127.0.0.1:8000. Same pages, with a sidebar, search, SFPUC colors and copy buttons on the Arcade.
- **As a hosted website:** the `Publish site` workflow in `.github/workflows/pages.yml` builds it to GitHub Pages, but only when someone runs it by hand. Pages for a private repo needs a paid GitHub plan, and on anything below GitHub Enterprise the site is public. Don't run it until the internal content below is cleared.

## Internal use

This repo holds the portal address, service and view names, SFFD inspector names and SFPUC logos. Keep it private and share it by adding collaborators. Brand source: `sstasio/sfpuc-design-system`.

## Making changes

This repo is the one place to edit the guide. Edit the Markdown under `docs/` and add a line to **Latest changes** on the front page (`docs/index.md`). The files crews and analysts load into ArcGIS are under `docs/kit/`; if you change one, rebuild `docs/kit/hydrant-mvp.zip` so the download matches.
