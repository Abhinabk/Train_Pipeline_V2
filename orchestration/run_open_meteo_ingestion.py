
from datetime import date

from duckdb import DuckDBPyConnection
import pandas as pd
from prefect import flow,task,ThreadPoolTaskRunner, unmapped
from prefect.tasks import exponential_backoff
import requests

from config.settings import S3_PREFIX_BRONZE_WEATHER
from ingestion.openmeteo.get_weather import fetch_weather_daily
from storage.duckdb.queries import get_min_max_date, get_station_coords
from storage.writer.bronze.write_bronze_metadata import insert_open_meteo_metadata
from storage.writer.common.write_parquet import write_parquet_to_s3
from validators.bronze.metadata import OpenMeteoMetadata

def is_retryable(task,task_run,state)->bool:
    try:
        state.result() # will re-raise exception fo the task 
    except requests.HTTPError as e:
        return e.response.status_code == 429 #retry only for rate-limited 
    except (requests.ConnectionError,requests.Timeout): #and connection timeout this covers connectionerror adn timeouts
        return True
    return False 

@task(name="open-meteo-ingestion",retries=3,retry_delay_seconds=exponential_backoff(backoff_factor=10),retry_condition_fn=is_retryable,
      retry_jitter_factor=0.2) #10*pow(2,i) 10,20,40 .. 
def ingest_per_station(station_code:str,longitude:float,latitude:float,start_date:str,end_date:str):
    with requests.Session() as session:
        result = fetch_weather_daily(session,
                            station_code=station_code,
                            longitude=longitude,
                            latitude=latitude,
                            start_date=start_date,
                            end_date=end_date)
        return {
        "status_code": result["status_code"],
        "station_code": result["station_code"],
        "weather_data": result["weather_daily"],
        }


@task(name="write-open-meteo")
def write_open_meteo_each_station(data:list[dict],station_code:str,run_date:date):
    if not data:
        return None
    df = pd.DataFrame(data)
    df["station_code"] = station_code
    return write_parquet_to_s3(df,'open_meteo',run_date,prefix=f'{S3_PREFIX_BRONZE_WEATHER}/{station_code}')

@flow(name="ingest-all-stations",task_runner=ThreadPoolTaskRunner)
def ingest_all_stations(con:DuckDBPyConnection,run_date:date):
    min_max = get_min_max_date(con,run_date)
    station  = get_station_coords(con,run_date)
    min_date,max_date = min_max
    station_code,_,longitude,latitude = zip(*station) #unzips intoo indiviual column
    task_runner = ingest_per_station.map(
        station_code,longitude,latitude,unmapped(min_date),unmapped(max_date)
    )#unmapped makes the arg const and passes it changed
    result = [t.result() for t in task_runner]
    for r in result:
        status_code = r["status_code"]
        station_code = r["station_code"]
        weather_data = r["weather_data"]
        file_path = write_open_meteo_each_station(list(weather_data),str(station_code),run_date)
        metadata = OpenMeteoMetadata(
            run_date = run_date,
            station_code=station_code,
            file_path = file_path,
            response_status_code=int(status_code),
            success=(status_code==200),
            error_message=None
        )
        insert_open_meteo_metadata(con,metadata)
