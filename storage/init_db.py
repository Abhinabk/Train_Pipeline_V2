from storage.duckdb_con import get_connection
from config.settings import SQL_DIR

create_bronze_metadata_sql = SQL_DIR/"bronze/create_metadata.sql" 

with get_connection() as con:
    con.execute(create_bronze_metadata_sql.read_text())