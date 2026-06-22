WITH stg_weather as (
    select * from {{ source('train_pipeline', 'weather') }}
),
final as (
    select
    current_timestamp as timestamp,
    CAST(station_code AS VARCHAR) AS station_code,
    CAST(weather_date AS DATE) AS weather_date,
    CAST(temperature_mean AS DOUBLE) AS temperature_mean,
    CAST(precipitation_sum AS DOUBLE) AS precipitation_sum,
    CAST(rain_sum AS DOUBLE) as rain_sum,
	CAST(daylight_duration AS DOUBLE) as daylight_duration ,
	CAST(wind_gusts_max AS DOUBLE) as  wind_gusts_max,
    CAST(weather_code AS INTEGER) AS weather_code
from stg_weather
)

select * from final