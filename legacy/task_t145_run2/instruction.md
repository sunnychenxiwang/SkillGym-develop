Create a single Excel deliverable that identifies the **one customer account** in `sample-salesv3.xlsx` whose **2014 net revenue** (sum of `ext price`, including negative return lines) is **closest to the overall median net revenue across all accounts**, and enrich that result with a **product-price sanity check** using `Products.xlsx`.

To do this, you must:

1. **Load and clean** `sample-salesv3.xlsx`:
   - Parse `date` as datetime and keep only rows in calendar year **2014** (should be all rows, but enforce it).
   - Ensure `ext price` is numeric and compute **net revenue per account number** as the sum of `ext price` (returns reduce revenue).

2. **Compute the target account deterministically**:
   - Compute the **median** of the per-account net revenue distribution.
   - Find the **single account number** whose net revenue has the **smallest absolute difference** from that median.
   - If there is a tie, break it by choosing the **smaller account number**.

3. **Use `Products.xlsx` for a sanity-check metric**:
   - For the target account, compute its **weighted average unit price** over all its transactions using `SUM(quantity * unit price) / SUM(quantity)` but **exclude rows where quantity ≤ 0** (returns/adjustments) from both numerator and denominator.
   - Compute the **overall median product Price** from `Products.xlsx`.
   - Create a boolean flag `AboveCatalogMedian` indicating whether the account’s weighted average unit price is **strictly greater** than the catalog median product price.

4. **Use `Formula Excel Template.xlsx` as the output template**:
   - Copy it to a new workbook and add a new worksheet named **`MedianAccount`**.
   - In `MedianAccount`, write a small, clearly labeled table with exactly these fields and values (one row of values):
     - `AccountNumber`
     - `CustomerName` (use the most frequent `name` for that account in `sample-salesv3.xlsx`; if tied, pick the lexicographically smallest name)
     - `NetRevenue2014`
     - `MedianNetRevenueAllAccounts`
     - `AbsDiffFromMedian`
     - `WeightedAvgUnitPrice_PosQtyOnly`
     - `CatalogMedianProductPrice`
     - `AboveCatalogMedian` (TRUE/FALSE)

5. **Also use `sample-1-sheet.xlsx` in a meaningful, verifiable way**:
   - Read `sample-1-sheet.xlsx` and use it to drive formatting rules in `MedianAccount`:
     - If the value in its `boolean` column is **True** for the row where `number` = 1, then format the header row in `MedianAccount` with **bold font** and a **yellow fill**; otherwise leave headers unformatted.
   - (This ensures the task genuinely depends on this file.)

6. **Save the final Excel file** (this is mandatory) to:
   - `/root/median_account_report.xlsx`

The workbook must preserve all original sheets from `Formula Excel Template.xlsx` unchanged, with only the added `MedianAccount` sheet containing the computed, uniquely determined results.