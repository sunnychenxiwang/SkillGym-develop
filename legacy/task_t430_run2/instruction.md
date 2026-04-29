Parse **all three** MATPOWER case files (`case57.m`, `case118.m`, `pglib_opf_case118_ieee.m`) and compute a **single, uniquely determined “topological signature”** for each network based on DC power-flow-ready topology, then identify which two cases are **most similar** by that signature.

**Definition (must follow exactly):**
1. For each case, read `mpc.baseMVA`, `mpc.bus`, and `mpc.branch`.
2. Keep only **in-service** branches (`status == 1`).
3. Treat the network as an **undirected multigraph** on bus numbers (parallel lines count separately).
4. For each bus, compute its **degree** = number of in-service incident branches (count multiplicity).
5. Build the **degree histogram** as a mapping `{degree_value: count_of_buses_with_that_degree}`.
6. Convert the histogram into a deterministic vector by sorting by `degree_value` ascending and listing counts in that order (degrees with zero count are omitted).
7. Define the **signature distance** between two cases as the **L1 distance** between their histograms over the union of degree keys:
   \[
   d(A,B)=\sum_{k \in K} |count_A(k)-count_B(k)|
   \]
8. Compute all three pairwise distances and select the pair with the **smallest** distance (break ties by lexicographic order of the pair’s filenames).

**Deliverable (single file, mandatory):**  
Write `/root/degree_signature_result.json` with exactly this schema:

```json
{
  "case_signatures": {
    "case57.m": { "n_buses": 0, "n_in_service_branches": 0, "degree_histogram": { "0": 0 } },
    "case118.m": { "n_buses": 0, "n_in_service_branches": 0, "degree_histogram": { "0": 0 } },
    "pglib_opf_case118_ieee.m": { "n_buses": 0, "n_in_service_branches": 0, "degree_histogram": { "0": 0 } }
  },
  "pairwise_L1_distances": {
    "case57.m__case118.m": 0,
    "case57.m__pglib_opf_case118_ieee.m": 0,
    "case118.m__pglib_opf_case118_ieee.m": 0
  },
  "most_similar_pair": {
    "files": ["<fileA>", "<fileB>"],
    "distance": 0
  }
}
```

Notes:
- Bus numbers may be non-contiguous; you must correctly map them when counting degrees.
- Do **not** run an OPF/AC solver; this task is purely topology extraction from the provided files.
- The JSON must contain the **actual computed integers** (no placeholders) and be deterministic.