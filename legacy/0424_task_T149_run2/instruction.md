Create a single Excel “Delay vs Demand” workbook that quantifies (in one number) how strongly monthly airline demand relates to flight delays, by combining both provided datasets.

1) From `/root/flights.csv`, compute **monthly total passengers** for each `(year, month)` (this file is already monthly; treat `passengers` as the monthly total).  
2) From `/root/flights_2.csv`, clean missing values (`"NA"` and empty strings as missing), then compute **monthly average arrival delay** for each `(year, month)` using `arr_delay` (ignore missing `arr_delay`).  
3) Join the two monthly tables on `(year, month)` and keep only months that exist in **both** datasets.  
4) Compute the **Pearson correlation coefficient** between `monthly_passengers` and `avg_arr_delay` over the joined months (a single scalar).  
5) Save an Excel file to **`/root/output/delay_vs_demand.xlsx`** with:
   - Sheet `monthly_joined`: the joined table with columns exactly: `year`, `month`, `monthly_passengers`, `avg_arr_delay`.
   - Sheet `result`: cell `A1` = `correlation`, cell `B1` = the computed correlation value (numeric).
   - A scatter chart (on sheet `result`) plotting `monthly_passengers` (x) vs `avg_arr_delay` (y), and apply financial-model styling conventions: headers bold; input/data cells in blue font; the correlation value cell in black font; reasonable number formats (passengers as integer with thousands separator; delay with 1 decimal; correlation with 4 decimals).

Writing the Excel file at the specified path is mandatory for completion.