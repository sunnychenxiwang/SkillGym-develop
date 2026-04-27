Using **both** `/root/flights_2.csv` (flight records) and `/root/airlines.csv` (carrier code → airline name mapping), identify the **single airline (by full Description name)** that has the **highest “delay burden”** for January 2014 flights in the dataset, where:

- Consider only rows where both `dep_delay` and `arr_delay` are present (i.e., not `NA`).
- For each flight row, define `delay_burden = max(dep_delay, 0) + max(arr_delay, 0)` (early/negative delays contribute 0).
- For each carrier, compute:
  - `total_delay_burden` = sum of `delay_burden` across its flights
  - `flight_count` = number of included flights
  - `avg_delay_burden` = `total_delay_burden / flight_count`
- Select the **airline with the maximum `avg_delay_burden`**.
- Break ties deterministically by choosing the carrier with the **lexicographically smallest carrier code**.

Then **write exactly one JSON file** to:

`/root/max_avg_delay_burden_airline.json`

with this exact schema (no extra keys):

```json
{
  "carrier_code": "XX",
  "airline_name": "Full Airline Description",
  "avg_delay_burden": 0.0,
  "total_delay_burden": 0.0,
  "flight_count": 0
}
```

Numeric values must be written as JSON numbers rounded to **2 decimal places**.