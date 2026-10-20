# Schema and field reasons

Hydrants only. Based on the requested field list (2026-10-16) and the SFFD FY22-23 "Items Needing Attention" report (low-pressure hydrant section: 1,882 rows, 44 engine companies, 458 inspector names).

The built schema lives in [build_hydrant_gdb.py](../kit/build_hydrant_gdb.py), which is the source of truth for field names, types and domains. This page explains why each field exists.

## Fields as built

Generated from [build_hydrant_gdb.py](../kit/build_hydrant_gdb.py). Both have GlobalIDs and editor tracking (`created_user`, `created_date`, `last_edited_user`, `last_edited_date`); the inspections table also takes photo attachments. Hydrants are stored in WGS84 (WKID 4326); change `SPATIAL_REF` in the script for State Plane. The relationship `Hydrants_HydrantInspections` links `Hydrants.GlobalID` to `HydrantInspections.HydrantGUID`, one hydrant to many inspections.

### Hydrants (layer 0)

| Field | Alias | Type | Domain |
|---|---|---|---|
| `GISID` | GIS ID | Text (20) |  |
| `SerialNo` | Serial Number | Text (20) |  |
| `Location` | Address/Location | Text (150) |  |
| `PressureType` | System | Text (10) | PressureType |
| `MainSize` | Main Size (in) | Short integer |  |
| `SpindlePSI` | Stamped Spindle Pressure (psi) | Short integer | PressurePSI |
| `ShutoffDist` | Distance to Shutoff (ft) | Short integer |  |
| `EngineCo` | Engine Company | Text (5) | EngineCompany |

### HydrantInspections (table 1)

| Field | Alias | Type | Domain |
|---|---|---|---|
| `HydrantGUID` | Hydrant | GUID |  |
| `GISID` | GIS ID | Text (20) |  |
| `InspDate` | Inspection Date | Date |  |
| `EngineCo` | Engine Company | Text (5) | EngineCompany |
| `Inspector` | Inspector | Text (50) | Inspector |
| `Location` | Address/Location | Text (150) |  |
| `Lat` | Latitude | Double |  |
| `Lon` | Longitude | Double |  |
| `FoundAtLoc` | Found at Location | Text (3) | YesNo |
| `Operable` | Operable | Text (10) | Operable |
| `Corrosion` | Corrosion | Text (3) | YesNo |
| `Gauge` | Gauge Pressure (psi) | Short integer | PressurePSI |
| `Spindle` | Spindle Pressure (psi) | Short integer | PressurePSI |
| `LowPressure` | Low Pressure | Text (3) | YesNo |
| `CapsMissing` | Caps Missing | Short integer | CapsMissing |
| `ShutoffValve` | Shutoff Valve | Text (20) | ShutoffValve |
| `Obstructed` | Obstructed | Text (3) | YesNo |
| `MissSerial` | Serial number missing or unreadable | Text (3) | YesNo |
| `MissSpindle` | Spindle pressure not stamped or unreadable | Text (3) | YesNo |
| `MissMainSize` | Main size not labeled | Text (3) | YesNo |
| `MissShutoffDist` | Distance to shutoff not labeled | Text (3) | YesNo |
| `DmgThreads` | Damaged outlet threads | Text (3) | YesNo |
| `StrippedSpindle` | Stripped or rounded spindle | Text (3) | YesNo |
| `Leak` | Leak (outlet, bonnet or spindle) | Text (3) | YesNo |
| `PaintedOver` | Painted over | Text (3) | YesNo |
| `DmgCap` | Damaged cap | Text (3) | YesNo |
| `HardToOperate` | Hard to operate | Text (3) | YesNo |
| `NeedsFollowup` | Needs SFPUC Follow-up | Text (3) | YesNo |
| `Remarks` | Remarks | Text (1000) |  |

### Domains

| Domain | Values |
|---|---|
| `YesNo` | Yes, No |
| `EngineCompany` | E01 to E51 |
| `Inspector` | 279 names from inspectors.csv, plus Other |
| `Operable` | Yes, Limited, No |
| `ShutoffValve` | OK, Buried or paved over, Inaccessible, Water in valve box, Not found |
| `PressureType` | Low pressure, High pressure (AWSS) |
| `PressurePSI` | 0 to 300 |
| `CapsMissing` | 0 to 3 |

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

## Original draft: inspection table

The field list as first drafted. The additions below were all built, as separate Yes/No fields so Field Maps can show them as switches and the dashboard can count each one.

### Draft core fields

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

### Draft additions (each is a recurring remark in the report)

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
