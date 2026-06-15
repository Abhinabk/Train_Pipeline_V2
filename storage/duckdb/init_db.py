from config.settings import SQL_DIR
from storage.duckdb.duckdb_con import get_connection

create_bronze_metadata_sql = SQL_DIR/"bronze"/"create_metadata.sql" 
create_weather = SQL_DIR/"bronze"/"create_weather.sql"
create_silver_metadata_sql = SQL_DIR/"silver"/"create_metadata.sql" 
create_reference_metadata_sql = SQL_DIR/"reference"/"create_metadata.sql"
def init_db(con):
    con.execute(create_bronze_metadata_sql.read_text())
    con.execute(create_silver_metadata_sql.read_text())
    con.execute(create_reference_metadata_sql.read_text())
    con.execute(create_weather.read_text())

if __name__ == "__main__":
    with get_connection() as con:
        init_db(con)