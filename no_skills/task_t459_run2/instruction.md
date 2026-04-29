Create a single Excel workbook that **validates RTPLAN references against the available CT and MR images** and outputs a **deterministic pass/fail verdict**.

1) Read `/root/rtplan.dcm` with **pydicom** and extract every UID-like reference found in the plan that could point to imaging objects (e.g., any element whose keyword contains `UID` and whose value matches a DICOM UID pattern, including values inside sequences). Deduplicate these referenced UIDs.

2) Read `/root/CT_small.dcm` and `/root/MR_small.dcm` with **pydicom** and collect their identifiers:
- `StudyInstanceUID`
- `SeriesInstanceUID`
- `SOPInstanceUID`
- `SOPClassUID`
Also record `Modality`, `Rows`, `Columns`, and `PixelSpacing` (if present).

3) Using **data-transform (pandas)**, build a single table where each row is one referenced UID from the RTPLAN with these columns:
- `referenced_uid`
- `uid_type_detected` (one of: `StudyInstanceUID`, `SeriesInstanceUID`, `SOPInstanceUID`, `Other/Unknown` based on matching against the CT/MR identifiers)
- `matched_file` (one of: `CT_small.dcm`, `MR_small.dcm`, or blank)
- `matched_identifier_field` (which of the CT/MR fields it matched, or blank)
- `match_status` (`MATCH` or `NO_MATCH`)

4) Compute a single overall verdict:
- `PASS` if **every** referenced UID extracted from the RTPLAN is a `MATCH` to at least one of the CT/MR identifiers collected in step (2)
- otherwise `FAIL`

5) Write a styled Excel report to **exactly**:
`/root/rtplan_reference_validation.xlsx`

The workbook must contain:
- Sheet `Summary` with:
  - Cell `B2`: the overall verdict (`PASS`/`FAIL`)
  - Cell `B3`: total referenced UID count
  - Cell `B4`: matched count
  - Cell `B5`: unmatched count
  - Apply Excel styling conventions from the exploration summary: `B2` yellow fill if `FAIL`, green fill if `PASS`; bold headers.
- Sheet `UID_Matches` containing the full table from step (3), with header row bold and autofit-ish column widths (set reasonable fixed widths).

This task is only complete if the Excel file is written to the specified path and the verdict is reproducible solely from the three provided DICOM files.