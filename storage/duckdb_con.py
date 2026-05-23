import duckdb
from config.settings import DUCK_DB_DATABASE
def get_connection():
    DUCK_DB_DATABASE.parent.mkdir(parents=True,exist_ok=True)
    return duckdb.connect(str(DUCK_DB_DATABASE))
    
