Using **all three CSVs** (`/root/Dataset S9.csv`, `/root/construction.csv`, `/root/construction_spending.csv`), determine **which construction-spending category’s month-to-month volatility best matches the LuxO-vs-C6706 growth advantage volatility**.

Define and compute the following, exactly:

1. **Growth-advantage volatility series (from `Dataset S9.csv`):**
   - Exclude `Strain == "Blank"`.
   - For each (`Strain`, `Time_hours`), compute the mean `OD` across replicates.
   - Pivot to wide form to get `OD_C6706(t)` and `OD_LuxO(t)` at each `Time_hours`.
   - Compute `adv(t) = OD_LuxO(t) - OD_C6706(t)`.
   - Compute the stepwise change `d_adv(t) = adv(t) - adv(t-1)` ordered by increasing `Time_hours`.
   - Let `sigma_adv = std(d_adv)` using the sample standard deviation (ddof=1).

2. **Candidate spending volatility series (from `construction_spending.csv`), restricted by months present in `construction.csv`:**
   - From `construction.csv`, build the set of (Year, MonthName) pairs present in the file (Month is the month name string as given).
   - In `construction_spending.csv`, restrict rows to those whose (`time.year`, `time.month name`) match that set.
   - Consider as candidates **all numeric spending columns whose names start with `annual.`** (ignore non-annual columns and the time columns).
   - For each candidate column `c`, sort by time (year then month number), compute `d_c = c(t) - c(t-1)` across the restricted months, then compute `sigma_c = std(d_c)` (sample std, ddof=1).

3. **Matching rule (single winner):**
   - For each candidate column, compute `gap_c = abs(sigma_c - sigma_adv)`.
   - Select the column with the **minimum** `gap_c`. Break ties by choosing the lexicographically smallest column name.

Save a single JSON file to:

`/root/volatility_match.json`

with exactly this schema:

```json
{
  "winner_column": "annual.combined.<exact column name from file>",
  "sigma_adv": 0.0,
  "sigma_winner": 0.0,
  "abs_gap": 0.0,
  "matched_months_count": 0
}
```

All floating values must be written as JSON numbers rounded to **6 decimal places**.