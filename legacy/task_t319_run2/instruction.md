Using **both** `/root/flights_2.csv` (flight records) and `/root/airlines.csv` (carrier code → airline name), determine the **single (carrier, origin, dest)** route in January 2014 that has the **highest “delay burden”**, defined as:

> **delay_burden = (mean(dep_delay for that route, ignoring nulls)) × (number of flights on that route with non-null dep_delay)**

Constraints (to make the result uniquely verifiable):
1. Only include flights where `dep_delay` is not null.
2. Group by exactly `carrier`, `origin`, `dest` (ignore date/time fields after filtering).
3. Compute `mean(dep_delay)` as a floating-point mean.
4. Compute `delay_burden` as `mean_dep_delay * n_valid_dep_delay`.
5. If there is a tie on `delay_burden`, break ties deterministically in this order:
   - higher `mean_dep_delay`
   - then higher `n_valid_dep_delay`
   - then lexicographically smallest `carrier`, then `origin`, then `dest`

After identifying the winning route, **join** to `airlines.csv` to add the carrier’s full airline name (`Description`).

Write **exactly one JSON file** to:

`/root/highest_delay_burden_route.json`

with this exact schema (keys in this exact order):

```json
{
  "carrier": "AA",
  "airline_name": "American Airlines Inc.",
  "origin": "SEA",
  "dest": "ORD",
  "n_valid_dep_delay": 123,
  "mean_dep_delay": 12.34,
  "delay_burden": 1517.82
}
```

Numeric requirements:
- `n_valid_dep_delay` must be an integer.
- `mean_dep_delay` and `delay_burden` must be rounded to **2 decimal places** in the JSON.