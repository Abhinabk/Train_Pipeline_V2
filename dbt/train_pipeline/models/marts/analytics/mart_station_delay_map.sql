select
    s.station_name,
    s.latitude,
    s.longitude,
    ROUND(avg(f.delay),2) as avg_delay,
    max(f.delay) as max_delay,
    count(*) as observations
from {{ ref('fact_delay') }} f
join {{ ref('dim_stations') }} s
    on f.station_key = s.station_key
group by 1,2,3