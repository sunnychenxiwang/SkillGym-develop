Parse **all three** MATPOWER case files (`case57.m`, `case118.m`, `pglib_opf_case118_ieee.m`) and determine the **single transmission branch (unordered bus pair i–j, ignoring direction)** that has the **largest absolute percentage change in series reactance `x`** between the two 118-bus datasets (`case118.m` vs `pglib_opf_case118_ieee.m`), **restricted to branches whose unordered bus pair also exists in the 57-bus case (`case57.m`)**.

Rules/definitions (must be followed exactly for determinism):
1. A “branch” is a row in `mpc.branch` with columns `[fbus, tbus, r, x, b, ...]`. Use the numeric `x` value as given.
2. Treat a branch as an **unordered pair**: `(min(fbus,tbus), max(fbus,tbus))`.
3. If multiple parallel branches exist for the same unordered pair within a case, use the **mean `x`** for that unordered pair in that case.
4. Consider only unordered pairs that appear in **all three** files (so `case57.m` acts as the filter set).
5. For each remaining unordered pair, compute:
   - `x_case118` = mean x in `case118.m`
   - `x_pglib` = mean x in `pglib_opf_case118_ieee.m`
   - `pct_change = abs(x_pglib - x_case118) / abs(x_case118)`  
   Exclude any pair where `x_case118 == 0` (to avoid division by zero).
6. Select the unordered pair with the **maximum `pct_change`**. Break ties deterministically by choosing the pair with the **smallest** `(bus_i, bus_j)` lexicographically.

Write the result to the file:

`/root/max_reactance_change.json`

with exactly this JSON schema (numbers as JSON numbers, not strings):
```json
{
  "bus_i": 0,
  "bus_j": 0,
  "x_case118": 0.0,
  "x_pglib": 0.0,
  "pct_change": 0.0
}
```

The task is complete only when that JSON file is created with the uniquely determined values computed from the three provided inputs.