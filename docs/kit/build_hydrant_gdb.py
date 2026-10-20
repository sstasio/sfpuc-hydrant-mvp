"""Build the hydrant inspection MVP file geodatabase.

Creates HydrantInspections.gdb with:
  - Hydrants point feature class (sample points loaded from data/sample_hydrants.csv)
  - HydrantInspections table, related 1:M on Hydrants.GlobalID -> HydrantInspections.HydrantGUID
  - Coded value and range domains, GlobalIDs, attachments and editor tracking

Then share it from ArcGIS Pro as one web layer to the Enterprise portal. Survey123
and Field Maps both edit that same service.

Run it one of three ways (all need ArcGIS Pro's arcpy). Use the full path to the
script, since none of them starts in the folder you unzipped hydrant-mvp into.

ArcGIS Pro notebook cell (this is Python, so a bare `propy ...` line is a SyntaxError):
    %run "C:\\temp\\hydrant-mvp\\build_hydrant_gdb.py" --out C:\\temp

ArcGIS Pro Python window (Analysis > Python > Python Window), which is plain Python
with no %run, so paste:
    import sys, runpy; sys.argv = [r"C:\\temp\\hydrant-mvp\\build_hydrant_gdb.py", "--out", r"C:\\temp"]; runpy.run_path(sys.argv[0], run_name="__main__")

ArcGIS Pro Python Command Prompt (Windows Start menu):
    propy "C:\\temp\\hydrant-mvp\\build_hydrant_gdb.py" --out C:\\temp
    add --hydrants path\\to\\real_hydrants.csv to load real hydrants instead

The definitions below have no arcpy dependency, so other scripts (the XLSForm
builder) can import them and stay in step with the geodatabase.
"""
import argparse
import csv
import os

GDB_NAME = "HydrantInspections.gdb"
HYDRANTS = "Hydrants"
INSPECTIONS = "HydrantInspections"
RELATIONSHIP = "Hydrants_HydrantInspections"
# Storage coordinate system. Input CSV coordinates are always WGS84 lat/lon and are
# projected to this on load; switch to 2227 (CA State Plane III, US ft) or the SFPUC
# standard if preferred.
SPATIAL_REF = 4326

# Folder holding data/. Pasted into a Pro notebook there is no __file__, so set
# HERE by hand to the folder you unzipped hydrant-mvp into.
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = r"C:\temp\hydrant-mvp"
INSPECTORS_CSV = os.path.join(HERE, "data", "inspectors.csv")
SAMPLE_HYDRANTS_CSV = os.path.join(HERE, "data", "sample_hydrants.csv")

YES_NO = [("Yes", "Yes"), ("No", "No")]
ENGINE_COS = [f"E{n:02d}" for n in range(1, 52)]


def inspector_code(name):
    """'Drake III,C' -> 'Drake_III_C' (XLSForm choice names can't hold spaces or commas)."""
    return name.replace(",", "_").replace(" ", "_").replace("'", "").replace(".", "")


def load_inspectors(path=INSPECTORS_CSV):
    with open(path, newline="", encoding="utf-8") as f:
        return [(r["EngineCo"], r["Inspector"]) for r in csv.DictReader(f)]


def coded_domains():
    inspectors = sorted({name for _, name in load_inspectors()})
    return {
        "YesNo": ("Yes or No", YES_NO),
        "EngineCompany": ("SFFD engine company", [(c, c) for c in ENGINE_COS]),
        "Inspector": ("Inspector name", [(inspector_code(n), n.replace(",", ", ")) for n in inspectors]
                      + [("Other", "Other (type in Remarks)")]),
        "Operable": ("Hydrant operable", [("Yes", "Yes"), ("Limited", "Limited"), ("No", "No")]),
        "ShutoffValve": ("Shutoff valve condition", [
            ("OK", "OK"),
            ("Buried", "Buried or paved over"),
            ("Inaccessible", "Inaccessible"),
            ("WaterInBox", "Water in valve box"),
            ("NotFound", "Not found"),
        ]),
        "PressureType": ("Hydrant system", [("Low", "Low pressure"), ("High", "High pressure (AWSS)")]),
    }


RANGE_DOMAINS = {
    "PressurePSI": ("Pressure in psi", 0, 300),
    "CapsMissing": ("Caps missing", 0, 3),
}

# (name, type, alias, length, domain)
HYDRANT_FIELDS = [
    ("GISID", "TEXT", "GIS ID", 20, None),
    ("SerialNo", "TEXT", "Serial Number", 20, None),
    ("Location", "TEXT", "Address/Location", 150, None),
    ("PressureType", "TEXT", "System", 10, "PressureType"),
    ("MainSize", "SHORT", "Main Size (in)", None, None),
    ("SpindlePSI", "SHORT", "Stamped Spindle Pressure (psi)", None, "PressurePSI"),
    ("ShutoffDist", "SHORT", "Distance to Shutoff (ft)", None, None),
    ("EngineCo", "TEXT", "Engine Company", 5, "EngineCompany"),
]

# Issue flags are separate Yes/No fields (not one multi-select) so Field Maps can show
# them as switches and the dashboard can count each one.
MARKING_FLAGS = [
    ("MissSerial", "Serial number missing or unreadable"),
    ("MissSpindle", "Spindle pressure not stamped or unreadable"),
    ("MissMainSize", "Main size not labeled"),
    ("MissShutoffDist", "Distance to shutoff not labeled"),
]
ISSUE_FLAGS = [
    ("DmgThreads", "Damaged outlet threads"),
    ("StrippedSpindle", "Stripped or rounded spindle"),
    ("Leak", "Leak (outlet, bonnet or spindle)"),
    ("PaintedOver", "Painted over"),
    ("DmgCap", "Damaged cap"),
    ("HardToOperate", "Hard to operate"),
]

INSPECTION_FIELDS = (
    [
        ("HydrantGUID", "GUID", "Hydrant", None, None),
        ("GISID", "TEXT", "GIS ID", 20, None),
        ("InspDate", "DATE", "Inspection Date", None, None),
        ("EngineCo", "TEXT", "Engine Company", 5, "EngineCompany"),
        ("Inspector", "TEXT", "Inspector", 50, "Inspector"),
        ("Location", "TEXT", "Address/Location", 150, None),
        ("Lat", "DOUBLE", "Latitude", None, None),
        ("Lon", "DOUBLE", "Longitude", None, None),
        ("FoundAtLoc", "TEXT", "Found at Location", 3, "YesNo"),
        ("Operable", "TEXT", "Operable", 10, "Operable"),
        ("Corrosion", "TEXT", "Corrosion", 3, "YesNo"),
        ("Gauge", "SHORT", "Gauge Pressure (psi)", None, "PressurePSI"),
        ("Spindle", "SHORT", "Spindle Pressure (psi)", None, "PressurePSI"),
        ("LowPressure", "TEXT", "Low Pressure", 3, "YesNo"),
        ("CapsMissing", "SHORT", "Caps Missing", None, "CapsMissing"),
        ("ShutoffValve", "TEXT", "Shutoff Valve", 20, "ShutoffValve"),
        ("Obstructed", "TEXT", "Obstructed", 3, "YesNo"),
    ]
    + [(n, "TEXT", a, 3, "YesNo") for n, a in MARKING_FLAGS + ISSUE_FLAGS]
    + [
        ("NeedsFollowup", "TEXT", "Needs SFPUC Follow-up", 3, "YesNo"),
        ("Remarks", "TEXT", "Remarks", 1000, None),
    ]
)


def build(out_folder, hydrants_csv):
    import arcpy

    gdb = os.path.join(out_folder, GDB_NAME)
    if arcpy.Exists(gdb):
        raise SystemExit(f"{gdb} already exists. Remove it from any open map, delete it "
                         "in the Catalog pane, then run again (or pick another --out folder)")
    os.makedirs(out_folder, exist_ok=True)
    arcpy.management.CreateFileGDB(out_folder, GDB_NAME)

    for name, (desc, values) in coded_domains().items():
        arcpy.management.CreateDomain(gdb, name, desc, "TEXT", "CODED")
        for code, label in values:
            arcpy.management.AddCodedValueToDomain(gdb, name, code, label)
    for name, (desc, lo, hi) in RANGE_DOMAINS.items():
        arcpy.management.CreateDomain(gdb, name, desc, "SHORT", "RANGE")
        arcpy.management.SetValueForRangeDomain(gdb, name, lo, hi)

    sr = arcpy.SpatialReference(SPATIAL_REF)
    arcpy.management.CreateFeatureclass(gdb, HYDRANTS, "POINT", spatial_reference=sr)
    arcpy.management.CreateTable(gdb, INSPECTIONS)
    hydrants = os.path.join(gdb, HYDRANTS)
    inspections = os.path.join(gdb, INSPECTIONS)

    for table, fields in ((hydrants, HYDRANT_FIELDS), (inspections, INSPECTION_FIELDS)):
        arcpy.management.AddFields(table, [[n, t, a, l or "", "", d or ""] for n, t, a, l, d in fields])
        arcpy.management.AddGlobalIDs(table)
        arcpy.management.EnableEditorTracking(
            table, "created_user", "created_date", "last_edited_user", "last_edited_date",
            "ADD_FIELDS", "UTC")
    arcpy.management.EnableAttachments(inspections)

    arcpy.management.CreateRelationshipClass(
        hydrants, inspections, os.path.join(gdb, RELATIONSHIP), "SIMPLE",
        "Inspections", "Hydrant", "NONE", "ONE_TO_MANY", "NONE", "GlobalID", "HydrantGUID")

    names = [n for n, *_ in HYDRANT_FIELDS]
    with open(hydrants_csv, newline="", encoding="utf-8") as f, \
            arcpy.da.InsertCursor(hydrants, names + ["SHAPE@"]) as cur:
        wgs84 = arcpy.SpatialReference(4326)
        count = 0
        for row in csv.DictReader(f):
            values = [int(row[n]) if t == "SHORT" and row.get(n) else (row.get(n) or None)
                      for n, t, *_ in HYDRANT_FIELDS]
            point = arcpy.PointGeometry(arcpy.Point(float(row["Lon"]), float(row["Lat"])), wgs84)
            cur.insertRow(values + [point.projectAs(sr)])
            count += 1
    print(f"Built {gdb} with {count} hydrants")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default=HERE, help="Folder to create the geodatabase in (default: next to this script)")
    p.add_argument("--hydrants", default=SAMPLE_HYDRANTS_CSV,
                   help="CSV of hydrants with the Hydrants fields plus Lat and Lon (WGS84)")
    # parse_known_args ignores the extra arguments a notebook kernel passes in
    args, _ = p.parse_known_args()
    build(args.out, args.hydrants)
