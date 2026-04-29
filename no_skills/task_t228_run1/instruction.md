Parse **all three** MATPOWER case files:

- `/root/harbor_workspaces/task_T228_run1/input/case57.m`
- `/root/harbor_workspaces/task_T228_run1/input/case118.m`
- `/root/harbor_workspaces/task_T228_run1/input/pglib_opf_case118_ieee.m`

Build a NetworkX undirected graph for each case using **only in-service branches** (`status == 1`) and treating each branch as an edge between `fbus` and `tbus` (ignore parallel-edge distinctions for connectivity, i.e., a simple `nx.Graph()` is fine).

Your single objective is to identify the **unique “most critical bus” per case**, defined deterministically as:

1. Compute articulation points of the case graph (nodes whose removal increases the number of connected components).
2. For each articulation point `v`, compute the number of connected components in the graph after removing `v` (call this `k_v`).
3. Select the bus with the maximum `k_v`.
4. Break ties by:
   - higher betweenness centrality (computed on the original case graph),
   - then smaller bus number.

Then create a single Excel workbook at:

`/root/critical_bus_report.xlsx`

with exactly two sheets:

1) **Summary** (one row per case, in this order: `case57`, `case118`, `pglib_opf_case118_ieee`) with columns:
- `case_name`
- `n_buses`
- `n_branches_in_service`
- `critical_bus`
- `components_after_removal` (the selected `k_v`)
- `betweenness` (of `critical_bus`, numeric)

2) **Details** listing, for each case, the top 10 articulation points ranked by the same ordering used in the selection (max `k_v`, then betweenness, then bus number), with columns:
- `case_name`
- `bus`
- `components_after_removal`
- `betweenness`
- `degree`

Excel formatting requirements (must be applied):
- Header row bold with light gray fill.
- Numeric columns formatted as:
  - integers: `0`
  - betweenness: `0.000000`
- Freeze panes at row 2 on both sheets.
- Use the financial-model color convention: any cell containing an Excel formula must be black font; any hardcoded text labels (like headers) black; no blue/green/red required beyond this.

The workbook content must be fully populated from computations on the three provided files; do not include screenshots or external references. Writing the Excel file to the specified path is mandatory.