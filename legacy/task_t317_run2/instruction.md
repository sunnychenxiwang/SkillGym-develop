Using **both** `/root/flights_2.csv` (flight performance data) and `/root/airlines.csv` (carrier code → airline name mapping), identify the **single airline (by full Description)** that had the **worst on-time performance** in this dataset, defined as the **highest mean arrival delay (`arr_delay`)** across all its flights **after excluding rows where `arr_delay` is missing/NA**.

Then save a compact, uniquely verifiable JSON artifact to:

`/root/worst_airline_by_mean_arr_delay.json`

with exactly this schema (keys in this order):

```json
{
  "carrier_code": "XX",
  "airline_description": "Full Airline Name",
  "flight_count_used": 123,
  "mean_arr_delay_minutes": 12.345
}
```

Requirements:
- Join `flights_2.csv.carrier` to `airlines.csv.Code` to populate `airline_description`.
- If `airlines.csv` contains duplicate `Code` values, resolve deterministically by using the **lexicographically smallest** `Description` for that `Code`.
- Compute `mean_arr_delay_minutes` as a floating-point value rounded to **3 decimal places**.
- The “worst” airline is the one with the **maximum** `mean_arr_delay_minutes`; break ties (if any) by choosing the **lexicographically smallest** `carrier_code`.
- `flight_count_used` must be the number of non-null `arr_delay` rows used for that carrier’s mean.