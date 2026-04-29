Parse **all three** MATPOWER case files:

- `/root/case57.m`
- `/root/case118.m`
- `/root/pglib_opf_case118_ieee.m`

Build a **single JSON artifact** that identifies the **most critical transmission corridor** that is *consistently critical across all three cases* using the following deterministic procedure:

1. For each case file, parse `mpc.bus` and `mpc.branch` and build an **undirected** NetworkX graph `G`:
   - Nodes = bus numbers (`bus_i`)
   - Edges = in-service branches only (`branch[:, 10] == 1`), with endpoints (`fbus`, `tbus`)
   - Treat parallel lines as a single undirected edge for centrality purposes (i.e., simple `nx.Graph()`; if multiple branches exist between the same buses, keep only one edge).

2. For each case’s graph, compute **edge betweenness centrality** (`nx.edge_betweenness_centrality(G, normalized=True)`).

3. For each case, take the **top 10 edges** by edge-betweenness centrality (descending). Represent an undirected edge canonically as the string `"minBus-maxBus"` (e.g., `"8-9"`).

4. Compute the **intersection** of these three top-10 sets (one set per file).  
   - If the intersection is empty, the task is considered failed (do not invent tie-breakers); otherwise continue.

5. From the intersection, select the single “winner” edge by:
   - For each candidate edge, compute its **average rank** across the three cases, where rank is its position in that case’s top-10 list (1 = highest centrality). If an edge is not present in a case’s top-10 list, it cannot be in the intersection, so this will not occur.
   - Choose the edge with the **lowest average rank**.
   - Break any remaining ties by choosing the lexicographically smallest canonical edge string.

6. Save the result to the file:

`/root/shared_critical_corridor.json`

with exactly this schema:

```json
{
  "winner_edge": "X-Y",
  "cases": {
    "case57.m": { "centrality": <number>, "rank": <int> },
    "case118.m": { "centrality": <number>, "rank": <int> },
    "pglib_opf_case118_ieee.m": { "centrality": <number>, "rank": <int> }
  },
  "intersection_size": <int>
}
```

Where:
- `"centrality"` is the edge betweenness value for that edge in that case (full precision as computed by NetworkX),
- `"rank"` is its rank (1–10) within that case’s top-10 list,
- `"intersection_size"` is the number of edges in the intersection before selecting the winner.

Writing the JSON file at the exact path above is mandatory for completion.