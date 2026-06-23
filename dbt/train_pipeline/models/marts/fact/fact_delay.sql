with delay_station as (
    select
        d.station_key, 
        s.delay,
        s.train_no,
        s.date
    from {{ ref('stg_station_delay') }} s
    join {{ ref('dim_stations') }} d
    on s.station_code = d.station_code
),

final as(
    select
        s.station_key,
        s.delay,
        s.date,
        t.train_key
    from delay_station  s
    join {{ ref('dim_trains') }} t 
    on s.train_no = t.train_no
)
select 
    f.station_key,
    f.train_key,
    f.delay,
    d.date_key 
from final f join {{ ref('dim_date') }} d 
    on f.date = d.full_date



