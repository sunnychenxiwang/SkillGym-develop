Create a single-slide PowerPoint “Imaging & RT Plan Consistency Card” that cross-references the two imaging DICOMs (`CT_small.dcm`, `MR_small.dcm`) with the RT Plan DICOM (`rtplan.dcm`) and reports one uniquely defined numeric result plus the supporting identifiers.

1) Read **all three** DICOM files and extract:
- From **CT_small.dcm** and **MR_small.dcm**: `Modality`, `Manufacturer`, `Rows`, `Columns`, `PixelSpacing` (both values), and (if present) `StudyDate`.
- From **rtplan.dcm**: `RTPlanName`, `PlanDate` (or closest available plan creation date tag), `PatientPosition`, and the **BeamSequence** energies (extract the numeric MV value(s) from the beam energy tag(s); if multiple beams/energies exist, use the maximum).

2) Compute a single metric called **FOV_area_mm2** for each imaging file:
- `FOV_x_mm = Columns * PixelSpacing[0]`
- `FOV_y_mm = Rows * PixelSpacing[1]`
- `FOV_area_mm2 = FOV_x_mm * FOV_y_mm`
Then compute **FOV_area_ratio_CT_over_MR = FOV_area_mm2(CT) / FOV_area_mm2(MR)** rounded to **6 decimal places**.

3) Perform one statistical check that must be based on the actual extracted values:
- Treat the two FOV areas as a 2-sample dataset and compute **Cohen’s d** for the difference (CT vs MR) using a standard independent-samples effect size definition. (With n=1 per group, handle this deterministically by using the pooled SD formula; if SD is zero/undefined, set `cohens_d` to `null`.)

4) Generate a PowerPoint at the exact path:
`/root/output/imaging_rtplan_card.pptx`

The slide must contain:
- A title: **“Imaging & RT Plan Consistency Card”**
- A 3-row table (CT, MR, RTPLAN) with the extracted key fields.
- A highlighted text box that shows exactly:
  - `FOV_area_ratio_CT_over_MR: <value>`
  - `MaxBeamEnergy_MV: <value>`
  - `cohens_d: <value or null>`

All numbers must be derived from the DICOM content (no hardcoding). Saving the PPTX file to the specified path is mandatory.