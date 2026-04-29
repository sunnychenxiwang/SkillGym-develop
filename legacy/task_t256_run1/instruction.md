Create a **single JSON artifact** that identifies the **one MITRE ATT&CK technique ID (format `T####` or `T####.###`) that is mentioned in the greatest number of the three provided reports**, using **all three PDFs**:

- `/root/input/ASD-Cyber-Threat-Report-2024.pdf`
- `/root/input/RedCanary-Threat-Detection-Report-2024.pdf`
- `/root/input/Secureworks-State-of-the-Threat-Report-2024.pdf`

**Method constraints (to ensure a uniquely verifiable result):**
1. Extract text from each PDF (any reliable method from the available `pdf` skill is acceptable).
2. Detect ATT&CK technique IDs by regex: `\bT\d{4}(?:\.\d{3})?\b`.
3. For each technique ID, compute:
   - `doc_count`: in how many of the 3 PDFs it appears at least once (presence/absence per document, not total frequency).
   - `total_mentions`: total number of regex matches across all three PDFs combined.
4. Select the winner by:
   - Highest `doc_count`
   - Tie-breaker 1: highest `total_mentions`
   - Tie-breaker 2: lexicographically smallest technique ID (string compare)

**Write the result to this exact path (writing the file is mandatory):**
`/root/most_common_attack_technique.json`

**Required JSON schema (exact keys):**
```json
{
  "technique_id": "T####",
  "doc_count": 0,
  "total_mentions": 0,
  "per_document_mentions": {
    "ASD-Cyber-Threat-Report-2024.pdf": 0,
    "RedCanary-Threat-Detection-Report-2024.pdf": 0,
    "Secureworks-State-of-the-Threat-Report-2024.pdf": 0
  }
}
```