"""Load demo inspections so every pop-up state shows up in the map.

Reads data/demo_inspections.csv (23 inspections on 17 of the 21 sample hydrants;
4 are left uninspected) and adds them to the HydrantInspections table. HydrantGUID
is filled in by matching GISID to the hydrant's GlobalID, so the records relate to
the right hydrant wherever the GlobalIDs were created.

The dates in the CSV were written as of AS_OF and are moved forward by the days
since then, so "inspected 10 days ago" stays 10 days ago whenever you load it.
Add --keep-dates to load them as written.

Every demo record's Remarks starts with "DEMO." Remove them all before the pilot
with --remove.

Run it in ArcGIS Pro's Python, the same three ways as build_hydrant_gdb.py. Point it
at the published source layer (not a view), signed in to the portal as its owner:

ArcGIS Pro Python Command Prompt:
    propy "C:\\temp\\hydrant-mvp\\load_demo_inspections.py" --service <source service URL ending in /FeatureServer>

Python window (sign in to the portal in Pro first):
    import sys, runpy; sys.argv = [r"C:\\temp\\hydrant-mvp\\load_demo_inspections.py", "--service", "<source service URL>"]; runpy.run_path(sys.argv[0], run_name="__main__")

Or into a local geodatabase before publishing:
    propy "C:\\temp\\hydrant-mvp\\load_demo_inspections.py" --gdb C:\\temp\\HydrantInspections.gdb
"""
import argparse
import csv
import datetime as dt
import os
import sys

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = r"C:\temp\hydrant-mvp"
sys.path.insert(0, HERE)
from build_hydrant_gdb import HYDRANTS, INSPECTIONS, INSPECTION_FIELDS  # noqa: E402

DEMO_CSV = os.path.join(HERE, "data", "demo_inspections.csv")
AS_OF = dt.date(2026, 10, 20)


def actual_names(table):
    """Map lower-case field name -> the name as stored. Publishing to the portal's
    data store can lower-case every field name (GISID becomes gisid)."""
    import arcpy

    return {f.name.lower(): f.name for f in arcpy.ListFields(table)}


def globalid_name(table):
    import arcpy

    return next(f.name for f in arcpy.ListFields(table) if f.type == "GlobalID")


def demo_where(table):
    return f"{actual_names(table)['remarks']} LIKE 'DEMO.%'"


def targets(args):
    if args.service:
        url = args.service.rstrip("/")
        return f"{url}/0", f"{url}/1"
    return os.path.join(args.gdb, HYDRANTS), os.path.join(args.gdb, INSPECTIONS)


def remove(inspections):
    import arcpy

    count = 0
    with arcpy.da.UpdateCursor(inspections, ["OID@"], demo_where(inspections)) as cur:
        for _ in cur:
            cur.deleteRow()
            count += 1
    print(f"Removed {count} demo inspections")


def load(hydrants, inspections, csv_path, keep_dates=False):
    import arcpy

    if any(True for _ in arcpy.da.SearchCursor(inspections, ["OID@"], demo_where(inspections))):
        raise SystemExit("Demo inspections are already loaded. Run with --remove first to reload them")

    hydrant_fields = [actual_names(hydrants)["gisid"], globalid_name(hydrants)]
    guid_by_gisid = {gisid: guid for gisid, guid in arcpy.da.SearchCursor(hydrants, hydrant_fields)}
    shift = dt.timedelta(0) if keep_dates else dt.date.today() - AS_OF

    names = [n for n, *_ in INSPECTION_FIELDS]
    types = {n: t for n, t, *_ in INSPECTION_FIELDS}
    stored = actual_names(inspections)
    missing = [n for n in names if n.lower() not in stored]
    if missing:
        raise SystemExit("The inspections table has no field " + ", ".join(missing)
                         + ". Check that --service points at the source layer, with inspections as table 1")
    count, skipped = 0, set()
    with open(csv_path, newline="", encoding="utf-8") as f, \
            arcpy.da.InsertCursor(inspections, [stored[n.lower()] for n in names]) as cur:
        for row in csv.DictReader(f):
            guid = guid_by_gisid.get(row["GISID"])
            if guid is None:
                skipped.add(row["GISID"])
                continue
            row["HydrantGUID"] = guid
            values = []
            for n in names:
                v = row.get(n) or None
                if v is not None and types[n] == "SHORT":
                    v = int(v)
                elif v is not None and types[n] == "DOUBLE":
                    v = float(v)
                elif v is not None and types[n] == "DATE":
                    v = dt.datetime.strptime(v, "%Y-%m-%d %H:%M") + shift
                values.append(v)
            cur.insertRow(values)
            count += 1
    print(f"Loaded {count} demo inspections"
          + (f" (dates moved forward {shift.days} days)" if shift.days else ""))
    if skipped:
        print("No hydrant with GIS ID " + ", ".join(sorted(skipped)) + ", so those rows were skipped")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument("--service", help="Source feature service URL ending in /FeatureServer")
    where.add_argument("--gdb", help="Path to HydrantInspections.gdb")
    p.add_argument("--csv", default=DEMO_CSV, help="Demo inspections CSV (default: data/demo_inspections.csv)")
    p.add_argument("--keep-dates", action="store_true", help="Load dates as written instead of moving them to today")
    p.add_argument("--remove", action="store_true", help="Delete every demo inspection (Remarks starting DEMO.)")
    args, _ = p.parse_known_args()
    hydrants, inspections = targets(args)
    if args.remove:
        remove(inspections)
    else:
        load(hydrants, inspections, args.csv, args.keep_dates)
