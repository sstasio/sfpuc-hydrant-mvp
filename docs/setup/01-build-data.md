# 1. Build and publish the data

**Who:** GIS analyst · **You need:** ArcGIS Pro, publisher rights on the portal · **Done when:** one hosted layer with Hydrants and HydrantInspections is on the portal

One script builds the whole geodatabase: hydrant points, the inspection table, the relationship between them, the pick lists (domains), photo attachments and editor tracking.

## Files for this step

| File | What it is |
|---|---|
| [build_hydrant_gdb.py](../kit/build_hydrant_gdb.py) | Builds `HydrantInspections.gdb`. Runs in ArcGIS Pro's Python |
| [data/sample_hydrants.csv](../kit/data/sample_hydrants.csv) | 21 sample hydrants: real E01 serials and spindle pressures from the SFFD report. **Coordinates are estimated, not surveyed**: move the points or swap in a real export |
| [data/inspectors.csv](../kit/data/inspectors.csv) | Engine companies and inspector names from the SFFD FY22-23 report, used for the Inspector pick lists |

Or get everything at once from [Downloads](../downloads.md).

## Steps

1. **Unzip the kit** to `C:\temp\hydrant-mvp`, so the script sits next to the `data` folder.
2. **Run the script**, always with its full path. Pick one of these:

    - **ArcGIS Pro notebook** (Insert > New Notebook). In a cell:

        ```python
        %run "C:\temp\hydrant-mvp\build_hydrant_gdb.py" --out C:\temp
        ```

        A notebook cell is Python, so typing `propy ...` there gives a SyntaxError.

    - **Python window** (Analysis > Python > Python Window). It doesn't understand `%run`, so paste:

        ```python
        import sys, runpy; sys.argv = [r"C:\temp\hydrant-mvp\build_hydrant_gdb.py", "--out", r"C:\temp"]; runpy.run_path(sys.argv[0], run_name="__main__")
        ```

    - **Python Command Prompt** (Windows Start > ArcGIS > Python Command Prompt):

        ```
        propy "C:\temp\hydrant-mvp\build_hydrant_gdb.py" --out C:\temp
        ```

    It prints `Built C:\temp\HydrantInspections.gdb with 21 hydrants`.

    To run it again, first remove the layers from your map and delete the old geodatabase in the Catalog pane.

    To use real hydrants instead, export 20 to 50 points to a CSV with the same columns (`Lat`/`Lon` in WGS84) and add `--hydrants your.csv`.

3. **Add `Hydrants` and `HydrantInspections` to a map.** Symbolize hydrants simply: water blue `#007DC3` points.
4. **Share > Web Layer**, copying all data to the portal's data store.
    - Under **Configuration > Feature**, turn on **Create, Update, Delete, Sync**. Sync is needed for offline.
    - In the same place, open the layer properties (pencil icon next to **Feature**) and **uncheck Only allow true curve updates by true curve clients**. Left on, Field Maps refuses to edit the layer with "Features with true curves cannot currently be edited", even though points and tables have no curves. Already published with it on? See [Troubleshooting](../reference/troubleshooting.md#features-with-true-curves-cannot-currently-be-edited).
    - Share it with yourself or the GIS team only. Crews get views instead (next step).
5. **Check the result:** one service, with layer 0 = Hydrants and table 1 = HydrantInspections. Write down the service URL and item ID.

## Next

[2. Lock down the source and create views](02-views.md)
