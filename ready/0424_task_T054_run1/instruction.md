Create an Excel deliverable that identifies the **single airline (carrier code)** with the **worst on-time performance** on the **SEA → LAX** route in the provided January-2014 flight records, and documents that result with an auditable calculation.

1. Using `/root/flights_2.csv`, filter to flights where `origin == "SEA"` and `dest == "LAX"`. Exclude rows where `arr_delay` is missing (`NA`).  
2. For each `carrier` in that filtered set, compute the **average arrival delay (minutes)**. Determine the **unique worst carrier** as the one with the **highest** average arrival delay. (If there is a tie, break it deterministically by choosing the alphabetically smallest carrier code among the tied carriers.)  
3. Using `/root/airlines.csv`, look up the winning carrier’s full airline name (`Description`) by matching the carrier code to `Code`.  
4. Save a formatted Excel workbook to **exactly**:  
`/root/output/sea_lax_worst_carrier.xlsx`

The workbook must contain exactly two sheets:

- **Sheet 1: `Route_Carrier_Summary`**  
  A table with one row per carrier on SEA→LAX containing: `carrier`, `carrier_name`, `flight_count_used` (count of non-missing `arr_delay` rows), and `avg_arr_delay_min` (numeric, rounded to 2 decimals). Sort rows by `avg_arr_delay_min` descending, then `carrier` ascending.

- **Sheet 2: `Answer`**  
  A small, clearly labeled block that contains:
  - `worst_carrier_code`
  - `worst_carrier_name`
  - `worst_avg_arr_delay_min`
  - A cross-sheet Excel formula (not a hardcoded duplicate) that pulls `worst_avg_arr_delay_min` from the top row of `Route_Carrier_Summary`.

Formatting requirements (minimal but strict for verification):
- Header row in `Route_Carrier_Summary` must be bold.
- `avg_arr_delay_min` and `worst_avg_arr_delay_min` must be numeric cells with number format `0.00`.
- The cross-sheet reference in `Answer` must be a real Excel formula string (e.g., `='Route_Carrier_Summary'!D2`), not a pasted value.

Writing the Excel file to the specified path is mandatory for completion.