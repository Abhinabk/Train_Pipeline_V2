from datetime import date

import pandas as pd
from prefect import flow, task
from prefect.cache_policies import NO_CACHE

from config.settings import TRAINS_CSV
from ingestion.etrain.build_url import build_train_url
from ingestion.etrain.create_session import create_session
from ingestion.etrain.scraper import fetch_train_history
from storage.duckdb.queries import check_existing_fetch
from storage.writer.bronze.write_bronze_metadata import insert_bronze_train_metadata
from config.logger import bronze_logger
import requests
from duckdb import DuckDBPyConnection

from validators.bronze.metadata import BronzeTrainMetadata


@task(retries=2,retry_delay_seconds=20,cache_policy=NO_CACHE,timeout_seconds=30)
def run_train_ingestion(session:requests.Session,con:DuckDBPyConnection,train_no:str,train_name:str,run_date:date,force:bool):

    if not force and check_existing_fetch(con,train_no,run_date):
        bronze_logger.log('SKIP',f"{train_name}_{train_no} aready fetched today")
        return
    url = build_train_url(train_no,train_name,time="1y") # type: ignore
    safe_train_name = train_name.strip().replace(" ", "-") # type: ignore
  
    try:
        result = fetch_train_history(url,session,train_no,safe_train_name,storage="s3")
        metadata = BronzeTrainMetadata(
            run_date=run_date,
            train_no=train_no,
            train_name=safe_train_name,
            source_url=url,
            file_path=result["file_path"],
            response_status_code=result["response_status_code"],
            success=True,
            error_message=None
        )
        bronze_logger.success(f"{metadata.train_name}_{metadata.train_no} ingested -> {metadata.file_path}")


    except requests.exceptions.RequestException as err:
        metadata = BronzeTrainMetadata(
            run_date=run_date,
            train_no=train_no,
            train_name=safe_train_name,
            source_url=url,
            file_path=result["file_path"],
            response_status_code=getattr(err.response,'status_code',None), #None is reqd here as even though exception as we may not even reach etrain website
            success=False,
            error_message=getattr(err.response,'reason', str(err))
        )
        bronze_logger.warning(f"{metadata.train_name}_{metadata.train_no} {metadata.source_url} {err}")
        
    insert_bronze_train_metadata(con,metadata)
    
@flow(name="bronze-train-ingestion")
def ingest_all_trains(con:DuckDBPyConnection,run_date:date,force:bool=False):
   
    train_config_path = TRAINS_CSV
    session = create_session()
    df = pd.read_csv(train_config_path)
    for rows in (df.itertuples(index=False)):
        train_no = rows.number 
        train_name = rows.name  
        run_train_ingestion(session,con,str(train_no),str(train_name),run_date,force)
    bronze_logger.success(f"Ingestion complete: {len(df)} trains processed")
