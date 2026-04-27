Create a single-slide PowerPoint briefing that answers this question with a uniquely verifiable result:

**“Which airline (by full name) had the highest average arrival delay on the SEA→PDX route in January 2014, and what was that average delay (minutes)?”**

To do this, you must:
1. Use `/root/flights_2.csv` to filter flights to **origin=SEA**, **dest=PDX**, **month=1**, and compute **mean `arr_delay` per `carrier`**, excluding rows where `arr_delay` is missing (`NA`).
2. Identify the single carrier with the **maximum** mean arrival delay (break ties deterministically by choosing the lexicographically smallest `carrier` code if needed).
3. Use `/root/airlines.csv` to map that carrier code to its **Description** (full airline name). If multiple matches exist due to code variants, use the exact `Code` match.
4. Run a statistical model that justifies the metric shown on the slide: fit an **OLS** model on the filtered SEA→PDX data with `arr_delay` as the dependent variable and `carrier` as a categorical predictor (intercept included), and use the model to confirm which carrier has the largest estimated mean (i.e., intercept + carrier effect).
5. Generate a PowerPoint file at exactly this path:

`/root/output/sea_pdx_worst_avg_arrival_delay.pptx`

The slide must contain:
- A title: **“SEA→PDX (Jan 2014): Worst Average Arrival Delay”**
- One sentence stating the winning airline **full name**, its **carrier code**, and the **average arrival delay rounded to 2 decimals**.
- A small table with exactly 3 columns and 2 rows (header + one data row): `carrier`, `airline_name`, `mean_arr_delay`.
- A footnote line with the OLS model’s **R²** (rounded to 4 decimals) computed on the same filtered dataset.

Writing the PPTX file to the specified path is mandatory for completion.