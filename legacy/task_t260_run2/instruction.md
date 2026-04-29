Create a **single JSON artifact** that deterministically identifies and counts the SharpDocx tutorial’s *major sections*, while also proving you correctly recognized which of the other three DOCX files are **not** SharpDocx documentation.

1) Read **`/root/input/Tutorial.docx`** and extract the **14 Table-of-Contents section titles** in their original order (these are the tutorial’s major sections). Treat the TOC entries as the ground truth list of section titles.

2) For each of the other three files:
- **`/root/input/sample-word-document.docx`**
- **`/root/input/sample.docx`**
- **`/root/input/template.docx`**

Extract the full raw text and compute a boolean `contains_sharpdocx_keyword` that is **true** if (case-insensitive) the text contains the substring `"sharpdocx"` anywhere, otherwise **false**.

3) Save exactly one file at:
**`/root/sharpdocx_toc_and_keyword_check.json`**

with this exact schema:

```json
{
  "tutorial_toc": {
    "section_count": 14,
    "sections": [
      "SECTION_TITLE_1",
      "SECTION_TITLE_2"
    ]
  },
  "other_files_keyword_check": [
    {
      "file": "sample-word-document.docx",
      "contains_sharpdocx_keyword": false
    },
    {
      "file": "sample.docx",
      "contains_sharpdocx_keyword": false
    },
    {
      "file": "template.docx",
      "contains_sharpdocx_keyword": false
    }
  ]
}
```

Constraints:
- `section_count` must equal the length of `sections` and must be **14**.
- `sections` must be the **exact TOC titles** as they appear in `Tutorial.docx` (preserve capitalization/punctuation).
- `other_files_keyword_check` must list the three non-tutorial files in the exact filename order shown above.
- Do not include any extra keys in the JSON. Writing the JSON file to the specified path is mandatory.