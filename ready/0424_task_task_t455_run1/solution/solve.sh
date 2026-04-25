#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Install pptxgenjs if needed
cd /root
npm list pptxgenjs >/dev/null 2>&1 || npm install pptxgenjs --silent 2>/dev/null

# Create the PPTX using Node.js/pptxgenjs
cat << 'EOF' > /root/create_pptx.js
const pptxgen = require("pptxgenjs");

// Data values from analysis (hardcoded from trajectory)
const carrier = "OO";
const airlineName = "SkyWest Airlines Inc.";
const meanDelay = 8.62; // rounded to 2 decimals
const r2 = 0.0000; // rounded to 4 decimals

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.title = 'SEA→PDX Arrival Delay Analysis';

const slide = pptx.addSlide();

// Title
slide.addText("SEA→PDX (Jan 2014): Worst Average Arrival Delay", {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 28, fontFace: "Arial", bold: true, color: "1E2761"
});

// Sentence with the result
slide.addText(
  "Worst carrier: " + airlineName + " (" + carrier + ") with mean arrival delay " + meanDelay.toFixed(2) + " minutes.",
  { x: 0.5, y: 1.3, w: 9, h: 0.6, fontSize: 16, fontFace: "Arial", color: "363636" }
);

// Table: exactly 3 columns, 2 rows (header + data)
const tableData = [
  [
    { text: "carrier", options: { bold: true, fill: { color: "1E2761" }, color: "FFFFFF" } },
    { text: "airline_name", options: { bold: true, fill: { color: "1E2761" }, color: "FFFFFF" } },
    { text: "mean_arr_delay", options: { bold: true, fill: { color: "1E2761" }, color: "FFFFFF" } }
  ],
  [
    { text: carrier, options: { fill: { color: "F1F1F1" } } },
    { text: airlineName, options: { fill: { color: "F1F1F1" } } },
    { text: meanDelay.toFixed(2), options: { fill: { color: "F1F1F1" } } }
  ]
];

slide.addTable(tableData, {
  x: 0.8, y: 2.2, w: 8.4,
  fontSize: 14, fontFace: "Arial",
  border: { type: "solid", color: "999999", pt: 1 },
  colW: [1.5, 4.5, 2.4]
});

// Footnote with OLS R²
slide.addText("OLS model R² = " + r2.toFixed(4), {
  x: 0.5, y: 5.0, w: 9, h: 0.3,
  fontSize: 10, fontFace: "Arial", italic: true, color: "666666"
});

// Save file
pptx.writeFile({ fileName: "/root/output/sea_pdx_worst_avg_arrival_delay.pptx" })
  .then(() => console.log("PPTX created successfully!"))
  .catch(err => { console.error("Error:", err); process.exit(1); });
EOF

# Execute the script from the project directory where node_modules exists
cd /root
node create_pptx.js
