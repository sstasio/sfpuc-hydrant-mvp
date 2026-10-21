# 5. Build the Field Maps form

**Who:** GIS analyst · **You need:** the web map from step 3 · **Done when:** a test inspection saves from Field Maps with the hydrant details filled in

This step builds the form crews fill in when they add an inspection in Field Maps. Without it, Field Maps falls back to a plain list of the pop-up's fields, with no Hydrant group, no automatic values and nothing hidden.

The form is saved in the web map, so build it on `Hydrant Inspections MVP`, the map from step 3. Labels below are from Field Maps Designer and may differ slightly in 11.5.

## 5a. Lay out the form

### Open the form builder

1. Sign in to `https://gis.sfpuc.org/portal` as the map's owner.
2. Open **Field Maps Designer**: the app launcher (the grid of squares, top right) **> Field Maps Designer**, or go to `https://gis.sfpuc.org/portal/apps/fieldmaps/`.
3. Pick the **Hydrant Inspections MVP** map, then **Forms** in the left bar.
4. In the list of layers and tables, pick the **HydrantInspections** table, not the Hydrants layer.
5. If it asks how to start, choose to start from the pop-up or from a new, blank form. Both give the same result here, because you'll set every field below.

In the builder:

- **The form** in the middle shows what crews will see, top to bottom.
- **Fields** lists the table's fields, ready to drag onto the form.
- **Form elements**, on the right side of the screen, holds **Group** and the other elements you can add.
- **Settings** for whatever you select on the form open when you select it.

### Add the fields first

Field Maps won't let you add groups to an empty form, so put the fields on the form first and group them after.

1. Drag each field in the table below from the **Fields** list onto the form, top to bottom in the order shown.
2. Select each field and set it up in its settings:
    - **Display name:** the label crews see (the Label column).
    - **Input type:** what crews tap. For a switch, set the **On** value to `Yes` and **Off** to `No`.
    - **Required:** on for the fields marked Yes.
    - **Editable:** leave on, except where the table says Calculated. Calculated fields turn read-only by themselves.

| Group | Field | Label | Input type | Required | Notes |
|---|---|---|---|---|---|
| Hydrant | `gisid` | GIS ID | Single line text | | Calculated, [5b](#5b-calculated-fields) |
| Hydrant | `location` | Location | Single line text | | Calculated |
| Hydrant | `lat` | Latitude | Number | | Calculated |
| Hydrant | `lon` | Longitude | Number | | Calculated |
| Crew | `inspdate` | Inspection date | Date, with time | Yes | Default to the current date and time, if 11.5 offers it |
| Crew | `engineco` | Engine company | Combo box | Yes | |
| Crew | `inspector` | Inspector | Combo box | Yes | Crews type to search the list |
| Found at location | `foundatloc` | Hydrant found at this location? | Switch | Yes | |
| Condition | `operable` | Operable | Radio buttons | Yes | Required only applies while the group shows |
| Condition | `corrosion` | Corrosion | Switch | Yes | |
| Condition | `gauge` | Gauge pressure (psi) | Number | | |
| Condition | `spindle` | Spindle pressure (psi) | Number | | |
| Condition | `lowpressure` | Low pressure | Switch | | Calculated |
| Condition | `capsmissing` | Caps missing | Number | | |
| Condition | `shutoffvalve` | Shutoff valve | Combo box | | |
| Condition | `obstructed` | Obstructed | Switch | | |
| Markings missing | `missserial` | Serial number missing or unreadable | Switch | | |
| Markings missing | `missspindle` | Spindle pressure not stamped or unreadable | Switch | | |
| Markings missing | `missmainsize` | Main size not labeled | Switch | | |
| Markings missing | `missshutoffdist` | Distance to shutoff not labeled | Switch | | |
| Other issues | `dmgthreads` | Damaged outlet threads | Switch | | |
| Other issues | `strippedspindle` | Stripped or rounded spindle | Switch | | |
| Other issues | `leak` | Leak (outlet, bonnet or spindle) | Switch | | |
| Other issues | `paintedover` | Painted over | Switch | | |
| Other issues | `dmgcap` | Damaged cap | Switch | | |
| Other issues | `hardtooperate` | Hard to operate | Switch | | |
| Follow-up | `needsfollowup` | Needs SFPUC follow-up | Switch | | Calculated |
| Follow-up | `remarks` | Remarks | Multiline text | | |

### Then group them

A group is a heading that holds fields and can collapse. With the fields on the form:

1. Drag **Group** from **Form elements** (right side of the screen) onto the form, just above the first field it should hold.
2. With the group selected, set its **Label** in its settings, and set **Initial state** to **Expanded**.
3. Drag that group's fields (the Group column in the table above) into it.
4. Repeat until you have the seven groups below, in this order. Drag a group up or down to reorder it, and its fields move with it.

| Group label | Shows | Initial state |
|---|---|---|
| Hydrant | Always | Expanded |
| Crew | Always | Expanded |
| Found at location | Always | Expanded |
| Condition | Only when found = Yes ([5c](#5c-conditional-visibility)) | Expanded |
| Markings missing | Only when found = Yes | Expanded |
| Other issues | Only when found = Yes | Expanded |
| Follow-up | Always | Expanded |

Leave these out of the form: `hydrantguid` (Field Maps fills it when the inspection is added from a hydrant), ObjectID, GlobalID and the editor tracking fields. Photos come from the attachments section Field Maps adds on its own.

Click **Save** at the top often. Nothing reaches the phone until you save.

## 5b. Calculated fields

A calculated field fills itself in from an Arcade expression, and crews can't change it.

**To add one:**

1. In the middle, select the field (for example GIS ID).
2. On the right, find **Calculated expression** (under **Logic**) and choose **New expression**. If you've already made the expression, pick it from the list instead.
3. The Arcade editor opens. Give the expression a **title** (for example `Hydrant GIS ID`), paste the code from below, and click **Run** to check it. A test run can return nothing when the sample record has no hydrant; that's fine.
4. Click **Done**, then **Save** the form.

Do this for all six calculated fields: GIS ID, Location, Latitude, Longitude, Low pressure and Needs SFPUC follow-up.

Field names are lower case on the portal (`gisid`, not `GISID`), so the code uses lower case. It finds the hydrant by `hydrantguid` rather than by relationship name, because the relationship name on the published service didn't match (the pop-up banner failed with "Invalid parameter"). `"Hydrants"` is the layer's name in the service. If an expression fails, check that name under **Profile variables** in the Arcade editor.

**GIS ID** (title `Hydrant GIS ID`). For **Location**, make a second expression titled `Hydrant location` and change `h.gisid` on the last line to `h.location`.

```arcade
var hg = $feature.hydrantguid;
var h = First(Filter(FeatureSetByName($datastore, "Hydrants", ["gisid", "location"], false), "globalid = @hg"));
return IIf(IsEmpty(h), null, h.gisid);
```

**Latitude** (title `Hydrant latitude`). For **Longitude**, make a second expression titled `Hydrant longitude` and change the last line to `return Round(lon, 6);`. The data is stored in WGS84, but Field Maps can hand the geometry over in the map's Web Mercator meters, so the expression converts when it needs to.

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

**Low pressure** (title `Low pressure`): Yes when the measured gauge pressure is below the stamped spindle pressure.

```arcade
var g = $feature.gauge;
var s = $feature.spindle;
return IIf(!IsEmpty(g) && !IsEmpty(s) && g < s, "Yes", "No");
```

**Needs SFPUC follow-up** (title `Needs follow-up`): Yes if any problem is flagged.

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

Conditional visibility hides a group or field until an expression is true. Here, the three condition groups stay hidden until the crew says the hydrant is there.

**To add it:**

1. In the middle, select the **Condition** group (the group itself, not a field inside it).
2. On the right, find **Conditional visibility** (under **Logic**) and choose **New expression**.
3. Title it `Hydrant found`, paste the line below, then **Done**.
4. Select the **Markings missing** group, open **Conditional visibility**, and pick the same `Hydrant found` expression from the list. Do the same for **Other issues**.
5. **Save** the form.

```arcade
$feature.foundatloc == "Yes"
```

Hidden fields aren't required, so Operable and Corrosion only become required once the Condition group shows.

### Check it before handing over

On a phone, reopen the map in Field Maps (pull down on the map list to refresh it), open hydrant **0291** and add an inspection:

- [ ] The Hydrant group shows 0291, its location, and a latitude and longitude in degrees, before you enter anything.
- [ ] Until found at location is set to Yes, the Condition, Markings missing and Other issues groups are hidden.
- [ ] A gauge of 40 turns Low pressure and Needs SFPUC follow-up on by themselves.
- [ ] You can't submit without an engine company, an inspector and an answer for found at location.

## 5d. Offline

**Field Maps Designer > Offline**: add a map area around the sample hydrants. The map needs an offline-ready basemap first; see [Offline basemap](../reference/offline-basemap.md) for the basemap and the [map area steps](../reference/offline-basemap.md#setting-up-the-offline-area-step-5d).

> **Check in 11.5:** that 11.5 offline areas include the related table and attachments.

## 5e. Check in 11.5

- **Calculated expressions in forms.** Field Maps makes calculated fields read-only, so crews can't override Needs Follow-up there; in Survey123 they can.
- **Default date.** Whether the Date input can default to the current date and time. If it can't, crews tap the date and pick today.
- **Contingent values.** These would let the Inspector list filter by engine company like it does in Survey123. Without them, crews search the full list.

## Next

[6. Publish the Survey123 form](06-survey123.md)
