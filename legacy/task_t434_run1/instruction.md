Using **all three MATPOWER case files** (`/root/harbor_workspaces/task_T434_run1/input/case57.m`, `/root/harbor_workspaces/task_T434_run1/input/case118.m`, `/root/harbor_workspaces/task_T434_run1/input/pglib_opf_case118_ieee.m`), compute a **DC power flow** for each case and identify the **single most thermally overloaded in-service branch** across the three runs, where overload is defined as the maximum value of:

\[
\text{loading\_pct} = \frac{|P_{f\to t}|\_\text{MW}}{\text{rateA}\_\text{MW}} \times 100
\]

Rules/requirements (must be followed exactly for determinism):

1. **Parsing & filtering (all files):**
   - Parse `mpc.baseMVA`, `mpc.bus`, `mpc.gen`, `mpc.branch` from each `.m` file.
   - Use only branches with `status == 1`.
   - Use DC model susceptance `b = 1/x` using the branch `x` column; ignore `r`, `b`, transformer `ratio`, and `angle` (treat as 1 and 0).
   - Treat `rateA == 0` as “no limit” and exclude those branches from overload consideration (but they may still be used in the B matrix).

2. **Bus injections (all files):**
   - Net real injection at each bus (MW) is `Pg_total_at_bus - Pd`.
   - Compute `Pg_total_at_bus` by summing `Pg` for all generators at that bus with `status == 1`.
   - Use the bus `Pd` column for demand.

3. **Slack bus:**
   - Use the bus with `type == 3` as slack (exactly one per case). Solve DC PF with slack angle fixed to 0.

4. **Solve & flows:**
   - Build the full B matrix from in-service branches.
   - Solve for bus angles `theta` (radians) for non-slack buses.
   - Compute branch real power flow (MW) for each in-service branch as:
     \[
     P_{f\to t} = \left(\frac{1}{x}\right)\left(\theta_f - \theta_t\right)\cdot baseMVA
     \]
   - Use absolute value for loading.

5. **Cross-file winner selection:**
   - Find the branch (across all three cases) with the **maximum** `loading_pct`.
   - If there is a tie (exact same `loading_pct` up to full floating precision), break ties by:
     1) lexicographically smaller `case_name` (`case57`, `case118`, `pglib_opf_case118_ieee`),
     2) then smaller `branch_index` (0-based row index in `mpc.branch` as parsed).

6. **Final deliverable (mandatory):**
   - Write a single JSON file to:
     `/root/harbor_workspaces/task_T434_run1/output/most_overloaded_branch.json`
   - The JSON must have exactly this schema (numbers as JSON numbers, not strings):
```json
{
  "case_name": "case57|case118|pglib_opf_case118_ieee",
  "slack_bus": 0,
  "branch_index": 0,
  "fbus": 0,
  "tbus": 0,
  "rateA_MW": 0.0,
  "x_pu": 0.0,
  "flow_MW": 0.0,
  "loading_pct": 0.0
}
```

The task is complete only if that JSON file is created with the correctly computed single “most overloaded branch” result derived by combining computations from **all three** input files.