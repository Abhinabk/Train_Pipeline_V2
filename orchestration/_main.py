from datetime import datetime

from dotenv import load_dotenv
from orchestration.run_ingestion import ingest_all_trains
from orchestration.run_parser import parse_all_trains
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.init_db import init_db

load_dotenv() 

if __name__ == "__main__":
    with get_connection() as con: 
        run_date = datetime.today().date()
        init_db(con)
        ingest_all_trains(con,run_date) #sequential scraper
        parse_all_trains(con,run_date) #parallel parser