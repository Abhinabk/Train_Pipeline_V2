from config.settings import TRAINS_CSV
from ingestion.etrain.create_session import create_session
from orchestration.run_ingestion import run_train_ingestion
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.init_db import init_bronze_train_metadata
from storage.readers.load_csv import load_csv


session = create_session()

train_config_path = TRAINS_CSV
df = load_csv(train_config_path)
with get_connection() as con: # type: ignore
    init_bronze_train_metadata(con)
    for rows in df.itertuples(index=False): # type: ignore
        train_no = rows.number # type: ignore
        train_name = rows.name  # type: ignore

        run_train_ingestion(session,con,train_no,train_name)
        break