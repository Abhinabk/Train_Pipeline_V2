from datetime import date

from duckdb import DuckDBPyConnection
from prefect import flow, task
from prefect.cache_policies import NO_CACHE

from storage.duckdb.duckdb_con import get_connection
from storage.writer.bronze.write_weather import (
    insert_weather_data_backfill,
    insert_weather_data_per_date,
)


@task(retries=2, retry_delay_seconds=30, cache_policy=NO_CACHE)
def load_weather_to_bronze_incremental(con: DuckDBPyConnection, run_date: date):
    insert_weather_data_per_date(con, run_date)

@task(retries=2, retry_delay_seconds=30, cache_policy=NO_CACHE)
def load_weather_to_bronze_backfill(con: DuckDBPyConnection):
    insert_weather_data_backfill(con)

@flow()
def load_weather_to_bronze(con: DuckDBPyConnection, run_date: date|None=None):
    if run_date is None:
        load_weather_to_bronze_backfill(con) 
    else:
       load_weather_to_bronze_incremental(con,run_date)

if __name__ == '__main__':
    with get_connection() as con:
        load_weather_to_bronze(con)
