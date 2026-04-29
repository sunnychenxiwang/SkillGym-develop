Using the three MATPOWER case files `/root/case57.m`, `/root/case118.m`, and `/root/pglib_opf_case118_ieee.m`, compute a **single, uniquely determined “most critical transmission corridor”** as follows:

1. For each file, parse the bus and branch tables, build the DC susceptance matrix from branch reactances, solve a DC power flow using net real-power injections (generation minus load) with the slack bus angle fixed at 0, and compute MW flow on every in-service branch.
2. For each file, also build a NetworkX graph of the network topology (buses as nodes, in-service branches as edges) and compute **edge betweenness centrality** for every branch.
3. For each file, rank branches by the **severity score**  
   \[
   \text{severity} = |\text{MW\_flow}| \times \text{edge\_betweenness}
   \]
   and select the single top-ranked branch. Represent a branch by the ordered pair `(min(fbus,tbus), max(fbus,tbus))` so it is direction-independent.
4. Across the three per-file winners, select the **overall winner** by the **largest normalized severity**, where normalization divides each file’s winning severity by that file’s total system load (sum of Pd over all buses). Break ties deterministically by: higher raw severity, then lexicographically smaller `(bus_u, bus_v)`, then file name order `case57.m`, `case118.m`, `pglib_opf_case118_ieee.m`.

Write the final result to the mandatory artifact:

`/root/output/most_critical_corridor.json`

with exactly this schema:

```json
{
  "overall_winner": {
    "source_file": "case57.m|case118.m|pglib_opf_case118_ieee.m",
    "bus_u": 0,
    "bus_v": 0,
    "mw_flow_abs": 0.0,
    "edge_betweenness": 0.0,
    "severity": 0.0,
    "total_load_mw": 0.0,
    "normalized_severity": 0.0
  },
  "per_file_winners": [
    {
      "source_file": "case57.m",
      "bus_u": 0,
      "bus_v": 0,
      "mw_flow_abs": 0.0,
      "edge_betweenness": 0.0,
      "severity": 0.0,
      "total_load_mw": 0.0,
      "normalized_severity": 0.0
    },
    {
      "source_file": "case118.m",
      "bus_u": 0,
      "bus_v": 0,
      "mw_flow_abs": 0.0,
      "edge_betweenness": 0.0,
      "severity": 0.0,
      "total_load_mw": 0.0,
      "normalized_severity": 0.0
    },
    {
      "source_file": "pglib_opf_case118_ieee.m",
      "bus_u": 0,
      "bus_v": 0,
      "mw_flow_abs": 0.0,
      "edge_betweenness": 0.0,
      "severity": 0.0,
      "total_load_mw": 0.0,
      "normalized_severity": 0.0
    }
  ]
}
```

All numeric values must be JSON numbers (not strings) and must be computed from the case data (no placeholders). Writing this file is required for completion.