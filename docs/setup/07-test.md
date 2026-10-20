# 7. Test before the pilot

**Who:** GIS analyst · **You need:** a crew test account (not yours), a real phone · **Done when:** every box below is ticked

## Both apps write to one place

- [ ] Do a test inspection of the same hydrant in each app. Both records show up under that hydrant in Map Viewer.

## Field Maps, with a crew test account, on a phone

- [ ] The map opens and shows hydrants and their past inspections.
- [ ] You can add an inspection from a hydrant, and its GIS ID and location fill in.
- [ ] You can't edit or move a hydrant, and there's no option to add one.
- [ ] You can fix an inspection you just added, but not one someone else added.
- [ ] Take the map offline, add an inspection, sync. It shows up in the source.

## Survey123 without signing in (only if you made the public view)

Use a private browser window.

- [ ] The survey opens from its link and submits.
- [ ] The public view's URL doesn't return any records. Open `.../FeatureServer/1/query?where=1=1&f=json`; it should be empty or refused.
- [ ] The source and field view URLs ask for a sign-in.

## Pop-ups and form on a phone, with the demo data

Load the [demo inspections](04-popups.md#load-demo-inspections) first. Save the web map in Map Viewer before each test, then reopen the map in Field Maps (pull down on the map list to refresh), or the phone keeps the old pop-up.

**Hydrant banners.** Tap each hydrant:

- [ ] **0353:** gray, "Not inspected yet"
- [ ] **0291:** green, "OK", 2 inspections
- [ ] **0383:** yellow, "Inspection due"
- [ ] **0358:** red, "Needs SFPUC follow-up"
- [ ] **0718:** red, "Not found at location"
- [ ] Banner and title read without zooming, one-handed.

**Inspection pop-up.** Tap an inspection under the hydrant:

- [ ] **0358:** the title shows date and company, the pressure line reads *38 psi measured · 50 psi stamped · LOW*, and Issues found lists Low pressure.
- [ ] **3402:** Issues found shows "Operable: No" and "Stripped spindle".
- [ ] **0291:** Issues found says "None".
- [ ] Related inspections are listed newest first, each titled with date and company.
- [ ] Photos open from the inspection pop-up (add one by hand; demo records have none).

**New inspection from the form.** Open 0291 and add an inspection:

- [ ] GIS ID, Location, Latitude and Longitude fill in by themselves. If one stays blank, check the layer name in its expression ([step 5b](05-field-maps-form.md#5b-calculated-fields)).
- [ ] Switching Found at Location to No hides the Condition, Markings and Other issues groups.
- [ ] A gauge of 40 (stamped is 62) sets Low Pressure and Needs Follow-up to Yes.
- [ ] After you submit, 0291's banner turns red and the new inspection is at the top of its list.
- [ ] Start the test record's Remarks with `DEMO.` so `--remove` clears it, or delete it in the source.

**Before the pilot:**

- [ ] All of the above also work with the map taken offline.
- [ ] Demo inspections are removed (`--remove`).

## Tap-test

- [ ] Search sits at the top and finds a hydrant by GIS ID.
- [ ] Buttons and switches are at least 44 px and easy to hit with one thumb.
- [ ] The "Inspect in Survey123" link opens Survey123 with the hydrant filled in.

## Next

[8. Run the staff pilot](08-pilot.md). A supervisor dashboard (low-pressure list, follow-up count, inspections by company) can come after, built on the same table.
