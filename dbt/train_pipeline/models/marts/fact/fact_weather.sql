with weather_station as (
    select 
        s.station_key,
        w.weather_date,
        w.station_code,
        w.temperature_mean,
        w.precipitation_sum,
        w.rain_sum,
        w.daylight_duration,
        w.wind_gusts_max,
        w.weather_code
    from {{ ref('stg_weather') }} w
    join {{ ref('dim_stations') }} s
    on w.station_code = s.station_code
),
dim_date as (
    select
        date_key,
        full_date
    from {{ ref('dim_date') }}
),
final as (
    select
        w.* exclude(weather_date),
        d.date_key 
    from weather_station w 
    join dim_date d
    on w.weather_date = d.full_date
)
select * from final

