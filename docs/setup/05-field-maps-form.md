# 5. Build the Field Maps form

**Who:** GIS analyst · **You need:** the web map from step 3 · **Done when:** a test inspection saves from Field Maps with the hydrant details filled in

Open **Field Maps Designer > Hydrant Inspections MVP > Forms > HydrantInspections table**.

## 5a. Form groups

Build these groups. They mirror the Survey123 form so the pilot compares like with like.

| Group | Fields | Input |
|---|---|---|
| Hydrant | GIS ID, Location, Latitude, Longitude | Calculated (read-only), see [5b](#5b-calculated-fields) |
| Crew | Inspection Date, Engine Company, Inspector | Date (default to current date), combo box, **combo box** (searchable; can't filter by engine company, see [5e](#5e-check-in-115)) |
| Found at Location | Found at Location | Switch |
| Condition (visible when Found = Yes) | Operable, Corrosion, Gauge, Spindle, Low Pressure, Caps Missing, Shutoff Valve, Obstructed | Radio buttons, switch, number, number, calculated, number, combo box, switch |
| Markings missing (visible when Found = Yes) | 4 Yes/No fields | Switches |
| Other issues (visible when Found = Yes) | 6 Yes/No fields | Switches |
| Follow-up | Needs SFPUC Follow-up, Remarks | Calculated, multi-line text |

**Required:** Inspection Date, Engine Company, Inspector and Found at Location, plus Operable and Corrosion when the Condition group shows.

## 5b. Calculated fields

Add each as a calculated expression on its field.

Field names are lower-case on the portal (`gisid`, not `GISID`), so the field lists below use lower case. They look up the hydrant by `hydrantguid` rather than by relationship name, because the relationship name on the published service didn't match (the pop-up banner failed with "Invalid parameter"). `"Hydrants"` is the layer's name in the service; **check** it in the Arcade editor's Profile variables if the expression fails.

**GIS ID** (for **Location**, swap `h.gisid` for `h.location`):

```arcade
var hg = $feature.hydrantguid;
var h = First(Filter(FeatureSetByName($datastore, "Hydrants", ["gisid", "location"], false), "globalid = @hg"));
return IIf(IsEmpty(h), null, h.gisid);
```

**Latitude** (for **Longitude**, return `lon` instead of `lat`). The data is stored in WGS84, but Field Maps can hand the geometry over in the map's Web Mercator meters, so the expression converts when it needs to.

```arcade
var hg = $feature.hydrantguid;
var h = First(Filter(FeatureSetByName($datastore, "Hydrants", ["globalid"], true), "globalid = @hg"));
if (IsEmpty(h)) return null;
var g = Geometry(h);
var lon = g.x; var lat = g.y;
if (Includes([3857, 102100], g.spatialReference.wkid)) {
  // Web Mercator meters to degrees
  var R = 6378137;
  lon = g.x / R * 180 / PI;
  lat = (2 * Atan(Exp(g.y / R)) - PI / 2) * 180 / PI;
}
return Round(lat, 6);
```

**Low Pressure:** Yes when the measured gauge pressure is below the stamped spindle pressure.

```arcade
var g = $feature.gauge;
var s = $feature.spindle;
return IIf(!IsEmpty(g) && !IsEmpty(s) && g < s, "Yes", "No");
```

**Needs SFPUC Follow-up:** Yes if any problem is flagged.

```arcade
var f = $feature;
var flags = [f.obstructed, f.lowpressure, f.missserial, f.missspindle, f.missmainsize,
             f.missshutoffdist, f.dmgthreads, f.strippedspindle, f.leak, f.paintedover,
             f.dmgcap, f.hardtooperate];
var issue = f.foundatloc == "No" || (!IsEmpty(f.operable) && f.operable != "Yes")
            || DefaultValue(f.capsmissing, 0) > 0
            || (!IsEmpty(f.shutoffvalve) && f.shutoffvalve != "OK")
            || Includes(flags, "Yes");
return IIf(issue, "Yes", "No");
```

## 5c. Conditional visibility

On the **Condition**, **Markings missing** and **Other issues** groups:

```arcade
$feature.foundatloc == "Yes"
```

## 5d. Offline

**Field Maps Designer > Offline**: add a map area around the sample hydrants. The map needs an offline-ready basemap first; see [Offline basemap](../reference/offline-basemap.md) for the basemap and the [map area steps](../reference/offline-basemap.md#setting-up-the-offline-area-step-5d).

> **Check in 11.5:** that 11.5 offline areas include the related table and attachments.

## 5e. Check in 11.5

- **Calculated expressions in forms.** Field Maps makes calculated fields read-only, so crews can't override Needs Follow-up there; in Survey123 they can.
- **Contingent values.** These would let the Inspector list filter by engine company like it does in Survey123. Without them, crews search the full list.

## Next

[6. Publish the Survey123 form](06-survey123.md)
