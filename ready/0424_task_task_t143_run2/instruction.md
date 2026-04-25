Create a single Excel workbook that answers this question: **Which “time.year” in `construction_spending.csv` has the highest *per-hour* construction spending intensity when normalized by the mean bacterial growth rate from `Dataset_S9.csv`, and what is that year’s Total housing construction level from `construction.csv`?**

To do this:

1. **From `Dataset_S9.csv` (growth curves):**
   - For each non-Blank strain+replicate, baseline-correct OD by subtracting the mean OD of the Blank (Replicate 0) at the same `Time_hours` (match on `Time_hours`).
   - For each strain+replicate, compute the **maximum growth rate** as the maximum slope of OD vs. time using consecutive points:  
     \[
     \max \left(\frac{\Delta OD}{\Delta Time\_hours}\right)
     \]
   - Compute the **mean of these maxima** across all non-Blank strain+replicates. Call this value `mean_max_growth_rate`.

2. **From `construction_spending.csv` (spending):**
   - For each `time.year`, compute `annual_total_spending` as the **sum across all columns whose names start with `annual.combined.`** (sum over columns, then sum over rows within the year).
   - Compute `spending_intensity = annual_total_spending / mean_max_growth_rate`.
   - Identify the single `time.year` with the **largest** `spending_intensity` (break ties by choosing the smallest year).

3. **From `construction.csv` (housing construction):**
   - For the identified year, compute `avg_monthly_total` as the average of the `Total` column across rows in that year (ignore NA).
   - If that year does not exist in `construction.csv`, set `avg_monthly_total` to blank (empty cell).

4. **Deliverable (must be saved as a file):**
   - Write an Excel file to:  
     `/root/output/spending_vs_growth_answer.xlsx`
   - The workbook must contain:
     - Sheet **`Answer`** with exactly one row of results and these columns in order:
       1) `mean_max_growth_rate`  
       2) `best_year`  
       3) `annual_total_spending`  
       4) `spending_intensity`  
       5) `avg_monthly_total`
     - Sheet **`Checks`** containing:
       - A pivot-style table of `max_growth_rate` by `Strain` and `Replicate`.
       - A year-by-year table with `annual_total_spending` and `spending_intensity`.

5. **Excel formatting requirements (financial-model style):**
   - In `Answer`, format numeric outputs:
     - `annual_total_spending` and `avg_monthly_total` as currency with `"$#,##0;($#,##0);\"-\""` (zeros shown as “-”).
     - `mean_max_growth_rate` and `spending_intensity` as numbers with 3 decimals.
   - Use blue font for any hardcoded labels/inputs (if any), black font for computed values.
   - Use formulas (not hardcoded numbers) in `Answer` to pull the final values from the `Checks` sheet (cross-sheet references), and wrap any division in `IFERROR(...,"-")`.

The workbook content must be fully reproducible from the three provided CSVs, and the `best_year` must be uniquely determined by the rules above.