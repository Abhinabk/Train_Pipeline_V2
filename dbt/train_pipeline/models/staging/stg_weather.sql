WITH stg_weather as (
    select * from {{ source('train_pipeline', 'weather') }}
),
station_state as (
select 
    "Station Code" as station_code
    from{{ ref('station_state_seed') }}
),

final as (
    select
    DISTINCT
    CAST(weather_date AS DATE) AS weather_date,
    CAST(s.station_code AS VARCHAR) AS station_code,
    CAST(temperature_mean AS DOUBLE) AS temperature_mean,
    CAST(precipitation_sum AS DOUBLE) AS precipitation_sum,
    CAST(rain_sum AS DOUBLE) as rain_sum,
	CAST(daylight_duration AS DOUBLE) as daylight_duration ,
	CAST(wind_gusts_max AS DOUBLE) as  wind_gusts_max,
    CAST(weather_code AS INTEGER) AS weather_code
from stg_weather w 
join 
station_state s 
on s.station_code = w.station_code

)

select * from final