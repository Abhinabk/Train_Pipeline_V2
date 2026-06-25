{% docs __overview__ %}

# Train Data Pipeline 

End-to-end data engineering project that 
- collects train delay history data, 
- enriches it with weather information,
- builds analytics-ready marts for reporting.
## Architecture
Bronze
  - Raw HTML from etrain
Silver
  - Parsed station delay
  - Weather observations
  - Route data
  - Fare data
Gold
  - KPI reporting
  - Delay trends
  - Station analytics
  - Train analytics

### Critical Data Quality Insights
* **Station Delay Nulls**: High null counts in the `delay` column
* **The Evidence**: 
  ```sql
  select
      train_no,
      count(*) as rows,
      count(delay) as recorded_delays,
      round(100.0 * count(delay) / count(*), 2) as pct_recorded
  from read_parquet('s3://train-pipeline-v2/silver/station_delay/*/*.parquet')
  group by train_no
  order by pct_recorded asc;
  ```
* **Conclusion**: Coverage varies significantly by train.
This is expected because the trains have different operating frequencies (daily, weekly,
bi-weekly) and different route lengths while routs mostly being in smaller stations where data entry mabe not be as robust,source may not register delays for all stations.Its a source data problem not a dbt problem

{% enddocs %}
