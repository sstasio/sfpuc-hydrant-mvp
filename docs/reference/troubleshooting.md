# Troubleshooting

Fixes for problems found while setting up the MVP on the portal.

## "Features with true curves cannot currently be edited"

**Where you see it:** Field Maps Designer (form or offline pages) or the Field Maps app, on Hydrants or HydrantInspections.

**Why:** our data has no curves at all (points and a table), so this is a service setting, not a data problem. When Pro publishes a layer, it can turn on **Only allow true curve updates by true curve clients**. Field Maps isn't a "true curve client", so it refuses to edit the whole layer. Esri tracks the false alarm as [BUG-000173715](https://support.esri.com/en-us/bug/arcgis-field-maps-designer-returns-the-error-features-w-bug-000173715).

**Fix:** turn that one setting off on every service Field Maps or Survey123 edits through. Nothing is lost by doing it here: the only downside Esri lists is that real curves edited in Field Maps get turned into straight segments, and we have none.

### 1. Find which services have it on

Open each service's REST page with `?f=pjson` on the end, signed in as the owner, and search the page for `TrueCurve`:

- the source layer
- `Hydrant Inspections Field` (the one the Field Maps map uses, so it matters most)
- `Hydrant Inspections Public`, if you made it

The URL is on each item page, bottom right (**URL**). It looks like `https://gis.sfpuc.org/server/rest/services/Hosted/<ServiceName>/FeatureServer?f=pjson`.

A service needs fixing if it shows `"onlyAllowTrueCurveUpdatesByTrueCurveClients": true`.

### 2. Turn it off in the ArcGIS Server admin directory

**Who:** portal admin, or the service owner if they can sign in to the server admin directory.

1. Go to the hosting server's admin directory: `https://gis.sfpuc.org/server/admin` (use your hosting server's address if it differs from the portal's). Sign in with a portal admin account.
2. **services > Hosted**, then click the service by name.
3. Click **edit**. The service's JSON opens in a text box.
4. Use the browser's Find (Ctrl+F) for `TrueCurve`. Change **every** match of:
    - `onlyAllowTrueCurveUpdatesByTrueCurveClients` to `false`
    - `allowTrueCurvesUpdates` to `true`

    Each can appear more than once, so keep going until Find finds no more `true` for the first one.
5. **Save Edits**. The service restarts, which takes a few seconds.
6. Repeat for each view from step 1. Views are their own services in the **Hosted** folder.

> **Check in 11.5:** the label in step 3 may read **edit** or **Edit Service**, and `allowTrueCurvesUpdates` may not be in a view's JSON at all. If it isn't there, only change the one that is.

### 3. Check it worked

1. Reload the `?f=pjson` page from step 1. It should now show `"onlyAllowTrueCurveUpdatesByTrueCurveClients": false`.
2. Reopen the map in **Field Maps Designer**. The warning should be gone from the form and offline pages.
3. On phones, **remove any downloaded offline areas and download them again**. An offline copy keeps the old setting.

If the warning is still there after this, it's the Designer bug itself rather than the setting. Note the Field Maps Designer build (bottom of its Help menu) and open a case with Esri support citing BUG-000173715.

### Stop it coming back

If you ever republish or overwrite the source from Pro, in **Share As Web Layer > Configuration**, open the layer properties (pencil icon next to **Feature**) and **uncheck Only allow true curve updates by true curve clients**. Leave **Allow update of true curves** checked. This is in [step 1](../setup/01-build-data.md) now too.

## Pop-up says "Some expressions failed to evaluate"

Field Maps shows **Unable to Load All Data** and a **View Errors** row where an Arcade element should be. The rest of the pop-up still loads.

### 1. Read the exact error

- **In Field Maps:** tap **View Errors**. It lists each failed expression by name with its message. Take a screenshot.
- **In Map Viewer (faster to fix):** open the pop-up, click the failing expression to open the Arcade editor, and click **Run**. The error and its line number appear under the code. Run tests against the first feature in the layer, so pick a hydrant that has inspections if the error is about related records.

### 2. Match it to the cause

| Message mentions | Cause | Fix |
|---|---|---|
| A field name, "field not found", or an invalid SQL / order-by | Field names were lower-cased when you published (`InspDate` became `inspdate`). Field lists and sort strings in quotes must match exactly | Use the lower-case Arcade in [step 4](../setup/04-popups.md) and [step 5](../setup/05-field-maps-form.md) |
| The relationship, or "invalid relationship name" | The relationship has a different name on the service | In the Arcade editor open **Profile variables > $feature**, find the related records entry, and paste its name into `var rel = ...` |
| A table or layer not found | The inspections table isn't in the web map, or editing/query is off for it in the view | Add the field view's HydrantInspections table to the map (step 3) |

### 3. Check it worked

Close and reopen the map in Field Maps (pull down on the map list to refresh) so it picks up the saved pop-up, then tap hydrant 0291. With the demo inspections loaded, the banner should be green ("OK").
