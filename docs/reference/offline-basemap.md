# Offline basemap

**Who:** GIS analyst (AGOL admin for option A's account) · **Used in:** [step 3](../setup/03-web-map.md) (pick the basemap) and [step 5d](../setup/05-field-maps-form.md#5d-offline) (offline area) · **Done when:** Field Maps downloads the map with a basemap, and the basemap still shows in airplane mode

## Why the usual basemaps don't work

Field Maps can only take a map offline if **every** layer in it can go offline, basemap included. The Esri basemaps that come with the Enterprise basemap gallery **can't be taken offline**, so a map built on them fails the offline check or downloads without a basemap.

Two ways around it:

| | A. Esri basemap "for Export" (recommended for the pilot) | B. Your own tile package (later, citywide) |
|---|---|---|
| What it is | An offline-ready copy of an Esri basemap from ArcGIS Online, added to the portal as an item | A `.vtpk` (vector) or `.tpkx` (raster) file of San Francisco you make in ArcGIS Pro |
| Looks like | Esri's street basemap, same as crews are used to | Whatever you put in it (streets, parcels, buildings, city labels) |
| Needs | An ArcGIS Online **organizational** account (SFPUC already uses AGOL) | ArcGIS Pro 3.7.3 and city base layers |
| How it reaches the phone | Downloaded with each offline area | Uploaded to the portal once; each phone downloads it once, then only the hydrant data downloads |
| Upkeep | None, Esri keeps it current | Rebuild when the city layers change |
| Best for | A small pilot area, set up in under an hour | Many crews, the whole city, or if AGOL credentials can't be stored on the portal |

**Recommendation:** use **A** for the pilot. It's the least work, it looks like a normal basemap, and the pilot area is a handful of blocks. Move to **B** if the app goes citywide.

## A. Esri basemap "for Export" (recommended)

Esri publishes export-enabled copies of its basemaps on ArcGIS Online. Their titles end in **(for Export)**. The Enterprise-supported way to use one is to add it to the portal as an item **with its ArcGIS Online sign-in stored**. Adding it straight into Map Viewer from ArcGIS Online is a known failure (Esri BUG-000138987, "not a supported workflow").

### A1. Get the service address (ArcGIS Online)

1. Sign in to SFPUC's **ArcGIS Online** org. Use a shared service account if the AGOL admin has one, since its sign-in will be stored on the portal.
2. Search ArcGIS Online (outside your org) for `for Export` and open **World Street Map (for Export)**. A light gray one also works if you want blue hydrants to stand out more.

    > **Check:** the exact titles. Pick a **vector** tile layer if there's one with the same look, since vector downloads are much smaller than raster.

3. On the item page, copy the **URL** (bottom right). It ends in `/VectorTileServer` or `/MapServer`.

### A2. Add it to the portal (Enterprise 11.5)

1. **Content > New item > URL**, paste the address.
2. Type: **Vector tile layer** (or **Tile layer** for a `/MapServer` address).
3. Tick **Store credentials with service item. Do not prompt for authentication.** Enter the AGOL account from A1.
4. Title it `SF Basemap (offline)`, tag it `Hydrant MVP`, save.
5. Share it with the **MVP test group**, the same group as the field view and web map.

> **Check in 11.5:** the label of the stored-credentials option and whether the item's **Settings** tab shows an **Offline** switch for it. If there's a switch, turn it on.

### A3. Use it in the web map

1. Open `Hydrant Inspections MVP` in **Map Viewer**. **Add > Browse layers > My content**, add `SF Basemap (offline)`.
2. On the new layer's **...** menu, choose **Move to basemap**. Remove the old gallery basemap layer so this is the only basemap layer.
3. **Save**.
4. On the web map's item page, **Settings > Offline**: turn on **Enable offline mode** and fix anything it lists.

Then build the offline area in [step 5d](../setup/05-field-maps-form.md#5d-offline).

## B. Your own tile package (citywide)

1. In **ArcGIS Pro 3.7.3**, make a map with the city base layers crews need: street centerlines with names, block or parcel lines, building footprints, and water bodies. Keep it plain and light gray so hydrants stand out. Set the map to Web Mercator (WKID 3857) so it lines up with Field Maps' tiling.
2. Run **Create Vector Tile Package** (`.vtpk`). Extent: San Francisco. Leave the scale range at the defaults; vector tiles stay small even at street level. Use **Create Map Tile Package** (`.tpkx`) only if you need imagery.
3. Share the package to the portal (**Share > Share As > Share Vector Tile Package**, or upload the file). Share it with the MVP test group.
4. **Field Maps Designer > Offline > Offline basemap**: choose to use a basemap on the device and pick the package.
5. On each phone, Field Maps downloads the package once. After that, offline areas only download the hydrants and inspections. For managed phones, the file can also be copied to the device (Files app on iOS, device storage on Android).

> **Check in 11.5:** the exact wording of the offline basemap option in Field Maps Designer. Esri documents it as "specify a tile package for the offline basemap" (Enterprise 10.7 or later).

## Setting up the offline area (step 5d)

Whichever option you pick:

1. **Field Maps Designer > open the map > Offline**. Fix anything the readiness check flags (sync on the field view, offline mode on the map).
2. **Add map area**. Draw a box around the pilot hydrants with a block of margin. Name it `E01 pilot area`.
3. **Level of detail**: from the citywide view down to the closest street level. Option A downloads these tiles with the area, so a small box keeps it quick. Option B ignores this, since the basemap is already on the phone.
4. **Save**, and wait for the area to finish packaging (a few minutes) before testing.
5. Test on a phone: download the area, turn on airplane mode, pan around the pilot hydrants, add an inspection, then turn airplane mode off and sync.

## If it goes wrong

| What you see | Likely cause |
|---|---|
| Offline check says the basemap can't be taken offline | The map still uses a gallery basemap, or the "for Export" layer was added straight from ArcGIS Online instead of through the portal item (A2) |
| Map area fails to package | The AGOL sign-in stored on the item expired or changed; edit the item and re-enter it |
| Crews get a sign-in prompt for the basemap | Credentials weren't stored on the item, or the item isn't shared with their group |
| Offline map has hydrants but a blank background | Option B package not on the device yet, or the area was drawn outside the package's extent |
