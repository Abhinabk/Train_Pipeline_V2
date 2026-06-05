from datetime import date
import json
from duckdb import DuckDBPyConnection
from prefect import flow, task, unmapped
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.tasks import exponential_backoff
import requests
from config.logger import bronze_logger
from config.settings import S3_BUCKET, S3_PREFIX_BRONZE_WEATHER
from ingestion.openmeteo.get_weather import fetch_weather_daily
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.queries import check_existing_weather, get_min_max_date, get_station_coords
from storage.object_store.s3 import save_json_s3
from storage.writer.bronze.write_bronze_metadata import insert_open_meteo_metadata
from validators.bronze.metadata import OpenMeteoMetadata


def is_retryable(task, task_run, state) -> bool:
    try:
        state.result()  # will re-raise exception fo the task
    except requests.HTTPError as e:
        if e.response is None:
            return False
        return e.response.status_code == 429  # retry only for rate-limited
    except (
        requests.ConnectionError,
        requests.Timeout,
    ):  # and connection timeout this covers connectionerror adn timeouts
        return True
    return False


@task(
    name="open-meteo-ingestion",
    task_run_name="open-meteo-{station_code}",
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    retry_condition_fn=is_retryable,
    retry_jitter_factor=0.2,
)  # 10*pow(2,i) 10,20,40 ..
def ingest_per_station(
    station_code: str, longitude: float, latitude: float, start_date: str, end_date: str
):
    with requests.Session() as session:
        result = fetch_weather_daily(
            session,
            station_code=station_code,
            longitude=longitude,
            latitude=latitude,
            start_date=start_date,
            end_date=end_date,
        )
        return result


@flow(name="ingest-all-stations", task_runner=ThreadPoolTaskRunner(max_workers=3))  # type: ignore
def ingest_all_stations(con: DuckDBPyConnection, run_date: date,force:bool=False):

    min_max = get_min_max_date(con, run_date)
    station = get_station_coords(con, run_date)
    min_date, max_date = min_max
    if not station:
        return
    if not force:
        station = [s for s in station if not check_existing_weather(con,s[0],run_date)] #s[0] is the station_code
        #fetches only those stations that dosen't return True 
        if not station:
            bronze_logger.log('SKIP',f" aready fetched all stations for {run_date}")
            return
    
    station_code, longitude, latitude = zip(*station)  # unzips into indiviual column
    prefect_states = ingest_per_station.map(
        station_code,
        longitude,
        latitude,
        unmapped(min_date),
        unmapped(max_date),
        return_state=True,
    )  # returns the results  wrapped in prefect state
    # e.g Completed(data={"status_code": 200, "station_code": "NDLS", "weather_data": [...]})

    for code, state in zip(station_code, prefect_states):
        if state.is_completed():
            r = state.result()  # actual value returned by the task
            file_path = save_json_s3(
                S3_BUCKET,
                f"{S3_PREFIX_BRONZE_WEATHER}/{run_date}/{code}.json",
                content=json.dumps(r.weather_data),
            )
            metadata = OpenMeteoMetadata(
                run_date=run_date,
                station_code=code,
                file_path=file_path,
                response_status_code=r.status_code,
                success=True,
                error_message=None
            )
            bronze_logger.success(f"Fetched {code} weather")
        else:
            metadata = OpenMeteoMetadata(
                run_date=run_date,
                station_code=code,
                file_path=None,
                response_status_code=None,
                success=False,
                error_message=str(state.message)
            )
            bronze_logger.warning(f"Failed {code} weather:{state.message}")

        insert_open_meteo_metadata(con, metadata)


if __name__ == "__main__":
    run_date = date.today()
    with get_connection() as con:
        ingest_all_stations(con, run_date)
