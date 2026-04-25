Using the Iris dataset at `/root/iris.csv`, generate a single Excel report that identifies **the one measurement (among sepal_length, sepal_width, petal_length, petal_width) that most strongly explains species differences** via an R²-based contribution approach, and present the result in a professionally formatted workbook.

**Required deliverable (must be written to disk):**  
Save the workbook to: `/root/output/iris_species_driver.xlsx`

**What the workbook must contain (single coherent objective: determine and report the top driver):**
1. **Data ingestion & validation (CSV):** Read the CSV and confirm the expected 5 headers exist; use a streaming/row-based CSV approach for this validation step before loading into a DataFrame.
2. **High-performance transformation:** Load the data with a high-performance DataFrame workflow and create a numeric modeling table where `species` is encoded deterministically into two dummy variables (alphabetical order of species; drop the first as baseline).
3. **Contribution analysis (uniquely determined):**  
   - Standardize the four numeric measurements.  
   - Fit a linear regression predicting the two dummy columns jointly (treat as two separate targets and average their R² values).  
   - Compute each measurement’s **R² contribution** as: `avg_R2_full_model - avg_R2_model_without_that_measurement`.  
   - Select the single measurement with the **largest positive contribution**; break ties (if any) by choosing the alphabetically earliest measurement name.
4. **Excel report content:** Create an Excel file with two sheets:
   - **`Result`**: a 2-row table with columns `Top_Measurement`, `Contribution`, `Avg_R2_Full`.  
   - **`Contributions`**: a table listing all four measurements and their computed contributions, sorted descending by contribution.
   Also include a simple bar chart (can be inserted as an image) visualizing the four contributions.
5. **Financial-model style formatting:** Apply Excel formatting conventions:
   - Header row bold with a light fill; numeric cells formatted to 4 decimals.  
   - In `Result`, make `Top_Measurement` value blue text (input-style) and the numeric outputs black text (formula-style).  
   - Auto-fit/adjust column widths for readability.

The task is complete only if `/root/output/iris_species_driver.xlsx` exists and the `Result` sheet’s `Top_Measurement` and `Contribution` are consistent with the deterministic computation above.