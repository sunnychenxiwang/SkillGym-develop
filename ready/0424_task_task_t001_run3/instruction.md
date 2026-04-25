Create a single JSON artifact that identifies the **one LaTeX math expression** that is **present in both** `/root/01-basic-example.md` and `/root/sample.md`, but **does not appear anywhere** in `/root/examples.md` (note: this file is an HTML capture of a GitHub page).

Define “math expression” as the exact LaTeX content inside any of these delimiters: `$...$`, `$$...$$`, or fenced ```math blocks. Treat whitespace differences as insignificant (normalize by collapsing all whitespace runs to a single space and trimming ends), but otherwise require exact string equality after normalization.

Then, using symbolic math, **simplify the identified expression** and compute the **sum of all distinct integer constants** appearing in the simplified form (e.g., in `x**2 + 2*x + 1`, the distinct integer constants are `{2, 1}` and the sum is `3`). If the simplified expression contains no integer constants, the sum is `0`.

Save the result to exactly this path (writing the file is mandatory):

`/root/output/shared_math_fingerprint.json`

with this exact schema:

```json
{
  "normalized_expression": "string",
  "simplified_expression": "string",
  "sum_distinct_integer_constants": 0
}
```

Constraints:
- `normalized_expression` must be the normalized LaTeX string you matched across the two markdown documents.
- `simplified_expression` must be a deterministic string form of the simplified symbolic expression (use SymPy’s default `str()` of the SymPy expression).
- The JSON must be valid, with keys in the exact order shown above.