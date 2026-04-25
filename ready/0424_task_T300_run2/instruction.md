Create a single decision-ready Word report that answers this one question:

**“Which month should we *avoid* scheduling major aircraft maintenance in, if we want to minimize disruption to demand (long-run seasonality) *and* minimize operational risk (2014 delay behavior)?”**

You must determine **exactly one month (January–December)** using both datasets as follows:

1. **Demand seasonality (from `/root/flights.csv`)**  
   - Compute the *seasonality index* for each month across all years:  
     `seasonality_index = (mean passengers for that month across 1949–1960) / (overall mean passengers) * 100`.
   - Higher index = higher demand.

2. **Operational risk (from `/root/flights_2.csv`)**  
   - Treat `NA` as nulls and exclude null delays from calculations.
   - For each month (numeric 1–12), compute:
     - `p90_arr_delay` = 90th percentile of `arr_delay`
     - `cancel_rate_proxy` = share of rows where `dep_time` is null (since missing departure time indicates a likely cancellation/diversion in this extract)
   - Higher values = higher risk.

3. **Single combined “avoid maintenance” score (must be deterministic):**  
   - Rank months by **seasonality_index** descending (rank 1 = highest demand).  
   - Rank months by **p90_arr_delay** descending (rank 1 = worst delays).  
   - Rank months by **cancel_rate_proxy** descending (rank 1 = highest proxy cancellations).  
   - Compute `avoid_score = demand_rank + delay_rank + cancel_rank`.  
   - The month with the **lowest** `avoid_score` is the recommended month to schedule maintenance (least disruption).  
   - If there is a tie, break it by choosing the month with the **lower seasonality_index**; if still tied, choose the **lower month number**.

4. **Deliverable (mandatory file artifact):**  
   Save a `.docx` report to:  
   **`/root/output/maintenance_month_recommendation.docx`**

   The document must include:
   - Title (Heading 1): “Maintenance Scheduling Recommendation”
   - A short **Metric Contract** paragraph defining the two datasets’ grains and the computed metrics.
   - A single-sentence **Recommendation** that names the chosen month.
   - One table (with DXA widths, Google Docs-safe) listing all 12 months with these columns exactly:  
     `month`, `seasonality_index`, `p90_arr_delay`, `cancel_rate_proxy`, `demand_rank`, `delay_rank`, `cancel_rank`, `avoid_score`
   - A brief **Decision Brief** section (3–6 bullet points) stating rationale, evidence, confidence, and caveats.

Notes:
- Month names must be consistent across files (map `flights_2.csv` numeric month to English month name to join/align).
- The report’s recommendation must be uniquely determined by the scoring rules above.
- Do not create any additional output files; only the `.docx` is required.