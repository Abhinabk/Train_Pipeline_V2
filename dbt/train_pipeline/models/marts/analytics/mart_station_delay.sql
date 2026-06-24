with delay as (
    select
        station_key,
        train_key,
        delay
    from {{ ref('fact_delay') }}
),
station_delay as (
    select 
        s.station_name,
        Round(avg(d.delay),2)  as avg_delay 
    from delay d 
    join {{ ref('dim_stations') }} s
    on d.station_key = s.station_key
    group by s.station_name
    order by avg_delay desc
    limit 10
)
select * from station_delay
