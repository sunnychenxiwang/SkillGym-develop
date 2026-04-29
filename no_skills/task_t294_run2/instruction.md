Using **both** `/root/flights_2.csv` and `/root/airlines.csv`, identify the **single airline (by carrier code)** that has the **highest cancellation rate** in `flights_2.csv`, where a flight is considered **cancelled** if `arr_delay` is `"NA"` (string NA in the CSV). Compute:

- `total_flights` per carrier (all rows for that carrier)
- `cancelled_flights` per carrier (`arr_delay` == NA)
- `cancellation_rate = cancelled_flights / total_flights`

Then **join** the winning carrier code to `airlines.csv` to obtain its `Description` (airline name). Save exactly one JSON file to:

`/root/highest_cancellation_airline.json`

with this exact schema (numbers must be numeric types, not strings):

```json
{
  "carrier": "XX",
  "airline_name": "Full Airline Name",
  "total_flights": 0,
  "cancelled_flights": 0,
  "cancellation_rate": 0.0
}
```

Tie-break rule (to ensure a unique, verifiable answer): if multiple carriers share the same highest `cancellation_rate`, choose the one with the **largest** `total_flights`; if still tied, choose the **lexicographically smallest** `carrier` code.