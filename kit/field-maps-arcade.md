# Arcade for the hydrant inspection MVP

Relationship name used below: `Hydrants_HydrantInspections` (the relationship class `build_hydrant_gdb.py` creates). If the published service shows a different name in Map Viewer's Arcade profile, use that one.

## Field Maps form: calculated expressions (HydrantInspections table)

Hydrant details from the related hydrant. Use one expression per field and change the returned attribute:

```arcade
// GIS ID  (swap "GISID" for "Location" in the Location expression)
var h = First(FeatureSetByRelationshipName($feature, "Hydrants_HydrantInspections", ["GISID", "Location"], false));
return IIf(IsEmpty(h), null, h.GISID);
```

```arcade
// Latitude  (use .x for Longitude). The sample data is stored in WGS84, so y is latitude.
var h = First(FeatureSetByRelationshipName($feature, "Hydrants_HydrantInspections", ["GlobalID"], true));
return IIf(IsEmpty(h), null, Round(Geometry(h).y, 6));
```

Low Pressure:

```arcade
var g = $feature.Gauge;
var s = $feature.Spindle;
return IIf(!IsEmpty(g) && !IsEmpty(s) && g < s, "Yes", "No");
```

Needs SFPUC Follow-up:

```arcade
var f = $feature;
var flags = [f.Obstructed, f.LowPressure, f.MissSerial, f.MissSpindle, f.MissMainSize,
             f.MissShutoffDist, f.DmgThreads, f.StrippedSpindle, f.Leak, f.PaintedOver,
             f.DmgCap, f.HardToOperate];
var issue = f.FoundAtLoc == "No" || (!IsEmpty(f.Operable) && f.Operable != "Yes")
            || DefaultValue(f.CapsMissing, 0) > 0
            || (!IsEmpty(f.ShutoffValve) && f.ShutoffValve != "OK")
            || Includes(flags, "Yes");
return IIf(issue, "Yes", "No");
```

## Field Maps form: conditional visibility

Condition, Markings missing and Other issues groups:

```arcade
$feature.FoundAtLoc == "Yes"
```

## Hydrant pop-up: "Inspect in Survey123" link

Add an Arcade expression to the Hydrants pop-up and use it as a link (Text element, link URL `{expression/s123}`). Replace `SURVEY_ITEM_ID` after publishing the survey.

```arcade
var params = {
  "itemID": "SURVEY_ITEM_ID",
  "portalUrl": "https://gis.sfpuc.org/portal",
  "field:HydrantGUID": $feature.GlobalID,
  "field:GISID": $feature.GISID,
  "field:Location": $feature.Location,
  "field:Spindle": $feature.SpindlePSI,
  "field:Lat": Round(Geometry($feature).y, 6),
  "field:Lon": Round(Geometry($feature).x, 6)
};
// Opens the Survey123 field app. For a browser instead, use
// "https://survey123.arcgis.com/share/SURVEY_ITEM_ID?" + UrlEncode(params)
return "arcgis-survey123://?" + UrlEncode(params);
```
