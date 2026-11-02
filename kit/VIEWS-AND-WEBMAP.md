# Hydrant inspection MVP: views and web map

Crews never touch the published layer directly. They edit through **views**: saved windows onto the same data, each with its own sharing and editing rules. Every view writes straight into the source, so there is nothing to sync or copy.

Target: ArcGIS Enterprise 11.5 (https://gis.sfpuc.org/portal). Written without portal access, so check each step in the UI as you go. Notes marked **check** are things I couldn't confirm for 11.5.

## The setup at a glance

| Item | Who sees it | Editing | Used by |
|---|---|---|---|
| **Source**: the hosted layer you published (Hydrants + HydrantInspections) | Owner and GIS team only | Full (owner) | GIS team, pilot data check, dashboard later |
| **Field view**: `Hydrant Inspections Field` | MVP test group | Add and update, crews can only edit records they created | Field Maps web map |
| **Public view**: `Hydrant Inspections Public` (optional) | Everyone | Add only, can't see any records | Survey123 form |

What this gets you:

- **Hydrants stay yours.** Crews can see hydrants but not move, change or delete them.
- **Inspections are add-only for crews**, plus fixing their own records in Field Maps.
- **The public can submit but can't browse.** Nobody without a sign-in can read inspections, inspector names or remarks.
- **The pilot and dashboard keep working.** They read the source, which holds every record from both apps.

## 1. Lock down the source

On the source item's page:

1. **Share**: owner only, or a GIS team group. Remove it from the MVP test group if you shared it there in build guide step 1.
2. **Settings > Feature Layer (hosted)**: leave **Enable editing** and **Enable Sync** on as published. Only the owner and admins can reach it now, and views need sync on the source to offer offline.
3. Turn off **Allow others to export to different formats**.

## Fields in each view

Keep **all fields** in both views.

- **Field view:** the Field Maps form and its Arcade read hydrant fields and fill several inspection fields automatically, so every field must be there. Hydrants are read-only through the ownership rule, not by hiding fields.
- **Public view:** the survey writes nearly every inspection field. A missing field makes submissions fail or lose that value. Privacy comes from "Editors can't see any features", not from hiding fields.
- ObjectID, GlobalID and the editor tracking fields can't be removed from a view anyway.

## 2. Create the field view

1. On the source item page, **Create View Layer** (the 11.5 label may read **Create Hosted Feature Layer View**). Name it `Hydrant Inspections Field`.
2. Keep **both** Hydrants and HydrantInspections in the view. The relationship comes with them, which Field Maps needs to show a hydrant's inspections and to fill hydrant details into the form.
3. No filters or area of interest for now. (Different areas per layer would block sync.)
4. On the view's **Settings > Feature Layer (hosted, view)**:
   - **Enable editing**: on.
   - **What kind of editing is allowed**: **Add** and **Update** (Attributes only). Delete off.
   - **What features can editors see**: **Editors can see all features**. Crews need to see past inspections at a hydrant.
   - **What features can editors edit**: **Editors can only edit their own features**. This is what keeps hydrants read-only: you created every hydrant, so to crews they all belong to someone else. It uses the `created_user` field that `build_hydrant_gdb.py` already turns on.
   - **Enable Sync**: on, for offline maps.
   - **Allow others to export**: off.
5. **Share** the view with the MVP test group.
6. **Test with a crew test account** before the pilot (see step 6). The settings above apply to the whole view, not per layer, so the "own features only" rule is what protects hydrants. If `created_user` on your hydrants is blank, that protection may not hold.

**check**: whether 11.5 allows different editing rules per layer in one view through the item page. If it does, set Hydrants to no editing outright and skip relying on ownership.

## 3. Create the public view (optional)

Only if the portal admin allows public sharing (see pilot script setup). Skip it otherwise and point Survey123 at the field view (step 5).

1. From the source item, **Create View Layer** again. Name it `Hydrant Inspections Public`.
2. Include **only HydrantInspections**. Leave Hydrants out so hydrant locations aren't published to everyone. The form gets the hydrant's GlobalID, GIS ID and location from the pop-up link instead.
   **check** that the table keeps its layer ID (1) in the view, since the form looks it up by name (`form_id` = `HydrantInspections`).
3. **Settings**:
   - **Enable editing**: on, **Add** only. If Add is greyed out, check that Add is on in the **source** layer's settings, because a view can't allow more than its source.
   - **What features can editors see**: **Editors can't see any features** (the 11.5 wording may add "even those they add").
   - **Enable Sync**: off. **Allow others to export**: off.
4. **Share** with **Everyone**. The source and field view stay private.

## 4. Build the web map for Field Maps

This replaces build guide step 2.1, which built the map from the source.

1. **Map Viewer > Add > Browse layers**, add `Hydrant Inspections Field`. Hydrants and the inspections table come in together.
2. **Basemap**: a light street basemap, so blue hydrant points stand out.
3. **Hydrants layer**:
   - Symbol: simple water blue `#007DC3` points, sized for a thumb (about 12 px).
   - **Turn off editing for this layer in the map** (layer properties, **Enable editing** off), so Field Maps doesn't offer crews an "add hydrant" button. The view's ownership rule still blocks edits underneath.
   - Pop-up: set it up exactly as in `FIELD-MAPS-POPUPS.md` (hydrant and inspection pop-ups).
4. **HydrantInspections table**: editing on.
5. **Map properties**: set **search** on Hydrants by GIS ID, so crews can type the stamped serial at the top of the screen.
6. **Save** as `Hydrant Inspections MVP` and share it with the MVP test group (same group as the field view).
7. Then carry on with build guide step 2.3 (the Field Maps form) and 2.4 (offline areas) on this map.

**check**: the Field Maps form expressions in `field-maps-arcade.md` use `FeatureSetByRelationshipName`. Views normally keep the relationship name `Hydrants_HydrantInspections`; confirm it in the Arcade editor's profile variables.

## 5. Point Survey123 at a view

One survey, two possible targets:

| If public sharing is allowed | If it isn't |
|---|---|
| Publish against **Hydrant Inspections Public** and share the survey with Everyone | Publish against **Hydrant Inspections Field** and share the survey with the MVP test group |

Steps in Survey123 Connect (replaces build guide step 3.1):

1. **New Survey > Feature service**, and pick the **view**, not the source. Then paste in the survey, choices and settings rows from `survey123/HydrantInspection.xlsx`.
2. Or open the file directly and set `submission_url` on the settings sheet to the view's URL, ending at `FeatureServer` (no layer number). `form_id` stays `HydrantInspections`.
3. Publish, then paste the survey's item ID into the pop-up link in `field-maps-arcade.md`. The link itself doesn't change: it points at the survey, and the survey knows which view to write to.

Trade-off to note for the pilot scoring: records sent through the public view have no SFPUC user in `created_user`, so nobody can fix them later from the app. The Inspector pick list still records who did the inspection, and the GIS team can correct records in the source.

## 6. Test before the pilot

With a **crew test account** (not yours), in Field Maps on a phone:

- [ ] The map opens and shows hydrants and their past inspections.
- [ ] You can add an inspection from a hydrant, and its GIS ID and location fill in.
- [ ] You can't edit or move a hydrant, and there's no option to add one.
- [ ] You can fix an inspection you just added, but not one someone else added.
- [ ] Take the map offline, add an inspection, sync. It shows up in the source.

Without signing in (private browser window), if you made the public view:

- [ ] The survey opens from its link and submits.
- [ ] The public view's URL doesn't return any records (open `.../FeatureServer/1/query?where=1=1&f=json`; it should be empty or refused).
- [ ] The source and field view URLs ask for a sign-in.

## Changes to the rest of the kit

Already made in this kit:

- `BUILD-GUIDE.md` steps 1.3, 2.1, 3.1 and 3.3 now point here.

No change needed:

- `survey123/HydrantInspection.xlsx`: `submission_url` is blank on purpose. Fill it with the view URL in Connect (step 5).
- `field-maps-arcade.md`: the pop-up link points at the survey's item ID, not a layer, so it works with either view. The relationship name carries over to the field view.
- `pilot/check_pilot_records.py`: export the inspections table from the **source**, which holds records from both views.

## 11.5 docs

I couldn't open Esri's site from here, so these are the 11.5 pages by their standard paths; labels above come from those pages' search excerpts and may differ slightly in your UI.

- [Create hosted feature layer views](https://enterprise.arcgis.com/en/portal/11.5/use/create-hosted-views.htm)
- [Edit a hosted feature layer view definition](https://enterprise.arcgis.com/en/portal/11.5/use/set-view-definition.htm)
- [Manage hosted feature layer editing](https://enterprise.arcgis.com/en/portal/11.5/use/manage-editing-hfl.htm)
- [Data access and editing](https://enterprise.arcgis.com/en/portal/11.5/use/data-access-and-editing.htm)
- [Use Survey123 with ArcGIS Enterprise](https://doc.arcgis.com/en/survey123/get-started/survey123withenterprise.htm)
