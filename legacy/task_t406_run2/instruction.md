Parse the three MATPOWER case files `/root/harbor_workspaces/task_T406_run2/input/case57.m`, `/root/harbor_workspaces/task_T406_run2/input/case118.m`, and `/root/harbor_workspaces/task_T406_run2/input/pglib_opf_case118_ieee.m` to compute a **single, uniquely defined network-stress metric** and save it as a compact JSON artifact.

**Primary objective (one metric):**  
For each case file, run a DC power flow using the branch reactances (`x`) and bus active demands (`Pd`) with the system baseMVA from the file, treating:
- the **slack bus** as the bus with type `3` in `mpc.bus` (use that as angle reference and remove its row/column when solving),
- net injections as `P_inj = (sum Pg at bus) - Pd` in MW, converted to per-unit by dividing by baseMVA,
- only **in-service branches** (`status == 1`),
- transformer `ratio` handling: if `ratio` is 0, treat as 1; otherwise use the given ratio when forming the DC B matrix (use standard DC transformer modeling: series susceptance scaled by `1/ratio` on off-diagonals and `1/ratio^2` on the “from” bus diagonal),
- ignore resistance `r`, line charging `b`, phase shift `angle` (DC approximation),
- handle non-contiguous bus numbering by building an explicit bus-id ↔ index map.

After solving bus angles, compute each branch’s MW flow (from-end) using DC approximation with transformer ratio handling, then compute the **Stress Index** for that case as:

> **Stress Index = 95th percentile of absolute branch MW flows divided by total system load (sum of Pd in MW)**

Finally, compute the **Comparative Stress Ratio**:

> **Comparative Stress Ratio = StressIndex(pglib_opf_case118_ieee) / StressIndex(case118)**

and also report the Stress Index for `case57` as a reference.

**Required output file (must be written):**  
Save exactly this JSON schema to:

`/root/powerflow_stress_metrics.json`

```json
{
  "case57": { "stress_index": 0.0 },
  "case118": { "stress_index": 0.0 },
  "pglib_opf_case118_ieee": { "stress_index": 0.0 },
  "comparative_stress_ratio_pglib_over_case118": 0.0
}
```

**Determinism requirements:**
- Use numpy’s percentile with linear interpolation (i.e., default behavior) and round all reported numeric values to **6 decimal places** in the JSON.
- If any branch has `x == 0`, exclude that branch from the B-matrix and from flow/stress calculations (to avoid singularities), but still include its buses in the network.

The task is complete only when the JSON file exists at the specified path and contains the computed values.