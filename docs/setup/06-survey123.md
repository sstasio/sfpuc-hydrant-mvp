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

Sign in to Connect with `https://gis.sfpuc.org/portal`, then either:

- **Simplest:** **New Survey > Feature service**, pick the **view** (not the source), then paste in the survey, choices and settings rows from `HydrantInspection.xlsx`. The field names already match.
- **Or** open `HydrantInspection.xlsx` directly and set `submission_url` on the settings sheet to the view's URL, ending at `FeatureServer` (no layer number). `submission_url` is blank on purpose. `form_id` must stay `HydrantInspections`.

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

## 6d. Add the "Inspect in Survey123" link

This lets crews open Survey123 from a hydrant in Field Maps with the hydrant already filled in.

1. In Map Viewer, open the **Hydrants** pop-up, **Attribute expressions > Add**, name it `s123`, and paste the code below.
2. Replace `SURVEY_ITEM_ID` with the survey's item ID.
3. Add a **Text** element (element 5 in [the hydrant pop-up](04-popups.md#hydrant-pop-up)). Type `Inspect in Survey123`, select it, click the link button, and enter `{expression/s123}` as the URL.

```arcade
var params = {
  "itemID": "SURVEY_ITEM_ID",
  "portalUrl": "https://gis.sfpuc.org/portal",
  "field:HydrantGUID": $feature.globalid,
  "field:GISID": $feature.gisid,
  "field:Location": $feature.location,
  "field:Spindle": $feature.spindlepsi,
  "field:Lat": Round(Geometry($feature).y, 6),
  "field:Lon": Round(Geometry($feature).x, 6)
};
// Opens the Survey123 field app. For a browser instead, use
// "https://survey123.arcgis.com/share/SURVEY_ITEM_ID?" + UrlEncode(params)
return "arcgis-survey123://?" + UrlEncode(params);
```

The link points at the survey, not a layer, so it works with either view.

**Why a Text element and not an Arcade element?** The Arcade only builds the web address; it lives under **Attribute expressions**, and `{expression/s123}` is the placeholder that drops that address into the link. An Arcade element could return an HTML `<a href>` link instead, but the Text element is simpler and easier to restyle.

## Next

[7. Test before the pilot](07-test.md)
