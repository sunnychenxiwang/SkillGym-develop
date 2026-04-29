Parse **all three** MATPOWER case files:

- `/root/case57.m`
- `/root/case118.m`
- `/root/pglib_opf_case118_ieee.m`

Build a **NetworkX undirected graph** for each case using only **in-service branches** (`status == 1`) and treating each branch as an unweighted edge between `fbus` and `tbus` (ignore parallel-edge multiplicity by collapsing to a simple graph). For each graph, compute **edge betweenness centrality** and identify the **single edge** with the maximum value; if there is a tie, break it deterministically by choosing the edge with the lexicographically smallest `(min(fbus,tbus), max(fbus,tbus))`.

Then, for each case, run a **DC power flow** (baseMVA from the case). Use:
- bus numbering via a proper `bus_num_to_idx` mapping (do not assume contiguous numbering),
- branch reactance `x` to form susceptance,
- net injections `P = Pg - Pd` (sum all generators at a bus; use Pd from bus table),
- select the slack/reference bus as the **unique bus with type == 3**,
- solve for voltage angles with the slack angle fixed at 0,
- compute the **MW flow on the identified max-edge-betweenness edge** using `flow_MW = (theta[f]-theta[t])*(1/x)*baseMVA` with the sign defined from `fbus -> tbus` as listed in the file (use that direction for reporting).

Create a single Excel workbook at:

`/root/critical_edge_dcflow_report.xlsx`

with these requirements:

1) Sheet `Summary` containing exactly one table with columns:
- `case_file` (the basename)
- `n_bus`
- `n_branch_in_service`
- `critical_edge_fbus`
- `critical_edge_tbus`
- `critical_edge_edge_betweenness`
- `critical_edge_flow_MW`

2) Apply financial-model styling conventions:
- Header row: bold black font, light gray fill.
- All numeric input cells (directly written numbers, not formulas) in the table: **blue font**.
- No other sheets or outputs.

The workbook content must be fully reproducible and uniquely determined by the three input files. Writing the Excel file to the specified path is mandatory.