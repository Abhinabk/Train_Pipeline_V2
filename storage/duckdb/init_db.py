from config.settings import SQL_DIR

create_bronze_metadata_sql = SQL_DIR/"bronze"/"create_metadata.sql" 
create_silver_metadata_sql = SQL_DIR/"silver"/"create_metadata.sql" 
def init_db(con):
    con.execute(create_bronze_metadata_sql.read_text())
    con.execute(create_silver_metadata_sql.read_text())
    