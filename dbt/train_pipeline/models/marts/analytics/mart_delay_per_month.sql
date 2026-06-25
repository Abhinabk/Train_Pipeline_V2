select
    date_trunc('month', d.full_date)::DATE as month,
    f.delay
from {{ ref('fact_delay') }} f
join {{ ref('dim_date') }} d
    on f.date_key = d.date_key
where f.delay is not null
order by month


