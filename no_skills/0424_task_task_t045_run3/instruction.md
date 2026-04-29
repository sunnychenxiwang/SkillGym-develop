Using the two CIF files and the Materials Project HTML page, build a **single JSON “polymorph fingerprint”** that deterministically identifies which CIF corresponds to the Materials Project material **mp-6930 (SiO₂ / quartz)** and quantifies how the two CIF polymorphs differ structurally and in diffraction, then reduces those differences to a 1D score via PCA.

Steps (all required for the one final deliverable):

1. **Parse the Materials Project HTML file** `/root/1272701` and extract:
   - the material id string (must be `mp-6930`),
   - the crystal system string,
   - the space group symbol string,
   - the space group number (integer).
   Treat these as the “reference” symmetry descriptors.

2. **Load both CIFs with pymatgen**:
   - `/root/SiO2-Quartz-alpha.cif`
   - `/root/SiO2-Cristobalite.cif`

   For each structure, compute:
   - space group symbol and number via `SpacegroupAnalyzer`,
   - crystal system via `SpacegroupAnalyzer`,
   - density (`struct.density`),
   - volume (`struct.volume`),
   - mean Si–O bond length estimated from local environments: for every Si site, use `CrystalNN().get_nn_info` to collect neighbor O distances and average them (one mean per structure),
   - an XRD pattern using `XRDCalculator().get_pattern(struct, two_theta_range=(10, 80))`, then compute:
     - `peak_count` = number of peaks (`len(pattern.x)`),
     - `max_intensity_2theta` = 2θ at maximum intensity.

3. **Identify the matching CIF for mp-6930** by exact match of (space group number AND symbol) against the reference extracted from the HTML. This must yield exactly one match; record its filename as `mp6930_match_file`.

4. **Create a 2-row feature table** (rows = the two CIFs) with exactly these numeric columns in this order:
   1) `volume`
   2) `density`
   3) `mean_si_o_bond`
   4) `peak_count`
   5) `max_intensity_2theta`

   Standardize the table (zero mean, unit variance), then run **FactorAnalyzer** with:
   - `n_factors=1`
   - `rotation=None`
   Fit on the 2x5 standardized matrix and compute:
   - the 1D factor scores for each CIF (`fa.transform`),
   - the eigenvalues (`fa.get_eigenvalues()`).

   Define `pca_separation` as the absolute difference between the two structures’ 1D scores (a single float).

5. **Write exactly one output file** at:
`/root/output/sio2_polymorph_fingerprint.json`

The JSON must have this exact schema (all keys required; no extras):
```json
{
  "reference_from_html": {
    "material_id": "mp-6930",
    "crystal_system": "...",
    "spacegroup_symbol": "...",
    "spacegroup_number": 0
  },
  "structures": [
    {
      "file": "SiO2-Quartz-alpha.cif",
      "spacegroup_symbol": "...",
      "spacegroup_number": 0,
      "crystal_system": "...",
      "volume": 0.0,
      "density": 0.0,
      "mean_si_o_bond": 0.0,
      "peak_count": 0,
      "max_intensity_2theta": 0.0,
      "factor_score_1d": 0.0
    },
    {
      "file": "SiO2-Cristobalite.cif",
      "spacegroup_symbol": "...",
      "spacegroup_number": 0,
      "crystal_system": "...",
      "volume": 0.0,
      "density": 0.0,
      "mean_si_o_bond": 0.0,
      "peak_count": 0,
      "max_intensity_2theta": 0.0,
      "factor_score_1d": 0.0
    }
  ],
  "mp6930_match_file": "...",
  "factor_analysis": {
    "n_factors": 1,
    "rotation": null,
    "eigenvalues": [0.0, 0.0, 0.0, 0.0, 0.0],
    "pca_separation": 0.0
  }
}
```

Determinism requirements:
- Keep the `structures` array in the fixed order shown above (Quartz-alpha first, Cristobalite second).
- Round all floating values in the JSON to **6 decimal places** before writing.
- `eigenvalues` must be the full length-5 list returned by the method (rounded to 6 decimals).