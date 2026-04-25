Create a single Excel workbook that quantifies **which U.S. construction-spending sector best tracks the microbial growth curve shape**.

1) Load `/root/Dataset_S9.csv` and compute a single time series `OD_mean` by:
- excluding `Strain == "Blank"`
- grouping by `Time_hours` and taking the mean OD across all remaining rows at each time point.

2) Load `/root/construction_spending.csv` and build monthly time series for exactly these three columns:
- `annual.combined.residential`
- `annual.combined.commercial`
- `annual.combined.educational`

For each of the three series, compute its **Pearson correlation** with `OD_mean` after aligning by index position as follows:
- resample/trim so both vectors have the same length `N` by taking the first `N` points from each series, where `N = min(len(OD_mean), len(series))`
- compute correlation on those aligned vectors (no shifting/lagging).

3) Load `/root/construction.csv` and compute a single scalar `avg_total_permits` = the mean of the `Total` column across all rows (ignore any non-numeric/missing values).

4) Produce an Excel file at **exactly**:
`/root/output/growth_vs_construction_correlation.xlsx`

The workbook must contain:
- Sheet `Results` with a 4-row table (header + 3 sectors) with columns:
  - `sector_column` (exactly the spending column name)
  - `corr_with_OD_mean` (rounded to 6 decimals)
  - `avg_total_permits` (same value repeated for all 3 rows, rounded to 2 decimals)
  - `best_match` (TRUE only for the single row with the highest correlation; FALSE otherwise)
- Professional formatting using Excel conventions:
  - header row bold with a light fill
  - numeric columns formatted (correlation as `0.000000`, permits as `0.00`)
  - freeze top row and enable autofilter
- A second sheet `Data_Used` containing two columns:
  - `OD_mean` (the aligned OD vector actually used for correlation)
  - `best_sector_series` (the aligned spending vector for the best-match sector)

The task is complete only if the Excel file is written to the specified path with the required sheets, values, and formatting.