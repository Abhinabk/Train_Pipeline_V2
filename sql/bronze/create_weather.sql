CREATE SCHEMA IF NOT EXISTS bronze;  
CREATE TABLE IF NOT EXISTS bronze.weather(
    run_date VARCHAR,
    station_code VARCHAR,
    weather_date DATE,
    temperature_mean DOUBLE,
    precipitation_sum DOUBLE, 
    rain_sum DOUBLE, 
    daylight_duration DOUBLE,
    wind_gusts_max DOUBLE, 
    weather_code INT,   
)