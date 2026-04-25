Create a single Excel workbook that quantifies **how much the “Blank” control in `Dataset_S9.csv` would distort a construction time-series if it were mistakenly included as real activity**, and express that distortion on the same scale as the government construction datasets.

1) Using `Dataset_S9.csv`, compute the **Blank-adjusted net growth signal** per timestamp as:  
   \[
   \text{Net\_OD}(t)=\Big(\text{mean OD across all non-Blank strains/replicates at }t\Big)\;-\;\Big(\text{mean OD of Blank (Replicate=0) at }t\Big)
   \]
   Then compute a single scalar **Blank Distortion Ratio (BDR)**:
   \[
   \text{BDR}=\frac{\sum_t \left|\text{mean\_OD\_all}(t)-\text{mean\_OD\_nonblank}(t)\right|}{\sum_t \left|\text{Net\_OD}(t)\right|}
   \]
   where `mean_OD_all(t)` includes Blank + all strains, and `mean_OD_nonblank(t)` excludes Blank.

2) Using `construction.csv`, compute the **Total permits grand mean** across all rows (ignore the “2 to 4 units” column entirely since it is NA throughout; do not impute it).

3) Using `construction_spending.csv`, compute the **grand mean of `current.combined.total`** across all rows.

4) Create an Excel file at exactly:  
`/root/output/blank_distortion_construction_scaled.xlsx`

The workbook must contain:
- Sheet **`Result`** with three labeled values:
  - `BDR` (from step 1)
  - `Permits_Total_GrandMean` (from step 2)
  - `Spending_CurrentCombinedTotal_GrandMean` (from step 3)
- Sheet **`Scaled_Impact`** that computes (via Excel formulas, not precomputed numbers) two scaled impacts:
  - `BDR * Permits_Total_GrandMean`
  - `BDR * Spending_CurrentCombinedTotal_GrandMean`

Excel formatting requirements (must be applied in the saved file):
- In `Result`: labels in bold; numeric cells formatted to 6 decimals for `BDR`, and `$#,##0.00` for spending mean, `#,##0.00` for permits mean.
- In `Scaled_Impact`: the two formula cells must be black text (formula convention) and use the same number formats as their respective bases (permits vs spending).
- Put the three `Result` numeric inputs in blue font (hardcoded inputs convention), even though they are computed—this is intentional for verification.

The task is complete only if the specified `.xlsx` file is written with the required sheets, values, formulas, and formatting.