Create a single **alignment report** that determines which of the three non-template DOCX files best matches the **structure required by** `/root/template.docx`, and prove the choice with a uniquely checkable score.

1) Use `markitdown` (or equivalent docx text extraction) on **all four** input files:
- `/root/template.docx`
- `/root/Tutorial.docx`
- `/root/sample-word-document.docx`
- `/root/sample.docx`

2) From `template.docx`, extract the **required section-heading set** by identifying headings (e.g., lines styled/represented as headings in the extracted markdown; if style info is missing, treat standalone title-cased/colon-terminated section lines as headings). Normalize headings by lowercasing and stripping punctuation/extra whitespace.

3) For each of the other three documents, extract its heading set using the **same normalization rules**, then compute:
- `matched_headings`: count of template headings present in the document (exact match after normalization)
- `missing_headings`: count of template headings absent from the document
- `extra_headings`: count of document headings not in the template
- `alignment_score = matched_headings * 2 - missing_headings - extra_headings`

4) Select the single **best-matching document** as the one with the **highest** `alignment_score`. Break ties deterministically by choosing the document with the lexicographically smallest filename.

5) Save exactly one JSON file to:
`/root/template_alignment.json`

with this exact schema (and no additional top-level keys):
```json
{
  "template_headings": ["..."],
  "documents": [
    {
      "filename": "Tutorial.docx",
      "matched_headings": 0,
      "missing_headings": 0,
      "extra_headings": 0,
      "alignment_score": 0
    },
    {
      "filename": "sample-word-document.docx",
      "matched_headings": 0,
      "missing_headings": 0,
      "extra_headings": 0,
      "alignment_score": 0
    },
    {
      "filename": "sample.docx",
      "matched_headings": 0,
      "missing_headings": 0,
      "extra_headings": 0,
      "alignment_score": 0
    }
  ],
  "best_match_filename": "..."
}
```

The task is complete only if the JSON is written to the specified path and the `best_match_filename` is consistent with the computed scores.