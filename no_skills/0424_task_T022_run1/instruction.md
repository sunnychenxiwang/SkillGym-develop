Using `/root/iris.csv`, build a **species-level factor profile** by (1) standardizing the four numeric measurement columns, (2) choosing the number of factors via the **Kaiser criterion** (count of eigenvalues > 1 computed from an unrotated fit), (3) fitting a **varimax-rotated** FactorAnalyzer model with that factor count, and (4) computing factor scores for every row and then the **mean factor score per species**.

Save a single JSON file to:

`/root/output/iris_species_factor_profile.json`

with exactly this schema (and no extra keys):

```json
{
  "n_factors": 0,
  "species_order": ["setosa", "versicolor", "virginica"],
  "mean_factor_scores": {
    "setosa": [0.0],
    "versicolor": [0.0],
    "virginica": [0.0]
  }
}
```

Requirements:
- `n_factors` must be the Kaiser-derived factor count.
- `species_order` must be the three species sorted alphabetically exactly as shown.
- In `mean_factor_scores`, each species’ list must contain `n_factors` floats in factor index order (Factor1..FactorN), computed from row-level scores and averaged within species.
- Round every float in `mean_factor_scores` to **6 decimal places** before writing the JSON.