Using **all three input CSVs** (`Dataset_S9.csv`, `construction.csv`, `construction_spending.csv`), determine the **single calendar month (year-month) that is the unique “best match”** between the microbial growth experiment’s peak-growth timing and U.S. construction activity, and save the result as a small, machine-verifiable JSON.

Define and compute the following, in this exact way:

1. **From `/root/Dataset_S9.csv` (growth data):**  
   - Exclude `Strain == "Blank"`.  
   - For each remaining (`Strain`, `Replicate`) series, baseline-correct OD by subtracting that series’ OD at the **earliest** `Time_hours`.  
   - For each corrected series, find the **earliest** `Time_hours` where corrected OD is **>= 0.30**.  
   - Take the **median** of those “time-to-0.30” values across all non-blank series; call it `t_median_hours`.

2. **From `/root/construction.csv` (housing starts):**  
   - Treat `NA` as missing.  
   - For each row (month), compute `starts_total = Total` (as numeric).  
   - Rank months by `starts_total` descending; if ties, break ties by earlier calendar month (Year then Month order as they appear in the file).  
   - Convert that rank into a **0–1 percentile**:  
     \[
     p_{starts} = \frac{rank-1}{N-1}
     \]
     where `rank=1` is highest Total, and `N` is number of months.

3. **From `/root/construction_spending.csv` (spending time series):**  
   - For each month, compute `spend_total = current.combined.total construction` (numeric).  
   - Rank months by `spend_total` descending; if ties, break ties by earlier calendar month (time.year then time.month).  
   - Convert that rank into a **0–1 percentile** the same way to get `p_spend`.

4. **Align months across files and select the best-match month:**  
   - Convert `t_median_hours` to a target percentile on 0–1 by:  
     \[
     p_{target} = \min(1,\max(0,\frac{t\_median\_hours}{10}))
     \]
     (since the experiment spans ~10 hours).  
   - Consider only months that exist in **both** `construction.csv` and `construction_spending.csv` after parsing (match by calendar year and month name/number).  
   - For each overlapping month compute a match score:  
     \[
     score = |p_{starts} - p_{target}| + |p_{spend} - p_{target}|
     \]
   - Choose the month with the **minimum** `score`. If there is a tie, choose the **earliest** calendar month.

5. **Write exactly one output file** at:  
   `/root/best_match_month.json`

The JSON must have this exact schema (numbers as JSON numbers, not strings):

```json
{
  "t_median_hours": 0.0,
  "p_target": 0.0,
  "best_match": {
    "year": 0,
    "month": "MonthName",
    "p_starts": 0.0,
    "p_spend": 0.0,
    "score": 0.0
  }
}
```

Notes/constraints:
- Month in the output must be the **month name** as shown in `construction.csv` (e.g., "December").  
- You must use pandas for the computations and may use openpyxl only if you choose to create intermediate Excel workbooks (not required).  
- Do not print the final answer to stdout; completion is verified solely by the saved JSON content.