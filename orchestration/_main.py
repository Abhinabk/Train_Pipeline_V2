from dotenv import load_dotenv
from duckdb import DuckDBPyConnection
from prefect import flow, task
from prefect.cache_policies import NO_CACHE
import requests
from config.settings import TRAINS_CSV
from ingestion.etrain.create_session import create_session
from orchestration.run_ingestion import run_train_ingestion
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.init_db import init_bronze_train_metadata
from storage.readers.load_csv import load_csv
from tqdm import tqdm 
load_dotenv() 

@task(retries=2,retry_delay_seconds=20,cache_policy=NO_CACHE)
def ingest_train_flow(session:requests.Session,con:DuckDBPyConnection,train_no:str,train_name:str):
    run_train_ingestion(session,con,str(train_no),str(train_name))

@flow(name="bronze-train-ingestion")
def ingest_all_trains():
    train_config_path = TRAINS_CSV
    session = create_session()
    df = load_csv(train_config_path)
    with get_connection() as con: # type: ignore
        init_bronze_train_metadata(con)
        for rows in tqdm(df.itertuples(index=False), total=len(df), desc="Ingesting trains"): # type: ignore
            train_no = rows.number # type: ignore
            train_name = rows.name  # type: ignore
            ingest_train_flow(session,con,str(train_no),str(train_name))

if __name__ == "__main__":
    ingest_all_trains()