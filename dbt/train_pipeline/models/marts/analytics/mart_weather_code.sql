select
    delay,
    case
        when weather_code = 0 then 'Clear Sky'
        when weather_code between 1 and 3 then 'Cloudy'
        when weather_code in (51,53,55) then 'Drizzle'
        when weather_code in (61,63,65) then 'Rain'
        else 'Other'
    end as weather_condition
from {{ ref('mart_delay_weather') }}