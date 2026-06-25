with delays as (
    select
        s.station_key,
        s.station_name,
        f.date_key,
        f.delay
    from {{ ref('fact_delay') }} f
    join {{ ref('dim_stations') }} s 
    on f.station_key = s.station_key
    where f.delay is not null
),

weather as (
    select
        station_key,
        date_key,
        temperature_mean,
        precipitation_sum,
        daylight_duration,
        rain_sum,
        wind_gusts_max,
        weather_code
    from {{ ref('fact_weather') }}
)

select
    d.station_name,
    d.date_key,
    d.delay,
    w.temperature_mean,
    w.precipitation_sum,
    w.daylight_duration,
    w.rain_sum,
    w.wind_gusts_max,
    w.weather_code
from delays d
join weather w
    on d.station_key = w.station_key
   and d.date_key = w.date_key