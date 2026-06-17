WITH stg_weather as (
    select * from {{ source('train_pipeline', 'weather') }}
),
final as (
    select
    current_timestamp as timestamp,
    station_code,
    weather_date,
    temperature_mean,
    precipitation_sum,
    rain_sum,
    daylight_duration,
    wind_gusts_max,
    weather_code
from stg_weather
)

select * from final