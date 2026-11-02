# Hydrant inspection MVP: downloads

Everything for the hydrant inspection MVP, in build order. Grab **hydrant-mvp.zip** for the whole kit, or pick single files below. Target is ArcGIS Enterprise 11.5; start with the build guide.

Updated 2026-10-20.

## Whole kit

| File | What it is |
|---|---|
| [hydrant-mvp.zip](hydrant-mvp.zip) | Every file below in one download (folder layout kept) |

## Start here

| File | What it is |
|---|---|
| [BUILD-GUIDE.md](BUILD-GUIDE.md) | Step-by-step setup: data, Field Maps, Survey123, pilot prep |

## Step 1: Build and publish the data

| File | What it is |
|---|---|
| [build_hydrant_gdb.py](build_hydrant_gdb.py) | Builds `HydrantInspections.gdb` (hydrants, inspection table, relationship, domains). Run it from a Pro notebook with `%run` or from the Python Command Prompt with `propy` (see build guide) |
| [data/sample_hydrants.csv](data/sample_hydrants.csv) | 21 sample E01 hydrants. Coordinates are estimated, not surveyed |
| [data/inspectors.csv](data/inspectors.csv) | Engine companies and inspector names for the Inspector pick lists |

## Step 1b: Views and web map

| File | What it is |
|---|---|
| [VIEWS-AND-WEBMAP.md](VIEWS-AND-WEBMAP.md) | Lock down the source, create the field and public views, build the web map, test with a crew account |

## Step 2: Field Maps app

| File | What it is |
|---|---|
| [FIELD-MAPS-POPUPS.md](FIELD-MAPS-POPUPS.md) | Hydrant and inspection pop-ups: elements, fields, labels and Arcade |
| [field-maps-arcade.md](field-maps-arcade.md) | Arcade for form calculations, conditional visibility, and the pop-up's Survey123 link |

## Step 3: Survey123 app

| File | What it is |
|---|---|
| [survey123/HydrantInspection.xlsx](survey123/HydrantInspection.xlsx) | XLSForm, ready to open in Survey123 Connect |
| [build_xlsform.py](build_xlsform.py) | Regenerates the XLSForm from the schema if fields change (needs `openpyxl`) |

## Step 4: Staff pilot

| File | What it is |
|---|---|
| [pilot/PILOT-SCRIPT.md](pilot/PILOT-SCRIPT.md) | Pilot guide: roles, setup, session script and task cards |
| [pilot/pilot-scorecard.xlsx](pilot/pilot-scorecard.xlsx) | Observer log, tester ratings, data check and team scoring, totaled on the Summary sheet |
| [pilot/answer_key.csv](pilot/answer_key.csv) | Correct values for every task card |
| [pilot/check_pilot_records.py](pilot/check_pilot_records.py) | Checks an export of the inspections table against the answer key and fills in the data check |
| [pilot/build_scorecard.py](pilot/build_scorecard.py) | Rebuilds the scorecard from the answer key if the tasks change |

## Reference

| File | What it is |
|---|---|
| [hydrant-inspection-schema-draft.md](hydrant-inspection-schema-draft.md) | Field list with the reasoning behind each field |
| [sffd-issues-noted-fy2223.txt](sffd-issues-noted-fy2223.txt) | SFFD FY22-23 "Items Needing Attention" report (source for sample hydrants and inspectors). Not in the zip |
