Create a single JSON “patient/study/plan consistency verdict” that cross-references identifiers across the two imaging instances (CT_small.dcm, MR_small.dcm) and the RT plan (rtplan.dcm) to determine **which imaging file (CT or MR) is the intended match for the RT plan’s patient**, using a deterministic scoring rule.

**Required method (must use all 3 files):**
1. Read all three DICOMs with pydicom and extract these fields when present (use empty string if missing):  
   - `PatientName`, `PatientID`, `PatientSex`, `StudyID`, `StudyInstanceUID`
2. Compute two match scores: `score_ct_vs_plan` and `score_mr_vs_plan`, each as the sum of:
   - +3 if `PatientID` exactly matches plan `PatientID`
   - +2 if `PatientName` exactly matches plan `PatientName`
   - +1 if `PatientSex` exactly matches plan `PatientSex`
   - +1 if `StudyID` exactly matches plan `StudyID`
   - +1 if `StudyInstanceUID` exactly matches plan `StudyInstanceUID`
3. Choose `best_match_modality` as:
   - `"CT"` if `score_ct_vs_plan` > `score_mr_vs_plan`
   - `"MR"` if `score_mr_vs_plan` > `score_ct_vs_plan`
   - `"TIE"` if equal
4. Save exactly one JSON file at:  
   `/root/dicom_plan_match.json`

**JSON schema (must match exactly):**
```json
{
  "plan_patient_id": "...",
  "plan_patient_name": "...",
  "ct_patient_id": "...",
  "ct_patient_name": "...",
  "mr_patient_id": "...",
  "mr_patient_name": "...",
  "score_ct_vs_plan": 0,
  "score_mr_vs_plan": 0,
  "best_match_modality": "CT|MR|TIE"
}
```

Notes:
- The task is only complete if the JSON file is written to the specified path.
- Do not include any additional keys beyond the schema above.