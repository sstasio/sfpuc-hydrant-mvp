# 3. Build the web map

**Who:** GIS analyst · **You need:** the field view from step 2 · **Done when:** `Hydrant Inspections MVP` is saved and shared with the MVP test group

Field Maps uses this map. Build it on the **field view**, never the source.

1. **Map Viewer > Add > Browse layers**, add `Hydrant Inspections Field`. Hydrants and the inspections table come in together.
2. **Basemap**: a light street basemap that can go offline, so blue hydrant points stand out and Field Maps can download it. The gallery basemaps can't go offline; use `SF Basemap (offline)` from [Offline basemap](../reference/offline-basemap.md).
3. **Hydrants layer**:
    - Symbol: simple water blue `#007DC3` points, sized for a thumb (about 12 px).
    - **Turn off editing for this layer in the map** (layer properties, **Enable editing** off), so Field Maps doesn't offer crews an "add hydrant" button. The view's ownership rule still blocks edits underneath.
    - Pop-ups: set up in the next step.
4. **HydrantInspections table**: editing on.
5. **Map properties**: set **search** on Hydrants by GIS ID, so crews can type the stamped serial at the top of the screen.
6. **Save** as `Hydrant Inspections MVP` and share it with the MVP test group (the same group as the field view).

> **Note:** the Arcade in the next steps finds related records by GlobalID (`Filter(FeatureSetByName(...))`), not by relationship name, because the relationship name on the published view didn't match. It needs the inspections table's name as it shows in this map's Layers list (on the SFPUC portal: "Hydrant Inspections Field - HydrantInspections").

## Next

[4. Set up pop-ups](04-popups.md)
