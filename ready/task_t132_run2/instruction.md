Using **all three** PDF reports below:

- `/root/input/ASD-Cyber-Threat-Report-2024.pdf`
- `/root/input/RedCanary-Threat-Detection-Report-2024.pdf`
- `/root/input/Secureworks-State-of-the-Threat-Report-2024.pdf`

determine the **single MITRE ATT&CK technique ID (format `T####` or `T####.###`) that is mentioned in the greatest number of the three documents** (i.e., appears in 3 documents if possible; otherwise 2; otherwise 1). Count a technique as “mentioned” in a document if its **technique ID string** appears anywhere in that PDF’s extracted text (case-insensitive), regardless of whether the technique name also appears.

Then write exactly one JSON file to:

`/root/most_common_attack_technique.json`

with this exact schema:

```json
{
  "technique_id": "TXXXX",
  "documents_containing": 3,
  "per_document": {
    "ASD-Cyber-Threat-Report-2024.pdf": true,
    "RedCanary-Threat-Detection-Report-2024.pdf": true,
    "Secureworks-State-of-the-Threat-Report-2024.pdf": true
  }
}
```

Rules for determinism (must follow):
1. Extract text from each PDF (use the available PDF skill tooling).
2. Find all substrings matching regex `\bT\d{4}(?:\.\d{3})?\b` in each document’s text.
3. Compute, for each technique ID, in how many distinct documents it appears.
4. Select the technique with the **highest** `documents_containing`.
5. If there is a tie, break ties by:
   - choosing the technique with the **highest total occurrence count across all three documents**;
   - if still tied, choose the **lexicographically smallest** technique ID.
6. The JSON file must reflect the selected technique and correct booleans for each document filename.

Writing the JSON file to the specified path is mandatory for completion.