Create a single Excel workbook that reconciles **all money amounts** found in the three PDF invoices against the spending totals implied by the three CSV datasets, and outputs one uniquely checkable “variance” number.

**What to do (single objective: produce the reconciled variance workbook):**

1. **Extract invoice totals from PDFs**
   - From `/root/invoice.pdf`, extract: invoice date, vendor, invoice number, and **Amount Due/Total**.
   - From `/root/invoice_2.pdf`, extract: invoice date (or issue date), vendor/seller, invoice number, and **Total Due**.
   - From `/root/sample-invoice.pdf`, extract: invoice date, vendor, invoice number, and **Total Due** (not “Subtotal” and not “Previous Balance”; use the final amount due).

2. **Compute the “CSV spending total” (one deterministic number)**
   - From `/root/purchases.csv`: sum the `amount` column.
   - From `/root/creditcard.csv`: sum the `Amount` column **only for rows where `Class == 1`**.
   - From `/root/transactions.csv`: because it has no headers, treat it as a raw table and compute the sum of the **3rd column** (the transaction amount column described in the file summary). Ignore rows where that field is missing/non-numeric.
   - Define **CSV_SPEND_TOTAL = purchases_sum + creditcard_fraud_amount_sum + transactions_amount_sum**.

3. **Compute the “Invoice total” (one deterministic number)**
   - Define **INVOICE_TOTAL = sum of the three extracted invoice final totals** from step (1).

4. **Create the required deliverable workbook**
   - Save an .xlsx file to exactly:  
     `/root/output/reconciled_spend_variance.xlsx`
   - The workbook must contain **exactly 3 sheets** with these exact names and required content:

   **Sheet 1 — `Invoices`**
   - Table with columns (in this order): `source_file`, `vendor`, `invoice_number`, `invoice_date`, `final_total`
   - One row per PDF invoice (3 rows).
   - `final_total` must be numeric currency.

   **Sheet 2 — `CSV_Totals`**
   - Table with columns (in this order): `source_file`, `rule`, `computed_total`
   - Three rows, one per CSV:
     - purchases.csv with rule `SUM(amount)`
     - creditcard.csv with rule `SUM(Amount) WHERE Class=1`
     - transactions.csv with rule `SUM(col3_amount)`
   - `computed_total` must be numeric currency.

   **Sheet 3 — `Reconciliation`**
   - Cells that compute (with Excel formulas, not hardcoded numbers):
     - `INVOICE_TOTAL`
     - `CSV_SPEND_TOTAL`
     - `VARIANCE = CSV_SPEND_TOTAL - INVOICE_TOTAL`
   - Put the final variance value in cell **B6** (label in A6 = `VARIANCE`).
   - Apply professional formatting conventions:
     - Currency number format `$#,##0.00`
     - Bold headers
     - Yellow fill for the three key result cells (the cells containing INVOICE_TOTAL, CSV_SPEND_TOTAL, VARIANCE)

**Completion requirement:** the task is complete only when the workbook exists at the specified path and cell `Reconciliation!B6` contains the formula-derived variance.