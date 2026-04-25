Using the 2014 flight records in `/root/flights_2.csv`, determine **which carrier had the best on‑time performance on the SEA→LAX route across the entire year 2014**, where “on‑time” is defined as **arrival delay ≤ 15 minutes** and **cancelled flights (missing `arr_delay`) are excluded**.

Then, use the airline reference table in `/root/airlines.csv` to map that winning carrier’s code to its full airline name.

Save a single JSON file to **`/root/output/sea_lax_best_carrier_2014.json`** with exactly this schema:

```json
{
  "route": "SEA-LAX",
  "year": 2014,
  "winning_carrier_code": "XX",
  "winning_carrier_name": "Full Airline Name",
  "on_time_rate": 0.0,
  "total_flights_included": 0
}
```

Requirements:
- `on_time_rate` must be a decimal proportion in \[0,1\] computed as (on-time included flights) / (included flights).
- “Included flights” = all SEA→LAX flights in 2014 with non-null `arr_delay`.
- If there is a tie for best on-time rate, break ties by **higher `total_flights_included`**, then by **lexicographically smallest `winning_carrier_code`**.
- The JSON must contain only the keys shown above (no extras).