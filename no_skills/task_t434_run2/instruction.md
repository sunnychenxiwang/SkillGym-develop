Compute a **single, uniquely defined “most critical transmission element”** across the IEEE 118-bus cases by combining topology/ratings from **both** `case118.m` and `pglib_opf_case118_ieee.m`, and using `case57.m` to define the comparison baseline.

1) Parse all three MATPOWER case files and extract `baseMVA`, `bus`, `gen`, and `branch` tables.
2) For **each** 118-bus file (`case118.m` and `pglib_opf_case118_ieee.m`), run a **DC power flow** with:
   - Slack bus = the bus with `type == 3`
   - Net injection at each bus = (sum of online `Pg` at that bus) − `Pd`
   - Build the susceptance matrix `B` from **in-service** branches (`status == 1`) using series reactance `x` (ignore `r`, `b`, taps/phase shift; treat each branch as `b = 1/x`)
   - Solve for bus angles (slack angle = 0), then compute each branch real power flow (MW) as  
     `flow_MW = (1/x) * (theta_f - theta_t) * baseMVA`
   - Compute branch loading percent using `rateA` as the rating:  
     `loading_pct = abs(flow_MW) / rateA * 100`  
     (If `rateA <= 0`, exclude that branch from consideration.)
3) For each 118-bus file, identify the **single branch with the maximum `loading_pct`**. If there is a tie, break it deterministically by choosing the branch with the smallest `(min(fbus,tbus), max(fbus,tbus))` lexicographic pair, and if still tied, the smallest original branch row index.
4) Use `case57.m` to compute the **baseline median branch reactance**: median of `x` over in-service branches with `x > 0`. (This is only used as a normalization constant.)
5) Define the **criticality score** for each 118-bus file’s max-loaded branch as:  
   `criticality = loading_pct / (x / median_x_case57)`  
   where `median_x_case57` is from step (4) and `x` is that branch’s reactance in the corresponding 118-bus file.
6) Choose the **single overall winner** between the two 118-bus files: the branch (and source file) with the larger `criticality`. If tied, prefer `pglib_opf_case118_ieee.m`.

Write the final result **as a JSON file** to:

`/root/most_critical_branch.json`

with exactly this schema:

```json
{
  "winner_source_file": "case118.m or pglib_opf_case118_ieee.m",
  "fbus": 0,
  "tbus": 0,
  "branch_row_index": 0,
  "x": 0.0,
  "rateA": 0.0,
  "flow_MW": 0.0,
  "loading_pct": 0.0,
  "median_x_case57": 0.0,
  "criticality": 0.0
}
```

All numeric values must be JSON numbers (not strings) and should be written with reasonable floating precision. Writing this file is mandatory for completion.