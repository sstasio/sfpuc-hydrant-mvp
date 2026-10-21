# 2. Lock down the source and create views

**Who:** GIS analyst · **You need:** the layer from step 1 · **Done when:** crews can only reach the data through views

Crews never touch the published layer directly. They edit through **views**: saved windows onto the same data, each with its own sharing and editing rules. Every view writes straight into the source, so there is nothing to sync or copy.

## The setup at a glance

| Item | Who sees it | Editing | Used by |
|---|---|---|---|
| **Source**: the hosted layer you published (Hydrants + HydrantInspections) | Owner and GIS team only | Full (owner) | GIS team, pilot data check, dashboard later |
| **Field view**: `Hydrant Inspections Field` | MVP test group | Add and update; crews can only edit records they created | Field Maps web map and the Survey123 form |

What this gets you:

- **Hydrants stay yours.** Crews can see hydrants but not move, change or delete them.
- **Inspections are add-only for crews**, plus fixing their own records in Field Maps.
- **Everyone signs in.** The portal doesn't allow anonymous access, so there is no public view. Both apps write through the field view.
- **The pilot and dashboard keep working.** They read the source, which holds every record from both apps.

## Fields in each view

Keep **all fields** in the field view. Don't hide any in **Update View**.

- The Field Maps form and its Arcade read hydrant fields and fill several inspection fields automatically, so every field must be there. Hydrants are read-only through the ownership rule, not by hiding fields.
- The survey writes nearly every inspection field. A missing field makes submissions fail or lose that value.
- ObjectID, GlobalID and the editor tracking fields can't be removed from a view anyway.

## 2a. Lock down the source

On the source item's page:

1. **Share**: owner only, or a GIS team group. Remove it from the MVP test group if you shared it there in step 1.
2. **Settings > Feature Layer (hosted)**: leave **Enable editing** and **Enable Sync** on as published. Only the owner and admins can reach it now, and views need sync on the source to offer offline.
3. Turn off **Allow others to export to different formats**.

## 2b. Create the field view

1. On the source item page, **Create View Layer**. The 11.5 label may read **Create Hosted Feature Layer View**. Name it `Hydrant Inspections Field`.
2. Keep **both** Hydrants and HydrantInspections in the view. The relationship comes with them, which Field Maps needs to show a hydrant's inspections and to fill hydrant details into the form.
3. No filters or area of interest for now. Different areas per layer would block sync.
4. On the view's **Settings > Feature Layer (hosted, view)**:

    | Setting | Value | Why |
    |---|---|---|
    | Enable editing | On | |
    | What kind of editing is allowed | **Add** and **Update** (attributes only). Delete off | |
    | What features can editors see | **Editors can see all features** | Crews need to see past inspections at a hydrant |
    | What features can editors edit | **Editors can only edit their own features** | Keeps hydrants read-only: you created every hydrant, so to crews they all belong to someone else. Uses the `created_user` field the script turns on |
    | Enable Sync | On | Offline maps |
    | Allow others to export | Off | |

5. **Share** the view with the MVP test group.
6. **Test with a crew test account** before the pilot ([step 7](07-test.md)). These settings apply to the whole view, not per layer, so the "own features only" rule is what protects hydrants. If `created_user` on your hydrants is blank, that protection may not hold.

> **Check in 11.5:** whether 11.5 allows different editing rules per layer in one view through the item page. If it does, set Hydrants to no editing outright and skip relying on ownership.

## Next

[3. Build the web map](03-web-map.md)
