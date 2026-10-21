# 6. Publish the Survey123 form

**Who:** GIS analyst, portal admin (for public sharing) · **You need:** Survey123 Connect, the views from step 2 · **Done when:** a test inspection saves from Survey123, opened from a hydrant pop-up

Use **Survey123 Connect**, not the web designer. The form needs a filtered inspector list (`choice_filter`), hidden calculations and an existing table, which only Connect handles.

## Files for this step

| File | What it is |
|---|---|
| [survey123/HydrantInspection.xlsx](../kit/survey123/HydrantInspection.xlsx) | The XLSForm, ready for Survey123 Connect |
| [build_xlsform.py](../kit/build_xlsform.py) | Regenerates the XLSForm from the schema if fields change (needs `openpyxl`) |

## 6a. Pick which view the survey writes to

One survey, two possible targets:

| If public sharing is allowed | If it isn't |
|---|---|
| Publish against **Hydrant Inspections Public** and share the survey with Everyone | Publish against **Hydrant Inspections Field** and share the survey with the MVP test group |

Ask the portal admin whether the portal allows anonymous access to items. For the MVP, a group of test accounts also works.

## 6b. Set up the survey in Connect

Sign in to Connect with `https://gis.sfpuc.org/portal`, then:

1. **New Survey > Feature service**, and pick the **view** (not the source). Connect builds a starter form from it.
2. That starter form is built on the **Hydrants** layer, with inspections as a repeat inside it. Don't publish it as is: every submission would add a new hydrant point. Our form writes to the inspections table only and gets the hydrant from the pop-up link.
3. In the new survey's folder, open Connect's `.xlsx` and replace its **survey** and **choices** sheets with the ones from `HydrantInspection.xlsx`.
4. On its **settings** sheet, keep Connect's `submission_url` and `namespaces`, and copy in `form_title`, `form_id`, `instance_name`, `version` and `allow_choice_duplicates` from ours. `form_id` must be `HydrantInspections`, the table's name.

Question names are all lower case, because the portal lower-cased the field names when it published the layer.

**Appearance** (Connect > Settings > Appearance), in SFPUC colors:

| Setting | Value |
|---|---|
| Header background | `#004A80` |
| Header text | `#FFFFFF` |
| Primary / input color | `#0074B8` |
| Logo | The 4 Color Reverse horizontal logo from `sfpuc-design-system/assets/logos` (white type, so it needs the dark header) |

## 6c. Publish and share

1. **Publish.**
2. Share the survey with **Everyone** (public view) or the **MVP test group** (field view), matching 6a.

Trade-off to note for the pilot scoring: records sent through the public view have no SFPUC user in `created_user`, so nobody can fix them later from the app. The Inspector pick list still records who did the inspection, and the GIS team can correct records in the source.

## 6d. Add the "Inspect in Survey123" button

This lets crews open Survey123 from a hydrant in Field Maps with the hydrant already filled in.

1. In Map Viewer, open the **Hydrants** pop-up and add an **Arcade** element (element 5 in [the hydrant pop-up](04-popups.md#hydrant-pop-up)).
2. Paste the code below and replace `SURVEY_ITEM_ID` with the survey's item ID.
3. Save the map, then refresh it in Field Maps.

```arcade
var g = Geometry($feature);
var lon = g.x; var lat = g.y;
if (Includes([3857, 102100], g.spatialReference.wkid)) {
  // Web Mercator meters to degrees
  var R = 6378137;
  lon = g.x / R * 180 / PI;
  lat = (2 * Atan(Exp(g.y / R)) - PI / 2) * 180 / PI;
}
var params = {
  "itemID": "SURVEY_ITEM_ID",
  "portalUrl": "https://gis.sfpuc.org/portal",
  "field:hydrantguid": $feature.globalid,
  "field:gisid": $feature.gisid,
  "field:location": $feature.location,
  "field:spindle": $feature.spindlepsi,
  "field:lat": Round(lat, 6),
  "field:lon": Round(lon, 6)
};
// Opens the Survey123 field app, or its web page if the app isn't installed.
// Apostrophes in addresses (33' W KEARNY) are encoded so they don't cut the link short.
var url = "https://survey123.arcgis.app/?" + Replace(UrlEncode(params), "'", "%27");
return {
  type: "text",
  text: '<a href="' + url + '" style="display:block;padding:12px;background-color:#0074B8;color:#FFFFFF;border-radius:6px;text-align:center;font-weight:bold;text-decoration:none;">Inspect in Survey123</a>'
};
```

The link points at the survey, not a layer, so it works with either view. The `field:` names must match the form's question names exactly, in lower case, or the form opens blank.

**Why an Arcade element and not a Text element link?** A Text element whose link is `{expression/...}` silently disappeared in Field Maps during testing. The Arcade element builds the whole link itself, and it shows as a full-width button that's easy to hit with a thumb.

## Next

[7. Test before the pilot](07-test.md)
