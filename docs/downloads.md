# Downloads

Everything you load into ArcGIS, in build order. Target is ArcGIS Enterprise 11.5.

## Whole kit

| File | What it is |
|---|---|
| [hydrant-mvp.zip](kit/hydrant-mvp.zip) | Every file below in one download, folder layout kept. Unzip to `C:\temp\hydrant-mvp` |

## Step 1: Build and publish the data

| File | What it is |
|---|---|
| [build_hydrant_gdb.py](kit/build_hydrant_gdb.py) | Builds `HydrantInspections.gdb` (hydrants, inspection table, relationship, domains). See [step 1](setup/01-build-data.md) for how to run it |
| [data/sample_hydrants.csv](kit/data/sample_hydrants.csv) | 21 sample E01 hydrants. Coordinates are estimated, not surveyed |
| [data/inspectors.csv](kit/data/inspectors.csv) | Engine companies and inspector names for the Inspector pick lists. Needs cleanup before the pilot ([step 8](setup/08-pilot.md#before-the-pilot-pilot-lead-and-portal-admin)) |

## Step 6: Survey123

| File | What it is |
|---|---|
| [survey123/HydrantInspection.xlsx](kit/survey123/HydrantInspection.xlsx) | XLSForm, ready to open in Survey123 Connect |
| [build_xlsform.py](kit/build_xlsform.py) | Regenerates the XLSForm from the schema if fields change (needs `openpyxl`) |

## Step 8: Staff pilot

| File | What it is |
|---|---|
| [pilot/pilot-scorecard.xlsx](kit/pilot/pilot-scorecard.xlsx) | Observer log, tester ratings, data check and team scoring, totaled on the Summary sheet |
| [pilot/answer_key.csv](kit/pilot/answer_key.csv) | Correct values for every task card |
| [pilot/check_pilot_records.py](kit/pilot/check_pilot_records.py) | Checks an export of the inspections table against the answer key and fills in the data check |
| [pilot/build_scorecard.py](kit/pilot/build_scorecard.py) | Rebuilds the scorecard from the answer key if the tasks change |

The Arcade for steps 4 to 6 is on those pages, with a copy button on each block.
