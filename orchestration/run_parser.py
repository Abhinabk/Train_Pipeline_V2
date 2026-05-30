
from bs4 import BeautifulSoup
from duckdb import DuckDBPyConnection
import pandas as pd
from parsing.get_fare import fare_details
from parsing.get_route import route_order
from parsing.get_station_delay import station_delay
from parsing.get_running_days import running_days
from storage.duckdb.queries import check_existing_parse, get_successful_trains
from datetime import date
from config.logger import silver_logger
from storage.object_store.s3 import get_object_from_uri
from storage.writer.silver.write_silver_metadata import insert_silver_metadata
from storage.writer.silver.write_silver_parquet import write_parquet_to_s3
from transformations.silver.station_delay import transform_station_delay_to_long
from prefect import flow ,task
from prefect import get_run_logger


def on_task_failure(task, task_run, state):
    silver_logger.error(f"Task {task.name} failed on run {task_run.name}: {state.message}")

def on_flow_failure(flow, flow_run, state):
    silver_logger.error(f"Flow {flow.name} failed: {state.message}")

@task(name='fetch-and-parse-a-train', retries=2,retry_delay_seconds=10,on_failure=[on_task_failure])
def parse_train(train_no:str,s3_uri:str)->dict:
    p_logger = get_run_logger()
    html = get_object_from_uri(s3_uri)
    soup = BeautifulSoup(html,'html.parser')
    result = {
        "station_delay":station_delay(soup, train_no),
        "route":route_order(soup, train_no),
        "fare_details":fare_details(soup, train_no),
        "running_days":running_days(soup,train_no)
    }
    p_logger.info(f"Processed train {train_no}")
    silver_logger.success(f"Processed train {train_no}")
    return result

@task(name="write-station-delay",on_failure=[on_task_failure])
def write_station_delay(all_station_delay:list|None,run_date:date):
    if not all_station_delay:
        return
    
    df = transform_station_delay_to_long(all_station_delay)
    write_parquet_to_s3(df,'station_delay',run_date)

@task(name="write-route",on_failure=[on_task_failure])
def write_route(all_route:list|None,run_date:date):
    if not all_route:
        return
    
    df = pd.DataFrame(all_route)
    write_parquet_to_s3(df,'route_order',run_date)
@task(name="write-fare",on_failure=[on_task_failure])
def write_fare(all_fare:list|None,run_date:date):
    if not all_fare:
        return
    
    df = pd.DataFrame(all_fare)
    write_parquet_to_s3(df,'fare_details',run_date)  
@task(name="write-running-days",on_failure=[on_task_failure])
def write_running_days(all_running_days:list|None,run_date:date):
    if not all_running_days:
        return
    
    df = pd.DataFrame(all_running_days)
    write_parquet_to_s3(df,'all_running_days',run_date)  

@flow(name="parse-all-trains", on_failure=[on_flow_failure])
def parse_all_trains(con:DuckDBPyConnection,run_date:date):
    if check_existing_parse(con,run_date):
        silver_logger.log('SKIP',f"aready fetched for {run_date}")
        return
    metadata = {
            "run_date":run_date,
            "station_delay_path":None,
            "route_path":None,
            "fare_path":None
    }
    all_station_delay = []
    all_route = []
    all_fare = []
    all_running_days = []
    all_train_s3_urls = list(get_successful_trains(con, run_date))
    #for paralles tasks
    task_runners = parse_train.map(
        train_no = [t[0] for t in all_train_s3_urls],
        s3_uri = [t[1] for t in all_train_s3_urls ]
    )
    #storing all the results of taks_runner together
    results = [t.result() for t in task_runners]
    for r in results:
        for value in r['station_delay']:
            all_station_delay.append(value)
        for value in r['route']:
            all_route.append(value)
        for value in r['fare_details']:
            all_fare.append(value)
        for value in r['running_days']:
            all_running_days.append(value)

    station_path =write_station_delay(all_station_delay,run_date)
    fare_path = write_fare(all_fare,run_date)
    route_path = write_route(all_route,run_date)
    running_days_path = write_running_days(all_running_days,run_date)
    metadata.update({'station_delay_path':station_path,'route_path':route_path,
                     'fare_path':fare_path,'running_days_path':running_days_path})
    insert_silver_metadata(con, metadata)






