from datetime import date, timedelta
from duckdb import DuckDBPyConnection
from prefect import flow, task
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.tasks import exponential_backoff
import requests
from config.logger import bronze_logger
from ingestion.openmeteo.fetch import fetch_weather_daily
from orchestration.weather.write_insert import write_insert
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.queries import get_last_weather_date, get_min_max_date, get_station_coords


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
def ingest_all_stations(con: DuckDBPyConnection, run_date: date,backfill:bool=False,force:bool=False,only_station:list[str]|None=None):

    station = get_station_coords(con)
    min_max = get_min_max_date(con, run_date)
    min_date, max_date = min_max
    
    if only_station and force: #have to run single stations with force flag if not force then next block runs
        station = [s for s in station if s[0] in only_station] #s[0] is the station_code column
        if not station:
            bronze_logger.warning(f"Station {only_station} not found for {run_date}")
            return
    if backfill:
        mode = "BACKFILL"
    elif force:
        targets = only_station or "all"
        mode = f"FORCE (stations={targets})"
    else:
        mode = "INCREMENTAL"
    bronze_logger.info(f"[{mode}] run_date={run_date} | min_date={min_date}")

    end_date = run_date 
    work = [] # (code,long,lat,start_date,end_date)
    for code,lon,lat in station:
        if backfill or force:
            start_date = min_date
        else:
            last = get_last_weather_date(con, code)
            if last is None: # means never fetched so start fetching from beginning
                start_date = min_date                 
            elif last >= run_date: #already on latest
                bronze_logger.log("SKIP", f"{code} on latest ")
                continue                               
            else:
                start_date = last + timedelta(days=1)  

        work.append((code, lon, lat, start_date, end_date))

    if not work: #only possinble if every station hits continue so latest data present
        bronze_logger.log("SKIP", f"All stations current through {run_date}")
        return
    
    station_code, longitude, latitude,starts,ends = zip(*work)  # unzips into indiviual column/tuple
    prefect_states = ingest_per_station.map(
        station_code,
        longitude,
        latitude,
        [str(s) for s in starts],
        [str(s) for s in ends],#fetch_weather expects in str
        return_state=True,
    )           # returns the results  wrapped in prefect state
                # e.g Completed(data={"status_code": 200, "station_code": "NDLS", "weather_data": [...]})

    write_insert(con,run_date,work,prefect_states)
  


if __name__ == "__main__":
    run_date = date.today()
    with get_connection() as con:
        ingest_all_stations(con, run_date)
