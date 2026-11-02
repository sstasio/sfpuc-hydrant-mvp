# Hydrant MVP kit (project files snapshot)

This folder is a copy of the `hydrant-mvp/` folder from the Inspections & Surveys project files, committed on 2026-11-02 so everything lives in one place. Folder structure is unchanged.

> **The guide in [`docs/`](../docs/) is still the source of truth.** The Markdown files here are older drafts from before 2026-10-20. The scripts, data and spreadsheets the guide links to are in [`docs/kit/`](../docs/kit/), and several of those are newer than the copies here. Use this folder as an archive, not for setup.

## Contents

| Path | What it is |
| --- | --- |
| `BUILD-GUIDE.md`, `VIEWS-AND-WEBMAP.md`, `FIELD-MAPS-POPUPS.md`, `DOWNLOADS.md` | Early drafts of the setup guide (superseded by `docs/`) |
| `README-MOVED.md` | Note saying the guide moved to this repo |
| `hydrant-inspection-schema-draft.md` | First draft of the hydrant and inspection schema |
| `field-maps-arcade.md` | Early Arcade expressions for Field Maps pop-ups |
| `build_hydrant_gdb.py` | arcpy script that builds the hydrant geodatabase (schema source) |
| `build_xlsform.py` | Builds the first Survey123 XLSForm |
| `load_demo_inspections.py` | Loads `data/demo_inspections.csv` as demo records |
| `hydrant-mvp.zip` | Download bundle of the kit as of 2026-10-20 |
| `data/` | Sample hydrants, inspector list, demo inspections (CSV) |
| `survey123/` | `HydrantInspection.xlsx` (first generated form) and `Hydrant_Inspections.xlsx` (merged Connect form) |
| `pilot/` | Staff pilot script, answer key, scorecard workbook and the scripts that build and check it |
| `site/build_artifact.py`, `site/tpl.html` | Builds the single-page preview artifact from this repo |
| `site/sfpuc-hydrant-mvp.bundle`, `site/sfpuc-hydrant-mvp-source.zip` | Backups of this repo itself (git bundle and source zip, 2026-10-20) |
| `sffd-issues-noted-fy2223.txt` | Source data: text of the SFFD FY 2022-23 "Items Needing Attention" report |
