# Hydrant inspection pilot: Field Maps vs Survey123

**Purpose.** Have SFFD crews try the same hydrant inspections in both apps, then pick one app to build out. The pilot answers three questions:

1. Which app can crews use quickly and correctly, without help?
2. Which app gives cleaner data (right values, and each inspection tied to its hydrant)?
3. Which app is easier for SFPUC to run: accounts, licensing, offline, upkeep?

**Format.** One session per tester, about 70 minutes, at a fire station table, using the tester's own work phone. Testers don't go to real hydrants. Each task comes on a printed card that says what the crew "sees" at the hydrant, so every tester enters the same answers and we can check them. (The sample hydrant points are estimated, so a street test would measure GPS error, not the apps.) A short street round on real hydrants can follow once the winner is chosen.

**Files in this folder**

| File | What it is |
|---|---|
| `PILOT-SCRIPT.md` | This guide: roles, setup, the session script and the task cards |
| `pilot-scorecard.xlsx` | Where observers log each task, testers' ratings, the data check and the team's scoring. The Summary sheet adds it all up |
| `answer_key.csv` | The correct values for every task card. Used by the checker and copied into the workbook |
| `check_pilot_records.py` | Compares an export of the inspections table against the answer key and fills in the data check for you |
| `build_scorecard.py` | Rebuilds `pilot-scorecard.xlsx` from the answer key if the tasks change |

## Roles

| Role | Who (suggested) | Does what |
|---|---|---|
| Pilot lead | GIS analyst who built the MVP | Owns the plan, sets up the apps, runs the team scoring, writes the recommendation |
| Facilitator | GIS analyst or SFFD liaison | Runs each session from the script below. Reads the words, doesn't coach |
| Observer | Second GIS staff member | Times each task, logs it in the scorecard, notes where the tester got stuck |
| Portal admin | SFPUC Enterprise admin | Test accounts, group sharing, and the yes/no on public (no sign-in) Survey123 |
| SFFD contact | Battalion or station officer | Picks testers, books station time |
| Data checker | GIS analyst | Exports the inspections after each session and runs the checker |
| Water Dept reviewer | Hydrant maintenance lead | Joins the team scoring: is the data what maintenance needs? |

## Who tests

- **6 to 8 testers** from at least 2 engine companies. Six is enough to see the big problems; eight evens out the app order.
- Mix them: iPhone and Android, comfortable and less comfortable with apps, and **at least 2 without a portal account**.
- Each tester gets a pilot ID: P1, P2 and so on. Log it on the Testers sheet with their company, phone and account status.

## App order

Everyone uses both apps. Half start with Field Maps and half with Survey123, so neither app gets the "second time is easier" boost. Each app gets a different set of hydrants (Set A or Set B) so testers can't copy their first answers.

| Pilot ID | First | Second |
|---|---|---|
| P1, P5 | Field Maps, Set A | Survey123, Set B |
| P2, P6 | Survey123, Set A | Field Maps, Set B |
| P3, P7 | Field Maps, Set B | Survey123, Set A |
| P4, P8 | Survey123, Set B | Field Maps, Set A |

## Before the pilot (pilot lead and portal admin)

Do these after BUILD-GUIDE.md steps 1 to 3 and the tap-test.

- [ ] **Clean the inspector list.** `data/inspectors.csv` picked up remark words from the SFFD report when the PDF wrapped lines, such as "Main Size Not Labeled Adams,E" and "Excessive Rust McGorrin,B". Roughly 70 of the 493 rows look like this. Fix them, then re-run `build_xlsform.py` and rebuild the domain, or testers will see junk in the Inspector list.
- [ ] **Accounts.** One test account per tester who has none for Field Maps, sharing the MVP group. Field Maps editing needs a user type that can edit (Contributor or Mobile Worker; **check** what the 11.5 portal licenses allow). Write down the licensing cost per crew member for the team scoring.
- [ ] **Public survey.** Ask the portal admin whether the survey can be shared with everyone (no sign-in). If not, the no-account tests (task 6) use a test account and the scoring notes that public access wasn't possible.
- [ ] **Phones.** On each tester's phone (or a loaner): install ArcGIS Field Maps and ArcGIS Survey123, sign in, download the survey in Survey123, and confirm the pop-up link opens Survey123 with the hydrant filled in. Leave the Field Maps offline area **not** downloaded; task 5 covers that.
- [ ] **Reset the data.** Delete practice inspections so only pilot records are in the table.
- [ ] **Print** the task cards below: one Set A and one Set B packet per tester. Print the Observer sheet from the workbook.
- [ ] **Dry run** the whole session once with a GIS colleague. Fix anything that breaks before the first crew sees it.

## Session script (facilitator)

Read the words in quotes as written. If the tester asks for help, say "What would you try if I weren't here?" Help only after about 2 minutes stuck, and the observer marks it "With help".

### 1. Welcome (5 min)

> "Thanks for doing this. We're testing two apps for hydrant inspections, not you. If something's confusing, that's what we need to know. Please think out loud as you go.
>
> Each card describes a hydrant as if you're standing at it. Enter what the card says. Start every Remarks entry with your pilot ID, like **P3**, so we can find your records afterward.
>
> We'll time each task, but there's no rush. Work like you would on a normal shift."

### 2. First app (about 20 min)

Hand over the first card packet. For each card, the observer starts the timer when the tester reads the card and stops it when the tester submits or gives up. After each task, ask:

> "On a scale of 1 to 7, how easy was that? 1 is very hard, 7 is very easy."

Survey123 sessions do task 6 after task 5. Field Maps sessions skip task 6.

### 3. After the first app (5 min)

Ask the four after-app questions (on the After-app sheet), 1 is strongly disagree, 5 is strongly agree:

1. "I could do a real inspection with this app without help."
2. "It's quick enough to use on a busy shift."
3. "Buttons and text were easy to use one-handed, and outdoors."
4. "I trust that what I entered was saved correctly."

Then: "What was the most frustrating part?"

### 4. Second app (about 20 min) and its questions (5 min)

Same as steps 2 and 3, with the second card packet.

### 5. Wrap-up (5 min)

> "If you had to use one of these every inspection season, which would you pick, and why?
> Is there anything from the paper process that neither app handled?"

Thank them. The data checker exports the table before the next tester starts.

## Observer notes

For each task, log on the Tasks sheet:

- **Time** in minutes (1.5 = one and a half minutes).
- **Result:** Alone (done without help), With help, or Failed (gave up or submitted the wrong hydrant).
- **Ease** 1 to 7, from the tester.
- **Notes:** where they hesitated, mis-taps, scrolling hunts, anything they said out loud. Watch especially for: finding the hydrant, the Inspector list, switches vs. tap lists, the photo step, and whether they noticed Low Pressure and Follow-up filling in by themselves.

## After each session (data checker)

1. In ArcGIS Pro, run **Table To Table** (or Export Table) on the HydrantInspections table to a CSV. Keep the field names, not aliases. If you want photos checked too, add a `PhotoCount` column with each record's attachment count; otherwise the observer notes photos.
2. Run `python check_pilot_records.py export.csv --out data_check.csv` and paste the result into the Data check sheet. For each pilot record it lists the tester, task, set and app, whether the record is tied to its hydrant, and every field that differs from the answer key. It finds the tester from the pilot ID at the start of Remarks and the app from the App order table above, so the order must be followed.
3. Spot-check one or two records by hand the first time to make sure the export matches what's on the phone.

## Team scoring (pilot lead, portal admin, Water Dept reviewer)

After the last session, the team fills in the Team criteria sheet together, scoring each app 1 to 5 on things crews can't judge: accounts and licensing cost, data tied to hydrants, offline, upkeep of the form and inspector list, the dashboard, and the later Maximo link through FME Flow. Weights are pre-filled and can be changed before scoring starts (agree on them first, not after seeing the numbers).

## How we decide

The Summary sheet shows both apps side by side. Before comparing totals, each app must pass these:

| Must pass | Why |
|---|---|
| 80% or more of tasks done **alone** | Crews will be on their own in the field |
| 95% or more of records tied to the right hydrant | An inspection that isn't under its hydrant is lost to maintenance |
| The offline task (task 5) synced for every tester | Some hydrants have poor signal |

If both pass, pick the one with the higher combined score (crew results and team scoring weigh equally). If they're within 10% of each other, account access decides: if crews without accounts can't use Field Maps and the portal can't fund accounts for them, choose Survey123; otherwise choose Field Maps for its full offline map and simpler upkeep.

## Known differences to watch

These come from the build, and the pilot should show how much each matters:

- **Accounts.** Field Maps always needs a sign-in. Survey123 can skip it, but only if the portal allows public sharing.
- **No-account crews lose the map.** Without a sign-in they can't open the Field Maps map, so they open Survey123 directly and type the GIS ID. Those records arrive with no link to the hydrant (empty `HydrantGUID`). Task 6 measures this. If Survey123 wins on accounts, a nightly FME or Python job that matches GIS ID to hydrant would close the gap.
- **Inspector list.** Survey123 filters names by engine company; Field Maps shows one long searchable list.
- **Issue checklist.** Survey123 uses tap lists; Field Maps uses one switch per issue.
- **Follow-up flag.** Both set it automatically. Crews can change it in Survey123, not in Field Maps.
- **Photos.** Survey123 requires one when follow-up is needed; Field Maps doesn't force it.

---

## Task cards

Print each set on its own pages, one card per half page. The **[Field Maps]** and **[Survey123]** lines tell the tester how to start; everything else is the same in both apps.

### Set A

**Card A1. Routine check**
Hydrant **0291**, south side of Geary St, 33 ft west of Kearny St.
[Field Maps] Find the hydrant on the map and add an inspection. [Survey123] Find the hydrant on the map, tap it, and open the inspection link.
Enter today's date, your engine company and your name.
The hydrant is there and works fine. No corrosion. Gauge reads **70 psi**. Spindle is stamped **62**. All caps on, shutoff valve OK, nothing in the way, all markings readable.
Remarks: your pilot ID only.

**Card A2. Low pressure, missing cap**
Hydrant **0490**, NW corner of Ellis St and Powell St.
Works fine. Corrosion on the bonnet. Gauge reads **40 psi**. Spindle stamped **55**. **One cap missing.** Shutoff valve OK, nothing in the way, markings readable.
Take a photo (photograph this card). Remarks: pilot ID, then "Cap missing on side outlet".

**Card A3. Several problems**
Hydrant **3641**, NW corner of Mission St and New Montgomery St.
It opens, but only with a cheater bar (**limited**, hard to operate). No corrosion. Gauge reads **90 psi**. Spindle stamped **88**. All caps on. **Shutoff valve is paved over.** Nothing in the way. **Main size isn't labeled.** **Leaking at the bonnet.**
Take a photo. Remarks: pilot ID, then "Leak at bonnet".

**Card A4. Hydrant not there**
Hydrant **0718**, SE corner of Jones St and Geary St.
There is **no hydrant** at this corner.
Take a photo (this card). Remarks: pilot ID, then "No hydrant at indicated location".

**Card A5. No signal**
Hydrant **3466**, NW corner of 6th St and Stevenson St.
[Field Maps] First download the map for offline use. [Both] Turn on airplane mode, then do the inspection.
Works fine. No corrosion. Gauge **62 psi**. Spindle stamped **60**. All caps on, shutoff OK, markings readable. **A car is parked in front of it** (obstructed).
Take a photo. Remarks: pilot ID, then "Car blocking hydrant".
Then turn airplane mode off and send or sync the inspection.

**Card A6. Survey123 only: no account**
Hydrant **3803**, NW corner of Howard St and 5th St.
Pretend you have no SFPUC account. Open the survey from the link on this card (or the QR code) instead of the map, and **type the GIS ID yourself**.
Works fine. No corrosion. Gauge **55 psi**. Spindle stamped **50**. All caps on, shutoff OK, nothing in the way, markings readable.
Remarks: pilot ID only.
Survey link: ______________________ (pilot lead fills in)

### Set B

**Card B1. Routine check**
Hydrant **0353**, SE corner of Grant Ave and Geary St.
[Field Maps] Find the hydrant on the map and add an inspection. [Survey123] Find the hydrant on the map, tap it, and open the inspection link.
Enter today's date, your engine company and your name.
The hydrant is there and works fine. No corrosion. Gauge reads **68 psi**. Spindle is stamped **60**. All caps on, shutoff valve OK, nothing in the way, all markings readable.
Remarks: your pilot ID only.

**Card B2. Low pressure, missing cap**
Hydrant **0564**, SE corner of Eddy St and Mason St.
Works fine. Corrosion on the bonnet. Gauge reads **35 psi**. Spindle stamped **50**. **One cap missing.** Shutoff valve OK, nothing in the way, markings readable.
Take a photo (photograph this card). Remarks: pilot ID, then "Cap missing on side outlet".

**Card B3. Several problems**
Hydrant **3402**, SE corner of New Montgomery St and Minna St.
It opens, but only with a cheater bar (**limited**, hard to operate). No corrosion. Gauge reads **70 psi**. Spindle stamped **65**. All caps on. **Shutoff valve is paved over.** Nothing in the way. **Main size isn't labeled.** **Leaking at the bonnet.**
Take a photo. Remarks: pilot ID, then "Leak at bonnet".

**Card B4. Hydrant not there**
Hydrant **0570**, NW corner of O'Farrell St and Mason St.
There is **no hydrant** at this corner.
Take a photo (this card). Remarks: pilot ID, then "No hydrant at indicated location".

**Card B5. No signal**
Hydrant **3467**, NW corner of 6th St and Jessie St.
[Field Maps] First download the map for offline use. [Both] Turn on airplane mode, then do the inspection.
Works fine. No corrosion. Gauge **58 psi**. Spindle stamped **55**. All caps on, shutoff OK, markings readable. **A car is parked in front of it** (obstructed).
Take a photo. Remarks: pilot ID, then "Car blocking hydrant".
Then turn airplane mode off and send or sync the inspection.

**Card B6. Survey123 only: no account**
Hydrant **3808**, NW corner of Howard St and 7th St.
Pretend you have no SFPUC account. Open the survey from the link on this card (or the QR code) instead of the map, and **type the GIS ID yourself**.
Works fine. No corrosion. Gauge **54 psi**. Spindle stamped **50**. All caps on, shutoff OK, nothing in the way, markings readable.
Remarks: pilot ID only.
Survey link: ______________________ (pilot lead fills in)
