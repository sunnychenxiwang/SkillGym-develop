Using **all three input files** (`countries.geojson`, `countries.geo.json`, and `geo-countries`), determine **which country polygon changed the most between the two GeoJSON datasets** and save a single JSON answer file.

**What to do (single objective: identify the country with the largest boundary change):**
1. Load both GeoJSON country datasets:
   - `/root/countries.geojson`
   - `/root/countries.geo.json`
2. From the saved GitHub HTML page `/root/geo-countries`, extract the repository identity (owner/repo string) and include it verbatim in the final output as the `source_repo` field (this ensures the result is grounded in the specific dataset provenance contained in that HTML file).
3. Match countries **between the two GeoJSON files** by a stable identifier present in both (prefer `ISO_A3` if available; otherwise use the best common ISO/code field you can find that yields a one-to-one match for most features). Drop any features that cannot be matched uniquely.
4. Reproject both matched layers to a **metric CRS** suitable for area calculations (e.g., `EPSG:4087`), then for each matched country compute:
   - `sym_diff_area_km2`: area of the **symmetric difference** between the two versions of that country’s geometry (i.e., area of parts that changed), in km².
5. Identify the **single country with the maximum** `sym_diff_area_km2`. This must be deterministic (if there is a tie, break it by choosing the lexicographically smallest matched country code you used for matching).
6. Write the result to exactly this file path (writing the file is mandatory):
   - `/root/largest_boundary_change.json`

**Output file schema (must be exactly this JSON structure):**
```json
{
  "source_repo": "OWNER/REPO",
  "match_key": "NAME_OF_MATCH_FIELD",
  "country_id": "MATCHED_ID_VALUE",
  "country_name": "COUNTRY_NAME_FROM_PROPERTIES",
  "sym_diff_area_km2": 12345.6789
}
```

Notes:
- Use GeoPandas/Shapely operations (e.g., overlay or geometry symmetric difference) and proper CRS handling (`to_crs`) so area is computed in meters then converted to km².
- The task is considered complete only if the JSON file exists at the specified output path and contains a single, uniquely determined winner.