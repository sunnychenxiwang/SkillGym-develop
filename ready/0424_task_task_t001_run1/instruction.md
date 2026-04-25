Create a single JSON artifact that identifies the **unique LaTeX math expression that appears in all three input documents**, and compute a deterministic numeric signature from it.

1. Read `/root/01-basic-example.md`, `/root/sample.md`, and `/root/examples.md` (note: `examples.md` is HTML; extract only the human-visible page text and any embedded code/pre blocks before searching).
2. From each file, extract all LaTeX math expressions (both inline and display) and normalize them by:
   - removing surrounding delimiters (`$...$`, `$$...$$`, and fenced ```math blocks),
   - stripping all whitespace characters,
   - leaving the remaining characters unchanged.
3. Find the **intersection** of the three normalized-expression sets. It is guaranteed there is exactly **one** common normalized expression; call it `common_expr`.
4. Using SymPy, interpret `common_expr` as the quadratic formula in terms of symbols `a`, `b`, `c`, and compute the discriminant `D = b**2 - 4*a*c`. Then, using the Math skill’s Z3 capability, prove that for all real `a,b,c` with `a != 0` and `D >= 0`, the two roots produced by `common_expr` are real numbers (i.e., no imaginary unit is required). Encode the proof result as a boolean `roots_real_proved` that must be `true` only if Z3 establishes the theorem (unsat of the negation).
5. Also compute an integer `signature` defined as: substitute `a=1, b=5, c=6` into the two roots from `common_expr`, take the product of the two roots, and multiply by 1000, then round to the nearest integer.

Write exactly this JSON (no extra keys) to `/root/output/quadratic_common.json`:

```json
{
  "common_expr": "...",
  "roots_real_proved": true,
  "signature": 0
}
```

The task is complete only if the file is created at that exact path with the correct values.