Create a single Excel report that **verifies whether the alpha‑quartz CIF file matches the Materials Project mp‑6930 page on space group and local Si–O geometry, and contrasts those results against the alpha‑cristobalite CIF**.

Use **all three input files** as follows:
1) Parse `/root/1272701` (the mp‑6930 HTML) to extract these three reference facts (as strings/numbers exactly as stated on the page):
   - Material identifier (`mp-6930`)
   - Space group symbol and number (e.g., `P3_221`, `#154`)
   - The reported Si–O bond lengths (two values, in Å) and the reported O–Si–O (or Si–O–Si if that is what is stated) angle value (in degrees) mentioned in the text.

2) Load both CIFs with pymatgen:
   - `/root/SiO2-Quartz-alpha.cif`
   - `/root/SiO2-Cristobalite.cif`

   For each structure:
   - Compute the space group symbol and number using `SpacegroupAnalyzer` (use `symprec=0.01`).
   - Using `CrystalNN`, find all Si sites, collect all Si–O neighbor distances (Å), and report:
     - the mean of the **two shortest** Si–O distances per Si (averaged over all Si),
     - the mean of the **two longest** Si–O distances per Si (averaged over all Si).
   - Also compute the mean Si–O–Si angle (degrees) by, for each O atom bonded to exactly two Si neighbors (per CrystalNN), calculating the Si–O–Si angle and averaging over all such O atoms.

3) Write the results to an Excel file at exactly:
`/root/sio2_mp6930_verification.xlsx`

The workbook must contain one sheet named `Verification` with this exact table layout (cell-for-cell), and use Excel conventions:
- Blue font (`0000FF`) for values extracted from the HTML (MP reference values).
- Black font (`000000`) for values computed from CIFs.
- Column headers bold.
- Numeric formatting: distances with `0.000` and angles with `0.0`.

Table layout (exact):
- Row 1 headers:
  - A1: `Metric`
  - B1: `MP mp-6930 (HTML)`
  - C1: `Quartz (CIF)`
  - D1: `Cristobalite (CIF)`
  - E1: `Quartz matches MP?`
- Rows 2–6 metrics in column A exactly:
  - A2 `Material ID`
  - A3 `Space group (symbol)`
  - A4 `Space group (number)`
  - A5 `Si–O short (Å)`
  - A6 `Si–O long (Å)`
  - A7 `Si–O–Si angle (deg)`

Fill columns B–D with the corresponding values (HTML in B, quartz in C, cristobalite in D).  
In column E, put `TRUE`/`FALSE` for rows 2–4 based on exact string/number equality between MP (col B) and Quartz (col C). For rows 5–7, put `TRUE` if Quartz differs from MP by **≤ 0.02 Å** for distances and **≤ 2.0°** for angle; otherwise `FALSE`.

Save the Excel file. The task is complete only if the file exists at the specified output path with the specified sheet name, layout, formatting rules, and computed values.