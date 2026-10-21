"""Check pilot inspection records against the answer key.

Export the HydrantInspections table to CSV (field names, not aliases), then:

    python check_pilot_records.py export.csv --out data_check.csv
    python check_pilot_records.py export.csv --hydrants hydrants.csv --out data_check.csv

--hydrants is an optional export of the Hydrants layer (GISID and GlobalID columns).
With it, the check also confirms each inspection is tied to the *right* hydrant,
not just to some hydrant. If the export has a PhotoCount column, photos are checked too.

Records are matched to testers by the pilot ID ("P3") at the start of Remarks, and
to a task by GIS ID. The app comes from the App order table in PILOT-SCRIPT.md.
Paste the output into the Data check sheet of pilot-scorecard.xlsx.
"""
import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ANSWER_KEY = os.path.join(HERE, "answer_key.csv")

FM, S123 = "Field Maps", "Survey123"
# Order by pilot number: (first app, first set). The second block swaps both.
ORDERS = [(FM, "A"), (S123, "A"), (FM, "B"), (S123, "B")]

# Field Maps switches can save an untouched switch as empty, so treat empty as No here.
FLAG_FIELDS = ["MissSerial", "MissSpindle", "MissMainSize", "MissShutoffDist", "DmgThreads",
               "StrippedSpindle", "Leak", "PaintedOver", "DmgCap", "HardToOperate"]
NUMBER_FIELDS = ["Gauge", "Spindle", "CapsMissing"]
CHECK_FIELDS = (["FoundAtLoc", "Operable", "Corrosion", "Gauge", "Spindle", "LowPressure",
                 "CapsMissing", "ShutoffValve", "Obstructed"] + FLAG_FIELDS + ["NeedsFollowup"])
OUT_FIELDS = ["PilotID", "Task", "Set", "App", "GISID", "Linked", "WrongCount", "WrongFields",
              "ObjectID", "Note"]


def app_for(pilot_num, hydrant_set):
    first_app, first_set = ORDERS[(pilot_num - 1) % 4]
    second_app = S123 if first_app == FM else FM
    return first_app if hydrant_set == first_set else second_app


def norm(field, value):
    value = (value or "").strip()
    if field in NUMBER_FIELDS:
        try:
            return str(int(float(value))) if value else ""
        except ValueError:
            return value
    if field in FLAG_FIELDS and not value:
        return "No"
    return value


# Column names the checks look up. Exports from the portal can have every field name
# lower-cased (gisid, remarks), so headers are matched to these regardless of case.
KNOWN_COLUMNS = (["GISID", "GlobalID", "HydrantGUID", "Remarks", "OBJECTID", "PhotoCount"]
                 + CHECK_FIELDS)


def read_csv(path):
    canonical = {c.lower(): c for c in KNOWN_COLUMNS}
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [{canonical.get(k.lower(), k): v for k, v in r.items()} for r in csv.DictReader(f)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", help="CSV export of the HydrantInspections table")
    ap.add_argument("--hydrants", help="optional CSV export of the Hydrants layer (GISID, GlobalID)")
    ap.add_argument("--out", default="data_check.csv")
    args = ap.parse_args()

    key = {r["GISID"]: r for r in read_csv(ANSWER_KEY)}
    guid_by_gisid = {}
    if args.hydrants:
        guid_by_gisid = {r["GISID"].strip(): r["GlobalID"].strip("{} ").lower()
                         for r in read_csv(args.hydrants)}

    records = read_csv(args.export)
    out, seen = [], {}
    for rec in records:
        m = re.match(r"\s*P(\d+)\b", rec.get("Remarks") or "", re.I)
        gisid = (rec.get("GISID") or "").strip()
        oid = rec.get("OBJECTID") or ""
        if not m:
            continue  # not a pilot record
        pnum = int(m.group(1))
        exp = key.get(gisid)
        if exp is None:
            out.append({"PilotID": f"P{pnum}", "GISID": gisid, "ObjectID": oid,
                        "Note": "GIS ID isn't on any task card (typo or wrong hydrant)", "WrongCount": ""})
            continue

        guid = (rec.get("HydrantGUID") or "").strip("{} ").lower()
        if not guid:
            linked = "No"
        elif guid_by_gisid and guid_by_gisid.get(gisid) != guid:
            linked = "Wrong hydrant"
        else:
            linked = "Yes"

        found_no = exp["FoundAtLoc"] == "No"
        wrong = []
        for f in CHECK_FIELDS:
            want = exp.get(f, "")
            if want == "" and not found_no:
                continue
            if found_no and f != "FoundAtLoc" and f != "NeedsFollowup":
                continue  # condition questions are hidden when the hydrant isn't there
            got = norm(f, rec.get(f))
            if got != norm(f, want):
                wrong.append(f"{f}: {got or '(empty)'} (want {want})")
        if "PhotoCount" in rec and exp["MinPhotos"]:
            photos = int(float(rec["PhotoCount"] or 0))
            if photos < int(exp["MinPhotos"]):
                wrong.append(f"Photos: {photos} (want {exp['MinPhotos']}+)")

        row = {"PilotID": f"P{pnum}", "Task": exp["Task"], "Set": exp["Set"],
               "App": app_for(pnum, exp["Set"]), "GISID": gisid, "Linked": linked,
               "WrongCount": len(wrong), "WrongFields": "; ".join(wrong), "ObjectID": oid, "Note": ""}
        dup = (pnum, gisid)
        if dup in seen:
            row["Note"] = "Duplicate: tester submitted this hydrant more than once"
            seen[dup]["Note"] = row["Note"]
        seen[dup] = row
        out.append(row)

    # Tasks a tester never submitted
    for pnum in sorted({p for p, _ in seen}):
        for gisid, exp in key.items():
            app = app_for(pnum, exp["Set"])
            if (pnum, gisid) not in seen:
                out.append({"PilotID": f"P{pnum}", "Task": exp["Task"], "Set": exp["Set"], "App": app,
                            "GISID": gisid, "Linked": "", "WrongCount": "", "WrongFields": "",
                            "ObjectID": "", "Note": "Missing: no record found"})

    out.sort(key=lambda r: (int(r["PilotID"][1:]), r.get("App", ""), r.get("Task", "")))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        w.writeheader()
        w.writerows(out)

    checked = [r for r in out if r["WrongCount"] != ""]
    clean = sum(1 for r in checked if r["WrongCount"] == 0)
    missing = sum(1 for r in out if r["Note"].startswith("Missing"))
    print(f"{len(checked)} pilot records checked, {clean} fully correct, {missing} missing. Wrote {args.out}")


if __name__ == "__main__":
    sys.exit(main())
