with delay_station as (
    select
        d.station_key, 
        s.delay,
        s.train_no
    from {{ ref('stg_station_delay') }} s
    join {{ ref('dim_stations') }} d
    on s.station_code = d.station_code
),

final as(
    select
        s.station_key,
        s.delay,
        t.train_key
    from delay_station  s
    join {{ ref('dim_trains') }} t 
    on s.train_no = t.train_no
)
select * from final



