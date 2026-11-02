# Hydrant inspection MVP: build guide

One feature service, two apps. Field Maps and Survey123 both write to the same `HydrantInspections` table, so every inspection lands in one place whichever app the crew used.

Target: ArcGIS Enterprise 11.5 (https://gis.sfpuc.org/portal). Everything here was written without access to the portal, so check each step in the 11.5 UI as you go. Notes marked **check** are features I couldn't confirm for 11.5.

## Files

| File | What it is |
|---|---|
| `build_hydrant_gdb.py` | Builds `HydrantInspections.gdb` (hydrant points, inspection table, relationship, domains, attachments, editor tracking). Run in ArcGIS Pro's Python |
| `data/sample_hydrants.csv` | 21 sample hydrants: real E01 serials and spindle pressures from the SFFD report. **Coordinates are estimated, not surveyed**: move the points or swap in a real export |
| `data/inspectors.csv` | Engine company and inspector names from the SFFD FY22-23 report (278 names), used for the Inspector lists |
| `build_xlsform.py` | Regenerates the Survey123 form from the same schema (needs `openpyxl`) |
| `survey123/HydrantInspection.xlsx` | Survey123 XLSForm, ready for Survey123 Connect |
| `field-maps-arcade.md` | Arcade for the Field Maps form and the pop-up's Survey123 link |
| `FIELD-MAPS-POPUPS.md` | Exact hydrant and inspection pop-ups, with Arcade |
| `VIEWS-AND-WEBMAP.md` | Views for crews and the public, and the Field Maps web map built on them |
| `hydrant-inspection-schema-draft.md` | Field list with the reasoning behind each field |

## 1. Build and publish the data

1. Unzip the kit to `C:\temp\hydrant-mvp`, then run the script one of three ways, always with its full path:
   - **ArcGIS Pro notebook** (Insert > New Notebook), in a cell: `%run "C:\temp\hydrant-mvp\build_hydrant_gdb.py" --out C:\temp`. A notebook cell is Python, so typing `propy ...` there gives a SyntaxError.
   - **Python window** (Analysis > Python > Python Window), which doesn't understand `%run`. Paste: `import sys, runpy; sys.argv = [r"C:\temp\hydrant-mvp\build_hydrant_gdb.py", "--out", r"C:\temp"]; runpy.run_path(sys.argv[0], run_name="__main__")`
   - **Python Command Prompt** (Windows Start > ArcGIS > Python Command Prompt): `propy "C:\temp\hydrant-mvp\build_hydrant_gdb.py" --out C:\temp`
   It prints `Built C:\temp\HydrantInspections.gdb with 21 hydrants`. To run it again, first remove the layers from your map and delete the old geodatabase in the Catalog pane.
   To use real hydrants instead, export 20 to 50 points to a CSV with the same columns (`Lat`/`Lon` in WGS84) and add `--hydrants your.csv`.
2. Add `Hydrants` and `HydrantInspections` to a map. Symbolize hydrants simply (water blue `#007DC3` points).
3. **Share > Web Layer**, copying all data to the portal's data store. Under **Configuration > Feature**, turn on **Create, Update, Delete, Sync** (sync is needed for offline). Share it with yourself or the GIS team only; crews get views instead (`VIEWS-AND-WEBMAP.md`).
4. One service with layer 0 = Hydrants and table 1 = HydrantInspections. Note the service URL and item ID.
5. Create the field view (and the public view, if allowed) using `VIEWS-AND-WEBMAP.md` steps 1 to 3.

## 2. Field Maps app

1. Build the web map from the **field view**, not the source, following `VIEWS-AND-WEBMAP.md` step 4. Save it as "Hydrant Inspections MVP" and share it with the MVP test group.
2. **Pop-ups** on Hydrants and HydrantInspections: follow `FIELD-MAPS-POPUPS.md`. Add the Survey123 link once the survey is published (step 3).
3. **Field Maps Designer > Forms > HydrantInspections table**. Build groups that mirror the Survey123 form:

   | Group | Fields | Input |
   |---|---|---|
   | Hydrant | GIS ID, Location, Latitude, Longitude | Calculated (read-only), see Arcade |
   | Crew | Inspection Date, Engine Company, Inspector | Date (default to current date), combo box, **combo box** (searchable; can't filter by company, see below) |
   | Found at Location | Found at Location | Switch |
   | Condition (visible when Found = Yes) | Operable, Corrosion, Gauge, Spindle, Low Pressure, Caps Missing, Shutoff Valve, Obstructed | Radio buttons, switch, number, number, calculated, number, combo box, switch |
   | Markings missing (visible when Found = Yes) | 4 Yes/No fields | Switches |
   | Other issues (visible when Found = Yes) | 6 Yes/No fields | Switches |
   | Follow-up | Needs SFPUC Follow-up, Remarks | Calculated, multi-line text |

   Set Inspection Date, Engine Company, Inspector and Found at Location as **required**, plus Operable and Corrosion when the Condition group shows.
4. **Offline:** Field Maps Designer > Offline, add a map area around the sample hydrants. **Check** that 11.5 offline areas include the related table and attachments.
5. **Check in 11.5:**
   - **Calculated expressions in forms.** Field Maps makes calculated fields read-only, so crews can't override Needs Follow-up there; in Survey123 they can.
   - **Contingent values.** These would let the Inspector list filter by company like it does in Survey123. Without them, crews search the full list.

## 3. Survey123 app

1. Open `survey123/HydrantInspection.xlsx` in **Survey123 Connect** (signed in to gis.sfpuc.org/portal).
   - Point the survey at a **view**, not the source: the public view if public sharing is allowed, otherwise the field view (`VIEWS-AND-WEBMAP.md` step 5).
   - Simplest route: **New Survey > Feature service**, pick that view, then paste in the survey, choices and settings rows from this file. The field names already match.
   - Or open the file directly and set `submission_url` on the settings sheet to the view's URL. `form_id` must stay `HydrantInspections`.
2. **Appearance (Connect > Settings > Appearance):**
   - Header background `#004A80`, header text `#FFFFFF`.
   - Primary/input color `#0074B8`.
   - Logo: the 4 Color Reverse horizontal logo from `sfpuc-design-system/assets/logos`.
3. **Publish.** For crews without accounts, share the survey and the public view with Everyone. This only works if the portal allows anonymous access to items, so **check** with your portal admin; for the MVP, a group of test accounts also works.
4. Paste the survey's item ID into the pop-up link (`field-maps-arcade.md`) so crews can open Survey123 from a hydrant in Field Maps with the hydrant already filled in.

### How the two forms differ (for the staff comparison)

| | Survey123 | Field Maps |
|---|---|---|
| Account needed | Optional (public survey) | Yes |
| Inspector list | Filtered by engine company | One searchable list |
| Issue checklist | One tap-list per section, saved as separate fields | One switch per issue |
| Needs Follow-up | Auto-set, crew can override | Auto-set, read-only |
| Hydrant details | Prefilled by the pop-up link | Filled from the related hydrant |
| Offline | Survey123 field app, but the hydrant must be opened from the link or picked manually | Full offline map with hydrants and their inspections |
| Photos | 2 photo questions | Unlimited attachments |

## 4. Before the staff pilot

- Do a test inspection of the same hydrant in each app and confirm both records show up under that hydrant in Map Viewer.
- Tap-test on a real phone: search at top, 44 px targets, one thumb. In Map Viewer, set GIS ID as the hydrant search field.
- A dashboard (low-pressure list, follow-up count, inspections by company) can come next, built on the same table.
