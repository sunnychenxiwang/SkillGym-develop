Create a single machine-verifiable JSON “study fingerprint” that uniquely characterizes all **three** provided DICOM objects by combining (a) modality-specific semantic fields and (b) deterministic pixel statistics where applicable.

Using **pydicom** to read each file:

1. For **CT_small.dcm** and **MR_small.dcm** (image objects):
   - Extract these metadata fields (use `getattr(ds, name, None)` for missing):
     - `Modality`, `Manufacturer`, `PatientID`, `StudyDate`, `Rows`, `Columns`, `PixelSpacing`, `SliceThickness`
   - Compute pixel statistics from `ds.pixel_array` (after any needed decompression):
     - `min`, `max`, `mean`, `std` (population std, i.e., `ddof=0`)
     - `nonzero_count`
   - Also compute `pixel_md5`: MD5 hash of the raw `PixelData` bytes (not the numpy array bytes).

2. For **rtplan.dcm** (RT Plan object; no pixel data expected):
   - Extract these semantic plan fields:
     - `Modality`, `RTPlanName`, `ApprovalStatus`, `PatientID`, `PatientPosition`
     - `BeamCount` = number of items in `BeamSequence` (0 if missing)
     - `TotalMeterset` = sum of `FinalCumulativeMetersetWeight` across all beams where present (treat missing as 0; result as float)

3. Combine results across all three files into **one** JSON object with this exact schema and ordering:
```json
{
  "CT_small.dcm": { ... },
  "MR_small.dcm": { ... },
  "rtplan.dcm": { ... },
  "cross_file_checks": {
    "patient_id_all_equal": true,
    "modalities": ["CT", "MR", "RTPLAN"],
    "earliest_study_date": "YYYYMMDD"
  }
}
```
- `patient_id_all_equal` must compare the extracted `PatientID` values across all three datasets (string equality; if any missing, treat as not equal).
- `modalities` must be the sorted unique list of the three `Modality` values.
- `earliest_study_date` must be the minimum non-null `StudyDate` across the three files (DICOM DA string), unchanged.

Write the JSON (UTF-8, pretty-printed with 2-space indentation, sorted keys **disabled**) to:

`/root/dicom_study_fingerprint.json`

Saving this file is mandatory for completion.