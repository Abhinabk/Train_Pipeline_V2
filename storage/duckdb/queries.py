from config.settings import SQL_DIR
from duckdb import DuckDBPyConnection

check_existing_sql = SQL_DIR/'bronze/check_existing_fetch.sql'

def check_existing_fetch(con:DuckDBPyConnection,train_no:str)->bool:
    ''' return true if already fetch '''
    result = con.execute(check_existing_sql.read_text(),[train_no]).fetchone()
    return True if result else False

# con = get_connection()
# check_existing_fetch(con,'15959')