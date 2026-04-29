Using **both** `/root/flights_2.csv` and `/root/airlines.csv`, identify the **single airline (by full name)** that has the **highest mean arrival delay** on the **SEA → LAX** route **on 2014-01-01**, computed **only from flights with non-missing `arr_delay`** (treat `"NA"` as missing and exclude those rows).

Then write a JSON file to **exactly** this path:

`/root/sea_lax_worst_airline_2014-01-01.json`

with this exact schema (and no extra keys):

```json
{
  "date": "2014-01-01",
  "origin": "SEA",
  "dest": "LAX",
  "carrier_code": "XX",
  "carrier_name": "Full Airline Name",
  "mean_arr_delay_minutes": 0.0,
  "flight_count_used": 0
}
```

Rules for determinism:
- Filter rows to `year=2014`, `month=1`, `day=1`, `origin="SEA"`, `dest="LAX"`.
- Exclude any row where `arr_delay` is missing (`"NA"`).
- Compute the **arithmetic mean** of `arr_delay` per `carrier`.
- Choose the carrier with the **maximum** mean.
- If there is a tie in mean, break ties by **larger** `flight_count_used`; if still tied, choose the **lexicographically smallest** `carrier_code`.
- Map `carrier_code` to `carrier_name` by joining to `airlines.csv` on `Code`. If the code is not found, set `carrier_name` to the empty string.
- `mean_arr_delay_minutes` must be a JSON number rounded to **2 decimal places**.