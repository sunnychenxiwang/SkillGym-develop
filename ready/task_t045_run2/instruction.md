Using **all three provided files** (`/root/SiO2-Quartz-alpha.cif`, `/root/SiO2-Cristobalite.cif`, and `/root/1272701`), build a **single JSON “polymorph identity check” artifact** that determines which CIF (quartz vs cristobalite) matches the Materials Project page (mp-6930) and quantifies how much the other CIF differs.

Requirements:

1. **Parse the Materials Project HTML (1272701)** to extract, at minimum:
   - the material id (e.g., `mp-6930`)
   - the crystal system string
   - the space group symbol (e.g., `P3_221`) and space group number (e.g., `154`)
   - any explicit polymorph/structure label present on the page (e.g., “alpha-quartz”)

2. **Load both CIFs with pymatgen** and, for each structure, compute:
   - `space_group_symbol` and `space_group_number` using `SpacegroupAnalyzer`
   - `crystal_system` using `SpacegroupAnalyzer`
   - `density` and `volume` from the `Structure`

3. **Decide the unique matching CIF** as the one whose `(space_group_number AND crystal_system)` exactly matches the HTML-extracted values. (If both or neither match, treat that as an error and still write the JSON with `"match_status": "ambiguous"` or `"match_status": "no_match"`.)

4. For the **non-matching CIF**, compute the **percent differences** relative to the matching CIF:
   - `density_percent_diff = 100 * (density_nonmatch - density_match) / density_match`
   - `volume_percent_diff = 100 * (volume_nonmatch - volume_match) / volume_match`
   Round these two percent differences to **3 decimal places**.

5. **Write exactly one output file** at:
   - `/root/sio2_polymorph_match.json`

The JSON must have exactly this schema (keys required, no extras), with all numeric values as JSON numbers:

```json
{
  "mp_material_id": "mp-6930",
  "mp_space_group_symbol": "P3_221",
  "mp_space_group_number": 154,
  "mp_crystal_system": "trigonal",
  "mp_label": "alpha-quartz",
  "match_status": "match",
  "matching_cif": "SiO2-Quartz-alpha.cif",
  "nonmatching_cif": "SiO2-Cristobalite.cif",
  "matching_properties": {
    "space_group_symbol": "P 32 2 1",
    "space_group_number": 154,
    "crystal_system": "trigonal",
    "density": 2.65,
    "volume": 112.9
  },
  "nonmatching_properties": {
    "space_group_symbol": "P 41 21 2",
    "space_group_number": 92,
    "crystal_system": "tetragonal",
    "density": 2.332,
    "volume": 171.104
  },
  "nonmatch_vs_match_percent_diff": {
    "density": -12.0,
    "volume": 51.6
  }
}
```

Notes:
- Use the **exact CIF basenames** shown above for `matching_cif` / `nonmatching_cif`.
- The `matching_properties` / `nonmatching_properties` values must come from pymatgen computations on the CIFs (not hardcoded from the CIF text).
- The MP-derived fields must come from parsing the provided HTML file (not inferred from the CIFs).