# Hydrant inspection schema (draft v1)

Hydrants only. Based on Sean's field list (2026-10-16) and the SFFD FY22-23 "Items Needing Attention" report (`sffd-issues-noted-fy2223.txt`, low-pressure hydrant section: 1,882 rows, 44 engine companies, 458 inspector names).

## What Gauge and Spindle are

| Field | Meaning (from the report) | Evidence | Type |
|---|---|---|---|
| **Gauge** | Static water pressure (psi) the crew reads with a gauge on the outlet during the inspection | Remarks such as "35 psi on gauge", "Read 35 psi"; values cluster at 50 to 110 | **Short Integer** |
| **Spindle** | Pressure (psi) stamped on the hydrant's operating spindle: the rated or expected static pressure, a fixed asset attribute | Remarks such as "spindle pressure not stamped", "Re-stamp spindle pressure", "Spindle PSI not stamped", "No pressure imprint on the spindle" | **Short Integer** |

- All ~1,735 readings in the report are whole numbers (the one decimal in the file is part of an address). Medians: gauge 75, spindle 70.
- **Gauge was below spindle in 561 readings**, which is what puts a hydrant on the "Low Pressure" list. That comparison is worth calculating automatically.
- **0 is used for "no reading"** (48 gauges at 0, and a "no hydrant at indicated location" row). In the new form, leave the field empty for no reading so averages aren't skewed.
- A few typos (gauge 820, spindle 770). Add a range check of 0 to 300 psi.
- The spindle stamp is often missing or illegible. Since it belongs to the hydrant rather than the visit, the real fix is to store it on the hydrant layer and show it in the form. The inspection then records whether the stamp is legible.

## Inspection table (related to hydrant layer, 1:M on GlobalID → HydrantGUID)

| Field | Alias | Type | Domain / rule | Notes |
|---|---|---|---|---|
| HydrantGUID | Hydrant | GUID | Required | Set by the relationship, not typed |
| GISID | GIS ID | Text (20) | Required, prefilled from hydrant | Report uses 4-digit serials (1,582 of 1,882), with odd ones like "?049" and "B0039" |
| InspDate | Inspection Date | Date | Required, default now | |
| EngineCo | Engine Company | Text (5) | Domain E01 to E51 | 44 companies in the report |
| Inspector | Inspector | Text (50) | See note below | |
| Location | Address/Location | Text (150) | Prefilled from hydrant | Kept for reference; the map point is the real location |
| Lat, Lon | Latitude, Longitude | Double | Calculated from geometry or device GPS | Read-only |
| Corrosion | Corrosion | Text (3) | Yes/No, required | Report mixes Y, N, No and blank |
| Gauge | Gauge Pressure (psi) | Short Integer | 0 to 300, empty = no reading | |
| Spindle | Spindle Pressure (psi) | Short Integer | 0 to 300, prefilled from hydrant if known | |
| LowPressure | Low Pressure | Text (3) | Calculated: Yes when Gauge < Spindle | Drives the dashboard list |
| Remarks | Remarks | Text (1000) | | |

## Suggested additions (each is a recurring remark in the report)

| Field | Type | Domain | Report lines it replaces |
|---|---|---|---|
| Found at location | Yes/No | Required | "no hydrant at indicated location" |
| Operable | Text | Yes / Limited / No | "inoperable", "unable to use", "operable with vice grips" |
| Caps missing | Short Integer | 0 to 3 | ~200 "missing cap(s)" |
| Markings missing | Multi-select | Serial, Spindle pressure, Main size, Distance to shutoff | ~490 main size, ~260 serial, many spindle |
| Physical issues | Multi-select | Damaged threads, Stripped or rounded spindle, Leak (outlet, bonnet or spindle), Painted over, Damaged cap, Hard to operate | Leaks, threads, stripped spindles |
| Shutoff valve | Text | OK / Buried or paved over / Inaccessible / Water in box / Not found | ~440 shutoff lines |
| Obstructed | Yes/No | | Bushes, parked cars, behind gates |
| Needs SFPUC follow-up | Yes/No | Calculated Yes if any issue, editable | "Water Dept. notified" |
| Photos | Attachments | At least 1 when an issue is flagged | |

Hydrant layer attributes to hold (or verify) so crews don't retype them: GISID, serial, main size, stamped spindle pressure, distance to shutoff, pressure zone, type (low pressure).

## Inspector without an account

- With 458 names in one year, a single dropdown is too long. Use Engine Company first, then a name list filtered to that company, plus an "Other" free-text option.
- **Accounts are a key comparison point.** Field Maps needs a signed-in ArcGIS account to edit. Survey123 can run as a public survey on Enterprise if the portal allows anonymous access, so crews without accounts can submit. Survey123 handles the filtered name list natively (`choice_filter`). In Field Maps the closest option is contingent values, which need checking in the 11.5 Field Maps Designer.
