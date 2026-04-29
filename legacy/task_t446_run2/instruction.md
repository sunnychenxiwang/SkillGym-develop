Create a single machine-verifiable JSON “consistency check” artifact that proves the RT Plan’s referenced imaging context matches the two provided imaging DICOMs.

Using **pydicom** (and pandas/numpy from **data-transform** if helpful), do the following:

1. Read these three DICOM files:
   - `/root/harbor_workspaces/task_T446_run2/input/CT_small.dcm`
   - `/root/harbor_workspaces/task_T446_run2/input/MR_small.dcm`
   - `/root/harbor_workspaces/task_T446_run2/input/rtplan.dcm`

2. From `rtplan.dcm`, locate **all referenced SOP Instance UIDs** that appear anywhere inside sequences (e.g., in `Referenced...Sequence` items). Collect them into a set called `rtplan_referenced_sop_instance_uids`.

3. From `CT_small.dcm` and `MR_small.dcm`, extract each file’s `SOPInstanceUID`.

4. Compute:
   - `ct_is_referenced_by_rtplan`: true iff CT’s `SOPInstanceUID` is in `rtplan_referenced_sop_instance_uids`
   - `mr_is_referenced_by_rtplan`: true iff MR’s `SOPInstanceUID` is in `rtplan_referenced_sop_instance_uids`
   - `referenced_match_count`: how many of {CT, MR} are referenced (0, 1, or 2)
   - `rtplan_total_reference_count`: total number of unique SOP Instance UIDs referenced by the RT Plan (size of the set)

5. Save exactly the following JSON schema to this path (writing the file is mandatory):
   - Output file: `/root/rtplan_imaging_reference_check.json`

```json
{
  "ct_sop_instance_uid": "string",
  "mr_sop_instance_uid": "string",
  "rtplan_total_reference_count": 0,
  "ct_is_referenced_by_rtplan": false,
  "mr_is_referenced_by_rtplan": false,
  "referenced_match_count": 0
}
```

Constraints:
- The JSON values must be derived only from the three provided files.
- The result must be deterministic (no randomness, no timestamps).
- Do not include extra keys beyond the schema above.