# 4. Set up pop-ups

**Who:** GIS analyst · **You need:** the web map from step 3 · **Done when:** both pop-ups read at a glance on a phone

Set these in **Map Viewer > select layer > Configure pop-ups**. Field Maps uses the web map's pop-ups as they are.

See both pop-ups on a phone in the [pop-up mockups](https://claude.ai/artifact/4VeRmAyeFMtAFJMPuF19c1), numbered to match the tables below.

> **Check in 11.5, on a phone:** that Field Maps shows the status banner's background color (fallback under [Expression A](#expression-a-status-banner-arcade-element)), and that the **Related records** element exists in 11.5's Map Viewer (fallback in element 6 below).

> **Field names are lower-case on the portal.** Publishing turned `GISID` into `gisid`, `InspDate` into `inspdate`, and so on. Arcade's `$feature.GISID` still works, but field lists and sort strings inside quotes are passed to the data as they are, so the Arcade on this page uses the lower-case names throughout. If an expression fails, see [Pop-up says "Some expressions failed to evaluate"](../reference/troubleshooting.md#pop-up-says-some-expressions-failed-to-evaluate).

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
| 5 | **Arcade** | "Inspect in Survey123" button. Add it in [step 6](06-survey123.md#6d-add-the-inspect-in-survey123-button), once the survey is published. Remove it after the pilot if Field Maps wins |
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
// Finds this hydrant's inspections by GlobalID. The name in quotes is the
// inspections table's name in the map's Layers list; change it if yours differs.
var gid = $feature.globalid;
var insp = Filter(FeatureSetByName($map, "Hydrant Inspections Field - HydrantInspections", ["*"], false),
                  "hydrantguid = @gid");
var n = Count(insp);
var last = First(OrderBy(insp, "inspdate DESC"));

var bg = "#5B6770"; var fg = "#FFFFFF";
var head = "Not inspected yet";
var sub = "No inspections on record";

if (!IsEmpty(last)) {
  var days = DateDiff(Now(), last.inspdate, "days");
  sub = "Last inspected " + Text(last.inspdate, "MMM D, Y") + " by " + last.engineco
        + " · " + n + IIf(n == 1, " inspection", " inspections");
  if (last.foundatloc == "No") { bg = "#BF2620"; head = "Not found at location"; }
  else if (last.needsfollowup == "Yes") { bg = "#BF2620"; head = "Needs SFPUC follow-up"; }
  else if (days > 365) { bg = "#FBB034"; fg = "#000000"; head = "Inspection due"; }
  else { bg = "#597E26"; head = "OK"; }
}

return {
  type: "text",
  text: "<div style='background-color:" + bg + ";color:" + fg + ";padding:10px 12px;border-radius:6px;'>"
      + "<b style='font-size:16px;'>" + head + "</b><br/><span style='font-size:13px;'>" + sub + "</span></div>"
};
```

> **Check in 11.5:** that Field Maps supports Arcade elements and inline `background-color` on `div`. If the background doesn't show on the phone, swap the `<div ...>` for colored bold text: `"<b style='color:" + bg + ";'>" + head + "</b>"` (use black instead of yellow for "Inspection due").

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
Text($feature.inspdate, "MMM D, Y") + " · " + $feature.engineco
```

### Expression C: result banner (Arcade element)

```arcade
var f = $feature;
var bg = "#597E26"; var head = "No follow-up needed";
if (f.foundatloc == "No") { bg = "#BF2620"; head = "Hydrant not found at location"; }
else if (f.needsfollowup == "Yes") { bg = "#BF2620"; head = "Needs SFPUC follow-up"; }
return {
  type: "text",
  text: "<div style='background-color:" + bg + ";color:#FFFFFF;padding:10px 12px;border-radius:6px;'>"
      + "<b style='font-size:16px;'>" + head + "</b></div>"
};
```

### Expression D: issues found (Arcade element)

Lists only the problems, instead of 11 Yes/No rows.

```arcade
Expects($feature, "*");
var f = $feature;
var flags = [
  ["obstructed", "Obstructed"],
  ["missserial", "Serial number missing"],
  ["missspindle", "Spindle pressure not stamped"],
  ["missmainsize", "Main size not labeled"],
  ["missshutoffdist", "Shutoff distance not labeled"],
  ["dmgthreads", "Damaged outlet threads"],
  ["strippedspindle", "Stripped spindle"],
  ["leak", "Leak"],
  ["paintedover", "Painted over"],
  ["dmgcap", "Damaged cap"],
  ["hardtooperate", "Hard to operate"]
];
var out = [];
if (f.lowpressure == "Yes") Push(out, "Low pressure");
if (!IsEmpty(f.operable) && f.operable != "Yes") Push(out, "Operable: " + f.operable);
if (DefaultValue(f.capsmissing, 0) > 0) Push(out, f.capsmissing + " cap(s) missing");
if (!IsEmpty(f.shutoffvalve) && f.shutoffvalve != "OK") Push(out, "Shutoff valve: " + DomainName(f, "shutoffvalve"));
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
var g = $feature.gauge; var s = $feature.spindle;
if (IsEmpty(g)) return "Not measured";
var t = g + " psi measured";
if (!IsEmpty(s)) t += " · " + s + " psi stamped";
if ($feature.lowpressure == "Yes") t += " · LOW";
return t;
```

## Load demo inspections

To see every pop-up state before crews add real inspections, load [data/demo_inspections.csv](../kit/data/demo_inspections.csv): 23 made-up inspections on 17 of the 21 sample hydrants. The script links each one to its hydrant by GIS ID, so it works on the layer you already published.

1. In ArcGIS Pro, sign in to the portal as the owner of the source layer.
2. Copy the **source** layer's service URL (from step 1, ending in `/FeatureServer`). Not the field view: there you can only edit records you created.
3. Open **Python Command Prompt** and run:

    ```
    propy "C:\temp\hydrant-mvp\load_demo_inspections.py" --service <source service URL>
    ```

    If it says it can't open the table, Pro isn't passing your sign-in to the command prompt. Run it from the **Python window** inside Pro instead:

    ```python
    import sys, runpy; sys.argv = [r"C:\temp\hydrant-mvp\load_demo_inspections.py", "--service", r"<source service URL>"]; runpy.run_path(sys.argv[0], run_name="__main__")
    ```

    It prints `Loaded 23 demo inspections`. To load into the geodatabase before publishing instead, use `--gdb C:\temp\HydrantInspections.gdb`.

4. Open the web map. The hydrants now show these states:

| State | Hydrants | What it shows |
|---|---|---|
| Not inspected yet (gray) | 0353, 0564, 3401, 3469 | No inspections on record |
| OK (green) | 0291, 3803, 3466, 3641, 3606 | 0291 has two clean years. 3803 was inspected today. 3466 used inspector "Other" with the name in Remarks. 3641 has no gauge reading ("Not measured"). 3606 is 350 days old, so it turns yellow about two weeks after you load it |
| OK after a repair (green) | 0490, 3658 | Latest inspection is clean; an older one needed follow-up (leak, low pressure) |
| Inspection due (yellow) | 0383, 0570 | Last inspected over a year ago. 0570 has three inspections, the newest two years old |
| Needs SFPUC follow-up (red) | 0358, 3402, 0046, 0563, 3467, 3511, 3808 | 0358 low pressure (38 psi measured, 50 stamped). 3402 inoperable, stripped spindle. 0046 limited, obstructed. 0563 shutoff valve buried. 3467 painted over, serial and spindle stamp missing. 3511 two caps missing, damaged threads. 3808 leak, water in valve box |
| Not found at location (red) | 0718 | Hydrant not found; the rest of the inspection is blank |

The dates in the CSV are moved forward to the day you load it, so the states above hold whenever you run it. The demo records have no photos; add one by hand to test attachments.

**Before the pilot,** remove them. Every demo record's Remarks starts with `DEMO.`, and this deletes only those:

```
propy "C:\temp\hydrant-mvp\load_demo_inspections.py" --service <source service URL> --remove
```

## Check on a phone

- [ ] Hydrant banner color matches the table above for one hydrant in each state (gray 0353, green 0291, yellow 0383, red 0358, not found 0718).
- [ ] Banner and title read without zooming, one-handed.
- [ ] Related inspections list shows newest first, each titled with date and company.
- [ ] Inspection with no problems shows "None" under Issues found.
- [ ] Photos open from the inspection pop-up.
- [ ] All of the above also work with the map taken offline.

## Next

[5. Build the Field Maps form](05-field-maps-form.md)
