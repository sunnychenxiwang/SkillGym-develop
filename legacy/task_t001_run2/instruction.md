Create a **single JSON artifact** that quantifies how consistently the three provided documents represent the **quadratic formula** in LaTeX.

1. From each file:
   - `/root/01-basic-example.md`
   - `/root/sample.md`
   - `/root/examples.md` (note: HTML source)
   
   extract every LaTeX math snippet that contains the quadratic-formula structure (i.e., an `x = ...` expression featuring `\pm` and a square root term).

2. For every extracted snippet, **normalize it into a canonical SymPy expression** for \(x\) (treat `a,b,c` as symbols; ignore whitespace and purely presentational LaTeX differences). Use SymPy to parse/construct expressions and simplify them.

3. Using SymPy, verify equivalence by simplifying the difference between each snippet’s parsed expression and the canonical quadratic formula:
\[
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\]
Count a snippet as “equivalent” only if SymPy proves it matches (up to algebraic simplification and the standard meaning of `\pm` as two branches).

4. Save the results to **exactly** this path (writing the file is mandatory):
`/root/quadratic_formula_consistency.json`

The JSON must have this exact schema (and only these keys):

```json
{
  "canonical_latex": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
  "files": {
    "01-basic-example.md": { "snippets_found": 0, "snippets_equivalent": 0 },
    "sample.md": { "snippets_found": 0, "snippets_equivalent": 0 },
    "examples.md": { "snippets_found": 0, "snippets_equivalent": 0 }
  },
  "total_snippets_found": 0,
  "total_snippets_equivalent": 0
}
```

Use all three files: each file must contribute to `snippets_found` (even if that contribution is zero after deterministic extraction), and totals must equal the sum across the three per-file counts.