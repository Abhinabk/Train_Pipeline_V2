with fact_with_dates as (
    select
        f.delay,
        d.full_date
    from {{ ref('fact_delay') }} f
    join {{ ref('dim_date') }} d
        on f.date_key = d.date_key
)

select
    full_date,
    round(avg(delay), 2) as avg_delay,
    round(percentile_cont(0.95) within group (order by delay),2) as p95_delay
from fact_with_dates
group by full_date
order by full_date