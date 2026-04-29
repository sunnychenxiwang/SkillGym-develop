Using **all three provided files**—`/root/SiO2-Quartz-alpha.cif`, `/root/SiO2-Cristobalite.cif`, and `/root/1272701`—determine **which CIF file corresponds to the Materials Project material mp-6930 shown in the HTML page** by verifying agreement on **(a)** reduced chemical formula and **(b)** space group (both Hermann–Mauguin symbol and international number).

Required method constraints (must be followed to make the result uniquely verifiable):
1. Parse the HTML file to extract mp-id, reduced formula, and space group symbol/number for mp-6930.
2. Load each CIF into a `pymatgen` `Structure`, use `SpacegroupAnalyzer` to compute its space group symbol and number, and compute its reduced formula from the structure composition.
3. Choose the **single** CIF whose reduced formula and space group (symbol + number) match the HTML-extracted mp-6930 values. If both or neither match, treat that as an error and still write the JSON with `"match_status": "ambiguous"` or `"match_status": "no_match"` accordingly.

Write the final result **as a single JSON file** to:

`/root/mp6930_cif_match.json`

with exactly this schema:

```json
{
  "mp_id": "mp-6930",
  "html_reduced_formula": "SiO2",
  "html_spacegroup_symbol": "P3_221",
  "html_spacegroup_number": 154,
  "matched_cif_filename": "SiO2-Quartz-alpha.cif",
  "matched_cif_reduced_formula": "SiO2",
  "matched_cif_spacegroup_symbol": "P3_221",
  "matched_cif_spacegroup_number": 154,
  "match_status": "match"
}
```

Notes:
- `matched_cif_filename` must be **exactly** one of: `"SiO2-Quartz-alpha.cif"` or `"SiO2-Cristobalite.cif"`.
- The JSON values must be derived from the files (no hardcoding).
- Creating the JSON file at the specified path is mandatory for completion.