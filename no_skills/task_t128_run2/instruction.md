Create a single Excel workbook that identifies the **unique fraud-flagging amount threshold** which best transfers from the labeled fraud dataset to the unlabeled e-commerce dataset, and then uses that threshold to score risk on the purchase-history dataset.

**Objective (one end goal):**  
Find the **single Amount threshold \(T\)** (in dollars) that **maximizes F1 score** for predicting `Class` in `/root/creditcard.csv` using the rule:

- predict fraud if `Amount >= T`, else legitimate

Then apply that same threshold to:
- `/root/transactions.csv` (use the transaction amount column) to compute the **share of transactions flagged** and the **total USD amount flagged** (only for rows whose currency code is `USD`)
- `/root/purchases.csv` to compute the **share of purchases flagged** and the **total amount flagged**

**Tie-breaking to ensure a unique answer:**  
If multiple thresholds achieve the same maximum F1 on `creditcard.csv`, choose the **smallest** such threshold \(T\).

**Required deliverable (must be saved as a file):**  
Save an Excel file to:

`/root/fraud_threshold_transfer_report.xlsx`

with exactly **two sheets**:

1) **`threshold_result`** (a 2-column table with headers `metric`, `value`) containing these rows:
- `best_threshold_T`
- `max_f1`
- `precision_at_T`
- `recall_at_T`
- `creditcard_fraud_rate` (overall mean of `Class`)
- `transactions_flag_rate` (fraction of all rows in `transactions.csv` with amount >= T)
- `transactions_usd_flagged_amount` (sum of amounts for rows with currency == USD and amount >= T)
- `purchases_flag_rate` (fraction of all rows in `purchases.csv` with amount >= T)
- `purchases_flagged_amount` (sum of amounts in `purchases.csv` with amount >= T)

2) **`validation`** containing a small table listing the **top 10 `Amount` values** from `creditcard.csv` (descending) with their `Class` values, so the threshold can be sanity-checked.

**Implementation notes (must follow):**
- Use only the provided files and the available skills (Excel Analysis + xlsx as needed).
- Treat `creditcard.csv` `Amount` as numeric; evaluate candidate thresholds only at **distinct observed Amount values** in `creditcard.csv` (so the result is deterministic).
- Parse `transactions.csv` correctly despite having **no header row**: infer columns by position and use the **3rd field** as amount and **4th field** as currency (as indicated by the file summary).
- Write the final results into the specified Excel workbook path; do not rely on stdout for the answer.