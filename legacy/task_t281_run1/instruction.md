Using **all three CSV files** (`/root/harbor_workspaces/task_T281_run1/input/construction.csv`, `/root/harbor_workspaces/task_T281_run1/input/construction_spending.csv`, and `/root/harbor_workspaces/task_T281_run1/input/Dataset S9.csv`), determine which dataset shows the **largest relative within-period variability** after normalizing each dataset to a comparable “coefficient of variation” (CV) metric, and save the result as a single JSON artifact.

Define the CV metric for each file as follows (must follow exactly):

1) **construction.csv (monthly housing starts/permits-style table)**  
   - Create a proper monthly date index from `Year` + `Month` (assume Month is English month name).  
   - Use only the `Total` column.  
   - Compute **month-over-month percent change** of `Total` (drop the first month).  
   - CV_construction = (standard deviation of those percent changes) / (absolute value of their mean).  

2) **construction_spending.csv (monthly spending, many columns)**  
   - Create a proper monthly date index from `time.year` + `time.month`.  
   - Filter rows where `time.period == "annual"` only.  
   - Use the single column `annual.combined.total` if present; otherwise use the column that exactly equals the total for annual combined spending (the one whose name ends with `.total` under `annual.combined.`).  
   - Compute **month-over-month percent change** of that total series (drop the first month).  
   - CV_spending = (standard deviation of those percent changes) / (absolute value of their mean).  

3) **Dataset S9.csv (microbial growth curves)**  
   - Exclude rows where `Strain == "Blank"`.  
   - For each (`Strain`, `Replicate`) pair, compute the **growth rate series** as the first difference of `OD` divided by the first difference of `Time_hours` (i.e., dOD/dt between consecutive timepoints). Drop the first timepoint per group.  
   - Pool all computed dOD/dt values across all non-blank groups into one vector.  
   - CV_microbe = (standard deviation of pooled dOD/dt) / (absolute value of mean pooled dOD/dt).  

Then:
- Identify `winner` = the dataset name among `["construction", "construction_spending", "microbe"]` with the **largest** CV value (ties broken by lexicographic order of the dataset name).
- Save **exactly** this JSON to `/root/variability_winner.json`:

```json
{
  "CV_construction": <float>,
  "CV_spending": <float>,
  "CV_microbe": <float>,
  "winner": "<string>"
}
```

Requirements:
- All three CV values must be finite floats (no NaN/inf); if a mean is zero, treat the CV for that dataset as `null` and exclude it from winning (but still write the key with null).
- Do not print the answer; writing the JSON file at the specified path is mandatory.