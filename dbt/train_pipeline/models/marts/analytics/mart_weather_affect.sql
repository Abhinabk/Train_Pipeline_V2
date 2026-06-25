select
    ROUND(corr(delay, rain_sum),4) as rain_corr,
    ROUND(corr(delay, wind_gusts_max),4) as wind_corr,
    ROUND(corr(delay, temperature_mean),4) as temp_corr,
    ROUND(corr(delay,daylight_duration),4) as daylight_corr
from {{ ref('mart_delay_weather') }}