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

- [ ] **0358**, newest inspection (Sep 30, 2026): the title shows date and engine company, the pressure line reads *38 psi measured · 50 psi stamped · LOW*, and Issues found lists Low pressure. The older one (Sep 15, 2025) reads *52 psi measured · 50 psi stamped* with no issues.
- [ ] **3402:** Issues found shows "Operable: No" and "Stripped spindle".
- [ ] **0291:** Issues found says "None".
- [ ] Related inspections are listed newest first, each titled with date and engine company.
- [ ] Photos open from the inspection pop-up (add one by hand; demo records have none).

**New inspection from the form.** Open 0291 and add an inspection:

- [ ] GIS ID, Location, Latitude and Longitude fill in by themselves. If one stays blank, check the layer name in its expression ([step 5b](05-field-maps-form.md#5b-calculated-fields)).
- [ ] Switching Found at Location to No hides the Condition, Markings and Other issues groups.
- [ ] Entering Spindle 62 and Gauge 40 sets Low Pressure and Needs Follow-up to Yes. Low pressure needs both numbers, since the crew types in the stamped spindle pressure.
- [ ] After you submit, 0291's banner turns red and the new inspection is at the top of its list.
- [ ] Before you submit, you typed `TEST.` at the very start of Remarks, so the record can be deleted later without touching the demo data ([Clean up test records](#clean-up-test-records)).

**Before the pilot:**

- [ ] All of the above also work with the map taken offline.
- [ ] Every test record is deleted (`--remove-tests`). Delete the demo inspections (`--remove`) only after the MVP demo ([Clean up test records](#clean-up-test-records)).

## Tap-test

- [ ] Search sits at the top and finds a hydrant by GIS ID.
- [ ] Buttons and switches are at least 44 px and easy to hit with one thumb.
- [ ] The "Inspect in Survey123" link opens Survey123 with the hydrant filled in.

## Field scenarios

Run these as a crew member would, with the crew test account, on a phone, standing at a real or pretend hydrant. Each one uses a hydrant the demo data leaves alone, so the results are easy to spot. In every inspection you add, type `TEST.` at the very start of Remarks (for example `TEST. Scenario 1`), so it's easy to delete afterwards ([Clean up test records](#clean-up-test-records)).

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
- [ ] Change to another engine company. Check that the inspector you picked is cleared or flagged, not kept silently under the wrong engine company.
- [ ] Pick Other, put the name in Remarks, and submit. Other is saved in the record.

**5. Fixing a mistake (Field Maps).**

- [ ] Open the inspection from scenario 1 and change the gauge to 58. The change saves.
- [ ] Open a demo inspection (made by your own account, so it's someone else's to the crew). There's no edit button, or the edit is refused.
- [ ] There's no way to delete any inspection, including your own.

**6. Two engine companies at one hydrant.** Hydrant **3469** again, a day later.

- [ ] Add a second inspection with a different engine company, an inspection date one day after scenario 1, and Corrosion Yes. Both inspections show under 3469, newest first.
- [ ] The banner follows the newest one: it shows the new date and engine company and "2 inspections".

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

## Survey123 in depth

Field scenarios 2 and 7 cover the basics. This section works through the rest of the survey. Use a phone with the Survey123 app installed and signed in with the crew test account, and the survey downloaded once in the app. In every survey you send, type `TEST.` at the very start of Remarks, as in the field scenarios.

**Opening the survey from the button**

- [ ] The blue "Inspect in Survey123" button shows on every hydrant pop-up.
- [ ] Tapping it opens a new, empty inspection for that hydrant, not the app's survey list.
- [ ] Back in Field Maps, open a different hydrant and tap its button. The form shows the new hydrant, with nothing left over from the last one.
- [ ] On a computer, the button opens the survey in the browser and asks you to sign in.

**Values carried over from the hydrant**

- [ ] **0570** (NW O'FARRELL ST & MASON ST): the location arrives whole, with the apostrophe and the ampersand. Both characters can break a link.
- [ ] **0718**: Spindle Pressure arrives as 115. A value over 100 checks that the number isn't cut short.
- [ ] After sending, the record's `hydrantguid`, `lat` and `lon` match the hydrant (see [Check the records in the source](#check-the-records-in-the-source)).

**The form itself**

- [ ] Inspection Date defaults to now and can be changed.
- [ ] Typing `E1` in Engine Company narrows the list to the engine companies starting with E1.
- [ ] Low Pressure can't be typed into. It only changes from the gauge and spindle values.
- [ ] Ticking "Serial number missing" and "Leak" sets those two flags to Yes on the record, and the other eight to No.
- [ ] Clearing every marking and issue (and with no other problems) sets Needs Follow-up back to No.
- [ ] Two photos send, and both show in the inspection pop-up in Field Maps.
- [ ] The Sent box lists the record by GIS ID and date, for example `0291 2026-10-21`.

**Drafts and sending**

- [ ] Close the app halfway through a form and choose to save it. The form waits in Drafts and opens again with your answers in place.
- [ ] Submitting with a required answer missing (Engine Company, Inspector or Operable) is blocked, and the form jumps to the question.
- [ ] Two forms sent from the Outbox at once both arrive, each under its own hydrant.

**For the pilot scoring**

- [ ] Time one full inspection in each app, from tapping the hydrant to sent, and note both times on the [pilot scorecard](08-pilot.md).

## Check the records in the source

After the scenarios, open the **source** layer's inspections table in Map Viewer (as yourself) and look at the new records:

- [ ] Each one sits under the right hydrant, so its `hydrantguid` matches that hydrant's GlobalID.
- [ ] Lat and Lon are in degrees (about 37.78 and -122.40), not large numbers in meters.
- [ ] `created_user` is the crew test account for the Field Maps records, and for Survey123 records sent through the field view.
- [ ] Inspection dates and times match when you did them, not shifted by 7 or 8 hours.
- [ ] The marking and issue fields read Yes or No. Blanks are fine only on the "not found" record.
- [ ] Nothing shows up twice.
- [ ] When you're done, delete the test records ([Clean up test records](#clean-up-test-records)).

## Clean up test records

There are two kinds of made-up records in the layer, and they're cleaned up at different times:

| Records | Remarks start with | Keep them? | Delete with |
|---|---|---|---|
| The 23 demo inspections from [step 4](04-popups.md#load-demo-inspections) | `DEMO.` | **Yes, through the MVP demo.** They're what shows every banner color. | `--remove`, after the demo and before real inspections start |
| Inspections you add while testing | `TEST.` | No | `--remove-tests`, whenever you finish a round of testing |

**While you test:** in every inspection or survey you add, type `TEST.` at the very start of the Remarks box: capital letters, then a period, then anything you like. For example: `TEST. Scenario 3, leak`. A record that starts any other way, even `Test` or ` TEST.` with a space in front, won't be deleted by the command. Never type `DEMO.` on a test record.

### Delete your test records (keeps the demo data)

Run this after each round of testing. It deletes every inspection whose Remarks starts with `TEST.` and nothing else, so the demo inspections stay.

1. In ArcGIS Pro, sign in to the portal as the owner of the source layer.
2. Copy the **source** layer's service URL, ending in `/FeatureServer`, as in [step 4](04-popups.md#load-demo-inspections). Don't use the field view's URL.
3. Open **Python Command Prompt** (Windows Start > ArcGIS > Python Command Prompt) and run this, with your URL in place of `<source service URL>`:

    ```
    propy "C:\temp\hydrant-mvp\load_demo_inspections.py" --service <source service URL> --remove-tests
    ```

4. It prints `Removed N test inspections`, where N is how many you added.

If it says it can't open the table, run the same thing from the Python window inside Pro, as in [step 4](04-popups.md#load-demo-inspections), with `"--remove-tests"` added to the end of the list.

- [ ] The script printed `Removed` with the number of test records you expected.
- [ ] Hydrants you tested on are back to how they looked before. For example 3469 is gray again, and 0291 is green with its two demo inspections.
- [ ] The demo hydrants still show the colors in the [step 4 table](04-popups.md#load-demo-inspections) (for example 0358 red, 0383 yellow).

### Delete the demo data (after the MVP demo)

Only once the demo is over and before crews enter real inspections, run the same command with `--remove` instead of `--remove-tests`:

```
propy "C:\temp\hydrant-mvp\load_demo_inspections.py" --service <source service URL> --remove
```

It prints `Removed 23 demo inspections`, and every hydrant goes back to **Not inspected yet** (gray).

### A record the commands miss

A test record that doesn't start with `TEST.` exactly has to be deleted by hand. This includes any you labeled `DEMO.` before this page changed. The alternative is to fix its Remarks to start with `TEST.` and run `--remove-tests` again.

1. In ArcGIS Pro, signed in as the owner, add the **source** layer (Map tab > Add Data > Data From Path, paste the source service URL).
2. Right-click the **HydrantInspections** table in the Contents pane and choose **Open**.
3. Find the record by its date, hydrant or Remarks, and click the gray box at the left of its row to select it. Demo records have dates moved to the day they were loaded and Remarks from the demo file, so a record you made today on a hydrant you tested is yours.
4. Right-click the selected row and choose **Delete**. If the **Save** button on the Edit tab lights up, click it to send the change to the portal.

## Next

[8. Run the staff pilot](08-pilot.md). A supervisor dashboard (low-pressure list, follow-up count, inspections by engine company) can come after, built on the same table.
