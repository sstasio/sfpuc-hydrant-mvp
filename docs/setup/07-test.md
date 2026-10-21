# 7. Test before the pilot

**Who:** GIS analyst · **You need:** a crew test account (not yours), a real phone · **Done when:** every box below is ticked

## Both apps write to one place

- [ ] Do a test inspection of the same hydrant in each app. Both records show up under that hydrant in Map Viewer.

## Field Maps, with a crew test account, on a phone

- [ ] The map opens and shows hydrants and their past inspections.
- [ ] You can add an inspection from a hydrant, and the form's Hydrant group fills in GIS ID, Location, Latitude and Longitude (needs the form from [step 5](05-field-maps-form.md)). The inspection pop-up doesn't show these; they're on the hydrant.
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

## Field scenarios

Run these as a crew member would, with the crew test account, on a phone, standing at a real or pretend hydrant. Each one uses a hydrant the demo data leaves alone, so the results are easy to spot. Start every Remarks with `DEMO.` so `--remove` clears the records afterwards.

**1. Routine inspection, nothing wrong (Field Maps).** Hydrant **3469**, never inspected.

- [ ] Search finds 3469 by typing `3469`, and its banner is gray.
- [ ] Add an inspection: Engine Company E01, an E01 inspector, found Yes, operable Yes, gauge 60, everything else clean. It submits without a photo.
- [ ] Needs Follow-up stays No, and the banner turns green with "OK" and 1 inspection.

**2. Low pressure with a photo (Survey123 link).** Hydrant **0564**, stamped 50 psi.

- [ ] Tap "Inspect in Survey123". The form opens with GIS ID 0564 and its location filled in.
- [ ] Gauge 42 sets Low Pressure and Needs Follow-up to Yes, and the form won't submit until you add a photo.
- [ ] After it sends, 0564's banner in Field Maps is red, "Needs SFPUC follow-up" (refresh the map if it doesn't change).
- [ ] The inspection pop-up shows the photo and *42 psi measured · 50 psi stamped · LOW*.

**3. Hydrant missing.** Hydrant **3401**, either app.

- [ ] Answer No to found at location. The condition questions disappear, and Needs Follow-up turns Yes by itself.
- [ ] In Survey123, it asks for a photo (of the empty spot) before it submits.
- [ ] The banner turns red, "Not found at location".

**4. Inspector not on the list.**

- [ ] Pick Engine Company E01. The Inspector list shows only E01 names plus Other.
- [ ] Change the company to another engine. Check that the inspector you picked is cleared or flagged, not kept silently under the wrong company.
- [ ] Pick Other, put the name in Remarks, and submit. Other is saved in the record.

**5. Fixing a mistake (Field Maps).**

- [ ] Open the inspection from scenario 1 and change the gauge to 58. The change saves.
- [ ] Open a demo inspection (made by your own account, so it's someone else's to the crew). There's no edit button, or the edit is refused.
- [ ] There's no way to delete any inspection, including your own.

**6. Two companies at one hydrant.** Hydrant **3469** again, a day later.

- [ ] Add a second inspection with a different engine company, an inspection date one day after scenario 1, and Corrosion Yes. Both inspections show under 3469, newest first.
- [ ] The banner follows the newest one: it shows the new date and company and "2 inspections".

**7. No signal (Survey123 only).** The Field Maps offline test waits on the basemap; this one doesn't.

- [ ] Put the phone in airplane mode, open the survey from the Survey123 app for hydrant 0564, and submit. It waits in the Outbox.
- [ ] Turn airplane mode off and send the Outbox. The record arrives once, not twice.

## Edge cases

- [ ] Open the survey from its plain link, not from a hydrant. GIS ID is blank and the form won't submit, and the hint tells you to open it from the pop-up.
- [ ] A gauge of 400 is refused with "Enter 0 to 300 psi". So is a negative number.
- [ ] Caps Missing of 4 is refused. Caps Missing of 1 sets Needs Follow-up to Yes.
- [ ] Gauge equal to the stamped pressure (60 at 3469) leaves Low Pressure at No. A blank gauge also leaves it at No.
- [ ] Turning Needs Follow-up back to No by hand sticks, and the photo is no longer required.
- [ ] A long remark (a few paragraphs) saves without being cut short in the pop-up.
- [ ] Searching `291` without the leading zero either finds 0291 or shows nothing. Note which, since crews will type it both ways.
- [ ] Sign in to Field Maps with an account that isn't in the MVP test group. The map doesn't appear in its list.

## Check the records in the source

After the scenarios, open the **source** layer's inspections table in Map Viewer (as yourself) and look at the new records:

- [ ] Each one sits under the right hydrant, so its `hydrantguid` matches that hydrant's GlobalID.
- [ ] Lat and Lon are in degrees (about 37.78 and -122.40), not large numbers in meters.
- [ ] `created_user` is the crew test account for the Field Maps records, and for Survey123 records sent through the field view.
- [ ] Inspection dates and times match when you did them, not shifted by 7 or 8 hours.
- [ ] The marking and issue fields read Yes or No. Blanks are fine only on the "not found" record.
- [ ] Nothing shows up twice.
- [ ] When you're done, run `--remove`, or delete the `DEMO.` records in the source.

## Next

[8. Run the staff pilot](08-pilot.md). A supervisor dashboard (low-pressure list, follow-up count, inspections by company) can come after, built on the same table.
