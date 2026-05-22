import duckdb
from pathlib import Path

def get_connection(db_file:Path):
    con = duckdb.connect(str(db_file))
    return con

