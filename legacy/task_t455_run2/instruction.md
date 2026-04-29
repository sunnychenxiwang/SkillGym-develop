Using `/root/flights_2.csv` and the carrier lookup table `/root/airlines.csv`, identify **the single airline (by full Description from airlines.csv)** with the **highest mean arrival delay** on the specific route **SEA → LAX** (consider **all dates in the file**).

Rules (must be followed exactly for a uniquely verifiable result):
1. Filter flights to `origin == "SEA"` and `dest == "LAX"`.
2. Exclude rows where `arr_delay` is missing (`NA`) or non-numeric.
3. Group by `carrier` and compute:
   - `n_flights` = number of remaining flights for that carrier on SEA→LAX
   - `mean_arr_delay` = arithmetic mean of `arr_delay`
4. Only consider carriers with `n_flights >= 5`.
5. Choose the carrier with the **largest** `mean_arr_delay`. Break ties (if any) by choosing the lexicographically smallest `carrier` code.
6. Join the winning `carrier` code to `airlines.csv` on `Code` to obtain the airline `Description`.

Write a single JSON file to **`/root/sea_lax_worst_airline.json`** with exactly this schema:

```json
{
  "route": "SEA-LAX",
  "carrier_code": "XX",
  "carrier_description": "Full Airline Name",
  "n_flights": 0,
  "mean_arr_delay": 0.0
}
```

`mean_arr_delay` must be a numeric JSON value (not a string) rounded to **2 decimal places**. Writing this file is mandatory for completion.