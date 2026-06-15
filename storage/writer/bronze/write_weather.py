from datetime import date

from duckdb import DuckDBPyConnection 

def _insert_weather(con: DuckDBPyConnection, path: str):
    #insert into first aloows to not have columns in strict order
    con.execute(r'''
    INSERT INTO bronze.weather
    SELECT
        regexp_extract(filename, 'weather/([^/]+)', 1) AS run_date,
        regexp_extract(filename, '/([^/]+)\.json', 1)  AS station_code,
        unnest(time)                AS weather_date,
        unnest(temperature_2m_mean) AS temperature_mean,
        unnest(precipitation_sum)   AS precipitation_sum,
        unnest(rain_sum)            AS rain_sum,
        unnest(daylight_duration)   AS daylight_duration,
        unnest(wind_gusts_10m_max)  AS wind_gust_max,
        unnest(weather_code)        AS weather_code
    FROM read_json(?, filename=true)
    ''',[path])

def insert_weather_data_per_date(con:DuckDBPyConnection,run_date:date):
    _insert_weather(con, f"s3://train-pipeline-v2/bronze/weather/{run_date}/*.json")

def insert_weather_data_backfill(con:DuckDBPyConnection):
    _insert_weather(con, "s3://train-pipeline-v2/bronze/weather/*/*.json")