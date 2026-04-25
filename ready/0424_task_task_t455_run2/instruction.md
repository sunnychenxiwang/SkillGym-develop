Using `/root/flights_2.csv` and `/root/airlines.csv`, identify the **single airline (by full name)** whose flights have the **strongest positive relationship between route distance and departure delay** in this dataset, under the following deterministic rules:

1. Keep only rows where `dep_delay` and `distance` are both present (not `NA`) and `distance > 0`.
2. Consider only carriers that have **at least 30 qualifying flights** after filtering.
3. For each remaining carrier, fit an **OLS regression**: `dep_delay ~ distance` (with intercept) and compute the **slope coefficient for `distance`**.
4. Select the carrier with the **largest positive slope**. If there is a tie, break it by choosing the carrier with the **larger qualifying-flight count**; if still tied, choose the **lexicographically smallest carrier code**.
5. Map the winning `carrier` code to its airline full name using `airlines.csv` (`Code` -> `Description`). If the code is not found, use `null` for the description (but still report the code).

Write exactly one JSON file to:
`/root/output/steepest_distance_delay_carrier.json`

with this exact schema (no extra keys):
```json
{
  "carrier_code": "XX",
  "carrier_name": "Full Airline Name or null",
  "n_flights": 123,
  "distance_slope": 0.012345
}
```

Requirements:
- `distance_slope` must be the fitted OLS slope for `distance` rounded to **6 decimal places**.
- `n_flights` must be the qualifying-flight count used for that carrier’s regression.