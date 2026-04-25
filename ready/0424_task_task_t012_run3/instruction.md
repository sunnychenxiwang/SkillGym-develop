Build a **deterministic “most critical line” identifier** by combining DC power-flow results with graph-theoretic criticality across all three provided MATPOWER cases, then save the single winning record as JSON.

1. Parse these three files as MATPOWER cases (bus + branch tables at minimum):
   - `/root/case57.m`
   - `/root/case118.m`
   - `/root/pglib_opf_case118_ieee.m`

2. For each case:
   - Build the DC susceptance matrix **B** from branch reactances (ignore/skip branches with `x == 0` or `status == 0`).
   - Solve a DC power flow with:
     - net injections \(P\) computed as (sum of generator Pg at bus) − (bus Pd), in MW, converted to per-unit on `baseMVA`.
     - slack bus = the unique bus with `type == 3` (set its angle to 0 and remove its equation to solve).
   - Compute MW flow on every in-service branch using \(F_{f\to t} = (1/x)\,(\theta_f-\theta_t)\,\text{baseMVA}\).
   - Build an undirected NetworkX graph of the in-service topology (buses as nodes, branches as edges) and compute **edge betweenness centrality** on that graph.

3. Define each branch’s **criticality score** as:
   \[
   \text{score} = |F_{f\to t}|\times \text{edge\_betweenness}(f,t)
   \]
   (use the edge betweenness value for that undirected edge).

4. Across **all branches in all three cases**, find the single branch with the **maximum score**.  
   Tie-break deterministically in this exact order:
   1) higher `score`  
   2) higher `abs_flow_mw`  
   3) lexicographically smaller `case_name` (one of: `case57`, `case118`, `pglib_opf_case118_ieee`)  
   4) smaller `fbus`  
   5) smaller `tbus`

5. Write exactly one JSON file to:
   - `/root/output/most_critical_branch.json`

The JSON must have this exact schema (numbers as JSON numbers, not strings):
```json
{
  "case_name": "case57",
  "fbus": 0,
  "tbus": 0,
  "abs_flow_mw": 0.0,
  "edge_betweenness": 0.0,
  "score": 0.0
}
```
This file is the only required deliverable.