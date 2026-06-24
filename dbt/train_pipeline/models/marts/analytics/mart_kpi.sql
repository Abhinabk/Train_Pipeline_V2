with fact_with_dates as(
    select
        f.*,
        d.full_date
    from {{ ref('fact_delay') }} f
    join {{ ref('dim_date') }} d
        on f.date_key = d.date_key
),

final as (
    select
        count(*) as total_delay_records,
        count(distinct train_key) as total_trains,
        count(distinct station_key) as total_stations,
        round(avg(delay),2) as avg_delay,
        min(full_date) as min_date,
        max(full_date) as max_date,
        date_diff('day',max(full_date),current_date) as data_lag_days
from fact_with_dates
)
select * from final

