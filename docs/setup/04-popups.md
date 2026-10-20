# 4. Set up pop-ups

**Who:** GIS analyst · **You need:** the web map from step 3 · **Done when:** both pop-ups read at a glance on a phone

Set these in **Map Viewer > select layer > Configure pop-ups**. Field Maps uses the web map's pop-ups as they are.

See both pop-ups on a phone in the [pop-up mockups](https://claude.ai/artifact/4VeRmAyeFMtAFJMPuF19c1), numbered to match the tables below.

> **Check in 11.5, on a phone:** that Field Maps shows the status banner's background color (fallback under [Expression A](#expression-a-status-banner-arcade-element)), and that the **Related records** element exists in 11.5's Map Viewer (fallback in element 6 below).

## Rules for both pop-ups

- **Answer first.** The top of each pop-up says whether the hydrant needs attention, so a crew member gets it without scrolling.
- **Show only what someone acts on.** No GlobalIDs, lat/long, or editor tracking fields. Lat/long is in the map; Field Maps shows the coordinates itself.
- **Short labels.** The phone column is narrow; labels over about 20 characters wrap and push values down.
- **Status colors** (SFPUC app theme, all pass contrast):

  | Status | Background | Text |
  |---|---|---|
  | Needs follow-up / not found | `#BF2620` red | white |
  | Inspection due (over 1 year) | `#FBB034` yellow | black |
  | OK | `#597E26` green | white |
  | Not inspected yet | `#5B6770` gray | white |

## Hydrant pop-up

Layer: **Hydrants**. Elements top to bottom:

| # | Element | Content |
|---|---|---|
| 1 | **Title** | `Hydrant {GISID}` |
| 2 | **Arcade** | Status banner (expression A below) |
| 3 | **Text** | `{Location}` |
| 4 | **Fields** | See field list below |
| 5 | **Text** | "Inspect in Survey123" link. Add it in [step 6](06-survey123.md#6d-add-the-inspect-in-survey123-link), once the survey is published. Remove it after the pilot if Field Maps wins |
| 6 | **Related records** | Inspections, sorted by Inspection Date, newest first, show 3. **Check in 11.5** that this element exists in 11.5 Map Viewer; if not, Field Maps still lists related inspections at the bottom of the pop-up |

Fields element (in this order, with these display labels):

| Field | Label in pop-up | Format |
|---|---|---|
| SpindlePSI | Stamped pressure | `{SpindlePSI} psi`, no decimals |
| PressureType | System | Domain label (Low pressure / High pressure (AWSS)) |
| EngineCo | Engine company | |
| MainSize | Main size (in) | No decimals |
| ShutoffDist | Shutoff distance (ft) | No decimals |
| SerialNo | Serial number | |

Turn off every other field (GISID and Location are already in the title and text). In Field Maps, empty values show as blank rows; that's fine for the MVP since most sample hydrants are missing main size and shutoff distance, and the blanks show crews what's missing.

**Add inspection button.** Field Maps adds this itself under the related inspections, because the table is editable in the map. No setup needed.

### Expression A: status banner (Arcade element)

```arcade
// Status banner for the hydrant pop-up. Reads the latest related inspection.
var insp = FeatureSetByRelationshipName($feature, "Hydrants_HydrantInspections",
    ["InspDate", "EngineCo", "NeedsFollowup", "FoundAtLoc"], false);
var n = Count(insp);
var last = First(OrderBy(insp, "InspDate DESC"));

var bg = "#5B6770"; var fg = "#FFFFFF";
var head = "Not inspected yet";
var sub = "No inspections on record";

if (!IsEmpty(last)) {
  var days = DateDiff(Now(), last.InspDate, "days");
  sub = "Last inspected " + Text(last.InspDate, "MMM D, Y") + " by " + last.EngineCo
        + " · " + n + IIf(n == 1, " inspection", " inspections");
  if (last.FoundAtLoc == "No") { bg = "#BF2620"; head = "Not found at location"; }
  else if (last.NeedsFollowup == "Yes") { bg = "#BF2620"; head = "Needs SFPUC follow-up"; }
  else if (days > 365) { bg = "#FBB034"; fg = "#000000"; head = "Inspection due"; }
  else { bg = "#597E26"; head = "OK"; }
}

return {
  type: "text",
  text: `<div style="background-color:${bg};color:${fg};padding:10px 12px;border-radius:6px;">`
      + `<b style="font-size:16px;">${head}</b><br/><span style="font-size:13px;">${sub}</span></div>`
};
```

> **Check in 11.5:** that Field Maps supports Arcade elements and inline `background-color` on `div`. If the background doesn't show on the phone, swap to colored bold text: `<b style="color:#BF2620;">${head}</b>`.

## Inspection pop-up

Table: **HydrantInspections**. Crews see this when they tap an inspection under a hydrant. The title is also what Field Maps shows in the related records list, so it has to identify the inspection on its own.

| # | Element | Content |
|---|---|---|
| 1 | **Title** | `{expression/title}` (expression B), e.g. *May 12, 2026 · E01* |
| 2 | **Arcade** | Result banner (expression C) |
| 3 | **Fields** | See field list below |
| 4 | **Arcade** | Issues found (expression D) |
| 5 | **Text** | `<b>Remarks</b><br/>{Remarks}` |
| 6 | **Attachments** | Photos, shown as a list (thumbnails) |

Fields element (in this order):

| Field | Label in pop-up | Format |
|---|---|---|
| Inspector | Inspector | Domain label |
| InspDate | Inspected | Short date and time |
| `{expression/pressure}` | Pressure | Expression E, e.g. *48 psi measured · 62 psi stamped · LOW* |
| Operable | Operable | |
| Corrosion | Corrosion | |
| CapsMissing | Caps missing | No decimals |
| ShutoffValve | Shutoff valve | Domain label |

Turn off: HydrantGUID, GISID, Location, Lat, Lon, EngineCo (it's in the title), FoundAtLoc, LowPressure, NeedsFollowup (all in the banner or pressure line), Gauge, Spindle (in the pressure line), Obstructed and the 10 marking and issue flags (in the issues list), Remarks (own element), and the editor tracking fields.

### Expression B: title

```arcade
Text($feature.InspDate, "MMM D, Y") + " · " + $feature.EngineCo
```

### Expression C: result banner (Arcade element)

```arcade
var f = $feature;
var bg = "#597E26"; var head = "No follow-up needed";
if (f.FoundAtLoc == "No") { bg = "#BF2620"; head = "Hydrant not found at location"; }
else if (f.NeedsFollowup == "Yes") { bg = "#BF2620"; head = "Needs SFPUC follow-up"; }
return {
  type: "text",
  text: `<div style="background-color:${bg};color:#FFFFFF;padding:10px 12px;border-radius:6px;">`
      + `<b style="font-size:16px;">${head}</b></div>`
};
```

### Expression D: issues found (Arcade element)

Lists only the problems, instead of 11 Yes/No rows.

```arcade
Expects($feature, "*");
var f = $feature;
var flags = [
  ["Obstructed", "Obstructed"],
  ["MissSerial", "Serial number missing"],
  ["MissSpindle", "Spindle pressure not stamped"],
  ["MissMainSize", "Main size not labeled"],
  ["MissShutoffDist", "Shutoff distance not labeled"],
  ["DmgThreads", "Damaged outlet threads"],
  ["StrippedSpindle", "Stripped spindle"],
  ["Leak", "Leak"],
  ["PaintedOver", "Painted over"],
  ["DmgCap", "Damaged cap"],
  ["HardToOperate", "Hard to operate"]
];
var out = [];
if (f.LowPressure == "Yes") Push(out, "Low pressure");
if (!IsEmpty(f.Operable) && f.Operable != "Yes") Push(out, "Operable: " + f.Operable);
if (DefaultValue(f.CapsMissing, 0) > 0) Push(out, f.CapsMissing + " cap(s) missing");
if (!IsEmpty(f.ShutoffValve) && f.ShutoffValve != "OK") Push(out, "Shutoff valve: " + DomainName(f, "ShutoffValve"));
for (var i in flags) {
  if (f[flags[i][0]] == "Yes") Push(out, flags[i][1]);
}
if (Count(out) == 0) {
  return { type: "text", text: "<b>Issues found</b><br/>None" };
}
return { type: "text", text: "<b>Issues found</b><br/>• " + Concatenate(out, "<br/>• ") };
```

### Expression E: pressure line (attribute expression)

```arcade
var g = $feature.Gauge; var s = $feature.Spindle;
if (IsEmpty(g)) return "Not measured";
var t = g + " psi measured";
if (!IsEmpty(s)) t += " · " + s + " psi stamped";
if ($feature.LowPressure == "Yes") t += " · LOW";
return t;
```

## Check on a phone

- [ ] Hydrant banner color matches the latest inspection for one hydrant in each state (add test inspections to get red, green and gray; edit a date in the source to get yellow).
- [ ] Banner and title read without zooming, one-handed.
- [ ] Related inspections list shows newest first, each titled with date and company.
- [ ] Inspection with no problems shows "None" under Issues found.
- [ ] Photos open from the inspection pop-up.
- [ ] All of the above also work with the map taken offline.

## Next

[5. Build the Field Maps form](05-field-maps-form.md)
