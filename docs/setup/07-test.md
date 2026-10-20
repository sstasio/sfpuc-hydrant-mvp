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

## Pop-ups on a phone

- [ ] Hydrant banner color matches the latest inspection for one hydrant in each state. Add test inspections to get red, green and gray; edit a date in the source to get yellow.
- [ ] Banner and title read without zooming, one-handed.
- [ ] Related inspections list shows newest first, each titled with date and company.
- [ ] An inspection with no problems shows "None" under Issues found.
- [ ] Photos open from the inspection pop-up.
- [ ] All of the above also work with the map taken offline.

## Tap-test

- [ ] Search sits at the top and finds a hydrant by GIS ID.
- [ ] Buttons and switches are at least 44 px and easy to hit with one thumb.
- [ ] The "Inspect in Survey123" link opens Survey123 with the hydrant filled in.

## Next

[8. Run the staff pilot](08-pilot.md). A supervisor dashboard (low-pressure list, follow-up count, inspections by company) can come after, built on the same table.
