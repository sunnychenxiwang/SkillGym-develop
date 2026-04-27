Create a single Excel deliverable that quantifies and compares **growth dynamics across biological strains** and **housing construction categories**, then ranks them on a common “relative change” scale.

Using **all three input files**:

1. From `/root/Dataset S9.csv`, compute for each **Strain** (excluding `Blank`) the **maximum OD fold-change** over the experiment, defined as:  
   \[
   \text{FoldChange}_{strain}=\frac{\max(\text{OD})}{\min(\text{OD})}
   \]
   where min/max are taken over all rows for that strain across replicates, but **ignore any OD ≤ 0** when computing the minimum (to avoid division by zero/negative).  

2. From `/root/construction.csv`, compute for each **building type column** (`1 unit`, `2 to 4 units`, `5 units or more`) the **max-to-min ratio** across all months, defined as:  
   \[
   \text{Ratio}_{type}=\frac{\max(\text{value})}{\min(\text{value})}
   \]
   ignoring `NA` values.

3. From `/root/construction_spending.csv`, identify the single spending category column whose **annual.combined.\*** series has the **largest max-to-min ratio** across all available years (use the same ratio definition as above). Record both the column name and its ratio.

Then, combine the results into one ranked table with exactly these rows:
- one row per non-Blank strain from (1)
- one row per building type from (2)
- one row for the winning spending category from (3)

Normalize nothing further; just rank by the computed ratio/fold-change (descending). If ties occur, break ties by alphabetical order of the `item_name`.

Save a formatted Excel file to **`/root/relative_change_ranking.xlsx`** containing:
- Sheet `Ranking` with columns exactly: `item_type`, `item_name`, `ratio`, `rank`
- `rank` must be 1 for the largest ratio.
- `ratio` must be written as a number with 4 decimal places.
- Apply bold header, freeze top row, and auto-fit column widths.

This Excel file is the only required output and must be written to the specified path.