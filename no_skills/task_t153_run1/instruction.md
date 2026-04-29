Using **all three** provided threat reports:

- `/root/ASD-Cyber-Threat-Report-2024.pdf`
- `/root/RedCanary-Threat-Detection-Report-2024.pdf`
- `/root/Secureworks-State-of-the-Threat-Report-2024.pdf`

create a single machine-verifiable JSON artifact that identifies the **one MITRE ATT&CK technique ID (format `T####` or `T####.###`) that is mentioned in the greatest number of the three PDFs**, and report exactly **which PDFs mention it**.

Rules/requirements (to ensure a unique, checkable result):

1. **Technique extraction**
   - Extract all substrings matching regex: `\bT\d{4}(?:\.\d{3})?\b` from the full text of each PDF.
   - Normalize by uppercasing (e.g., `t1059` → `T1059`).

2. **Cross-file counting**
   - For each technique ID, compute in how many distinct PDFs it appears (document frequency across the 3 files; multiple mentions in the same PDF still count as 1).

3. **Winner selection (deterministic tie-break)**
   - Choose the technique with the **highest document frequency**.
   - If there is a tie, choose the tied technique with the **highest total mention count across all PDFs** (sum of per-PDF counts).
   - If still tied, choose the **lexicographically smallest** technique ID string.

4. **Output file (mandatory)**
   - Save the result to exactly:
     - `/root/most_common_attack_technique.json`

5. **JSON schema (must match exactly)**
```json
{
  "technique_id": "T###