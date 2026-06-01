from config.settings import SQL_DIR
from duckdb import DuckDBPyConnection
from datetime import date

def check_existing_fetch(con:DuckDBPyConnection,train_no:str,run_date:date)->bool:
    ''' return true if already fetch '''
    query= SQL_DIR/'bronze/check_existing_fetch.sql'
    result = con.execute(query.read_text(),[train_no,run_date]).fetchone()
    return True if result else False

def check_existing_parse(con:DuckDBPyConnection,run_date:date)->bool:
    query= SQL_DIR/'silver/check_existing_parse.sql'
    result = con.execute(query.read_text(),[run_date]).fetchone()
    return True if result else False

def get_successful_trains(con:DuckDBPyConnection,run_date:date)->list[tuple]:
    '''returns train_no and s3_url returns for today if no date provided'''
    query = SQL_DIR/'silver/get_train_info.sql'
    result = con.execute(query.read_text(),[run_date]).fetchall()
    return result

def get_route_path(con:DuckDBPyConnection,run_date:date)->str|None:
    query =  SQL_DIR/'silver/get_route_path.sql'
    result = con.execute(query.read_text(),[run_date]).fetchone()
    if result:
        return result[0]
# con = get_connection()
# check_existing_fetch(con,'15959')