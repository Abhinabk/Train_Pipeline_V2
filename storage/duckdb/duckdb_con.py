import duckdb
from dotenv import load_dotenv
import os
from config.settings import DUCK_DB_DATABASE

load_dotenv()
token = os.getenv("MOTHERDUCK_TOKEN")
database_name = os.getenv("MOTHERDUCK_DATABASE_NAME")
def get_connection(type="motherduck"):
    if type == "local":
        DUCK_DB_DATABASE.parent.mkdir(parents=True,exist_ok=True)
        return duckdb.connect(str(DUCK_DB_DATABASE))
    if type == "motherduck":
        con = duckdb.connect(f"md:?motherduck_token={token}")
        con.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        con = duckdb.connect(f"md:{database_name}?motherduck_token={token}")
        return con
    raise ValueError(
        f"Invalid connection mode: {type}"
    )
    
    
