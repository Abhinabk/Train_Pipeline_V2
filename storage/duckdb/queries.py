from config.settings import SQL_DIR
from duckdb import DuckDBPyConnection
from datetime import date

def check_existing_fetch(con:DuckDBPyConnection,train_no:str)->bool:
    ''' return true if already fetch '''
    query= SQL_DIR/'bronze/check_existing_fetch.sql'
    result = con.execute(query.read_text(),[train_no]).fetchone()
    return True if result else False

def get_successful_trains(con:DuckDBPyConnection,date:date=date.today())->list[tuple]:
    '''returns train_no and s3_url returns for today if no date provided'''
    query = SQL_DIR/'silver/get_train_info.sql'
    result = con.execute(query.read_text(),[date]).fetchall()
    return result
# con = get_connection()
# check_existing_fetch(con,'15959')