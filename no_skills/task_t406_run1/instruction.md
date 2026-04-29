Using **all three MATPOWER case files** (`/root/case57.m`, `/root/case118.m`, `/root/pglib_opf_case118_ieee.m`), compute a **deterministic “critical corridor” ranking** as follows:

1. **Parse each file** to extract the `mpc.bus` and `mpc.branch` tables (use the case file’s own baseMVA; do not assume contiguous bus numbering).
2. For each case, run a **DC power flow** with:
   - Net injections \(P\) (in per-unit) computed as \((\text{sum Pg at bus} - \text{Pd at bus}) / \text{baseMVA}\).
   - Slack bus angle fixed at 0 (use the case’s type-3 bus; if multiple, use the lowest bus_i among type-3).
   - Branch susceptance \(b = 1/x\) using `mpc.branch` reactance column; ignore branches with `status = 0`; if any `x = 0`, exclude that branch from B-matrix and from flow calculations.
3. Compute **MW line flow** on every in-service branch as \(F_{f\to t} = (\theta_f - \theta_t)\cdot (1/x)\cdot \text{baseMVA}\).
4. For each case, identify the **single branch** with the **largest absolute MW flow**; record it as an undirected corridor key `(min(fbus,tbus), max(fbus,tbus))`.
5. Across the three cases, find the **unique corridor that appears in at least 2 of the 3 cases** among those “top-flow” branches. (The task is constructed so exactly one corridor satisfies this.)
6. Create an Excel workbook at exactly:
   - `/root/critical_corridor.xlsx`

The workbook must contain:
- Sheet `result` with exactly one row of data and these columns:
  - `corridor_fbus` (integer, the smaller bus number)
  - `corridor_tbus` (integer, the larger bus number)
  - `cases_where_topflow` (string: comma-separated among `case57`, `case118`, `pglib118`)
- Sheet `evidence` listing (one row per case) the top-flow branch for that case with columns:
  - `case` (as above)
  - `top_fbus`
  - `top_tbus`
  - `top_abs_flow_mw` (numeric, absolute value)
  - `top_flow_mw_signed` (numeric, signed flow from fbus to tbus as stored in file)
  - `baseMVA`

Saving the Excel file to the specified path is mandatory for completion.