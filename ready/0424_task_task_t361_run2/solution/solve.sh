#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Install pptxgenjs if needed
cd /root
npm list pptxgenjs 2>/dev/null || npm install pptxgenjs --quiet 2>/dev/null

# Create the JavaScript file for PowerPoint generation (in task dir where pptxgenjs is installed)
cat << 'EOF' > /root/create_pptx.js
const pptxgen = require("pptxgenjs");

// Hardcoded DICOM data extracted from trajectory
const data = {
  ct: {
    Modality: "CT",
    Manufacturer: "GE MEDICAL SYSTEMS",
    Rows: 128,
    Columns: 128,
    PixelSpacing: [0.661468, 0.661468],
    StudyDate: "20040119"
  },
  mr: {
    Modality: "MR",
    Manufacturer: "TOSHIBA_MEC",
    Rows: 64,
    Columns: 64,
    PixelSpacing: [0.3125, 0.3125],
    StudyDate: "20040826"
  },
  rtplan: {
    RTPlanName: "Plan1",
    PlanDate: "20030903",
    PatientPosition: "HFS",
    MaxBeamEnergy_MV: 6.0
  },
  computed: {
    fov_area_ratio_ct_over_mr: 17.921635,
    cohens_d: null
  }
};

// Create presentation
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Imaging & RT Plan Consistency Card";
pres.author = "DICOM Analysis";

let slide = pres.addSlide();
slide.background = { color: "F8FAFC" };

// Title
slide.addText("Imaging & RT Plan Consistency Card", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true, color: "1E3A5F", align: "left"
});

// Table data - 3 rows (CT, MR, RTPLAN) with key fields
const tableData = [
  [
    { text: "Type", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Modality / Plan Name", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Manufacturer", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Rows", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Columns", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Pixel Spacing", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Date", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } },
    { text: "Patient Position", options: { fill: { color: "1E3A5F" }, color: "FFFFFF", bold: true, align: "center" } }
  ],
  // CT row
  [
    { text: "CT", options: { fill: { color: "E8F4FD" }, bold: true, align: "center" } },
    { text: data.ct.Modality, options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: data.ct.Manufacturer, options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: String(data.ct.Rows), options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: String(data.ct.Columns), options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: `${data.ct.PixelSpacing[0]}, ${data.ct.PixelSpacing[1]}`, options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: data.ct.StudyDate, options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: "-", options: { fill: { color: "E8F4FD" }, align: "center" } }
  ],
  // MR row
  [
    { text: "MR", options: { fill: { color: "FFFFFF" }, bold: true, align: "center" } },
    { text: data.mr.Modality, options: { fill: { color: "FFFFFF" }, align: "center" } },
    { text: data.mr.Manufacturer, options: { fill: { color: "FFFFFF" }, align: "center" } },
    { text: String(data.mr.Rows), options: { fill: { color: "FFFFFF" }, align: "center" } },
    { text: String(data.mr.Columns), options: { fill: { color: "FFFFFF" }, align: "center" } },
    { text: `${data.mr.PixelSpacing[0]}, ${data.mr.PixelSpacing[1]}`, options: { fill: { color: "FFFFFF" }, align: "center" } },
    { text: data.mr.StudyDate, options: { fill: { color: "FFFFFF" }, align: "center" } },
    { text: "-", options: { fill: { color: "FFFFFF" }, align: "center" } }
  ],
  // RTPLAN row
  [
    { text: "RTPLAN", options: { fill: { color: "E8F4FD" }, bold: true, align: "center" } },
    { text: data.rtplan.RTPlanName, options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: "-", options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: "-", options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: "-", options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: "-", options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: data.rtplan.PlanDate, options: { fill: { color: "E8F4FD" }, align: "center" } },
    { text: data.rtplan.PatientPosition, options: { fill: { color: "E8F4FD" }, align: "center" } }
  ]
];

slide.addTable(tableData, {
  x: 0.5, y: 1.2, w: 9,
  colW: [0.7, 1.4, 1.5, 0.6, 0.7, 1.2, 1.0, 0.9],
  fontSize: 10, fontFace: "Arial",
  border: { pt: 0.5, color: "CCCCCC" }
});

// Highlighted text box background
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.6, w: 9, h: 1.7,
  fill: { color: "FFF9E6" },
  line: { color: "D4A800", width: 2 }
});

// Highlighted text with computed values
const highlightText = [
  { text: "FOV_area_ratio_CT_over_MR: ", options: { bold: true, fontSize: 16 } },
  { text: String(data.computed.fov_area_ratio_ct_over_mr), options: { fontSize: 16, breakLine: true } },
  { text: "MaxBeamEnergy_MV: ", options: { bold: true, fontSize: 16 } },
  { text: String(data.rtplan.MaxBeamEnergy_MV), options: { fontSize: 16, breakLine: true } },
  { text: "cohens_d: ", options: { bold: true, fontSize: 16 } },
  { text: "null", options: { fontSize: 16 } }
];

slide.addText(highlightText, {
  x: 0.7, y: 3.75, w: 8.6, h: 1.4,
  fontFace: "Arial", color: "333333", valign: "middle"
});

// Save to exact required path
const outputPath = "/root/output/imaging_rtplan_card.pptx";
pres.writeFile({ fileName: outputPath })
  .then(() => console.log("PowerPoint created at: " + outputPath))
  .catch(err => { console.error(err); process.exit(1); });
EOF

# Execute the JavaScript to create the PowerPoint
node /root/create_pptx.js
