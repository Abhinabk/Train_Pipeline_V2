from config.settings import SQL_DIR
from duckdb import DuckDBPyConnection
from datetime import date

def check_existing_fetch(con:DuckDBPyConnection,train_no:str,run_date:date)->bool:
    ''' return true if already fetch '''
    query= SQL_DIR/'bronze/check_existing_fetch.sql'
    result = con.execute(query.read_text(),[train_no,run_date]).fetchone()
    return True if result else False

def check_existing_weather(con:DuckDBPyConnection,station_code:str,run_date:date):
    ''' return true if already fetch '''
    query= SQL_DIR/'bronze/check_existing_weather.sql'
    result = con.execute(query.read_text(),[station_code,run_date]).fetchone()
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
    
def get_min_max_date(con:DuckDBPyConnection,run_date:date)->tuple:
    '''return a tuple containing (min_date,max_date)'''
    path = con.execute("""
        SELECT 
            station_delay_path 
        FROM silver.parse_metadata
        WHERE run_date = ?
    """,[run_date]).fetchone()
    if not path:
        raise ValueError(f"No path found check data for run_date={run_date} exists")

    result =  con.execute("""
    SELECT MIN(date::DATE), MAX(date::DATE)
    FROM read_parquet(?)
    """, [path[0]]).fetchone() #will return (None,None) on filure
    if result is None or result[0] is None:
        raise ValueError(f"No rows found in parquet file {path[0]}")
    
    return result

def get_station_coords(con:DuckDBPyConnection,run_date:date)->list[tuple]:
    '''
    return list of tuple containing [(station_code,station_name,log,latitude),...]
    for run_date provided make sure reference ran on that day
    '''
    path = con.execute("""
        SELECT matched_key
        FROM reference.metadata
        WHERE run_date = ?
    """,[run_date]).fetchone()
    if not path:
        raise ValueError(f"No path found check for run_date={run_date} exists")
    result =  con.execute("""
        SELECT station_code, longitude, latitude FROM read_parquet(?)   
    """,[path[0]]).fetchall() #return [] on failure
    if not result:
        raise ValueError(f"No rows found in parquet file {path[0]}")
    return result

