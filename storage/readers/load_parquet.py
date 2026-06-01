
import duckdb

def load_parquet(data_path:str)->list[tuple]:
    return duckdb.execute('''
                SELECT * FROM read_parquet(?)
            ''',[data_path]).fetchall()

def load_distinct_route_stations_parquet(route_path:str)->list[tuple]|None:
    ''' get path form s3 metadata return distinct station_code and station_name for route parquet file'''
    result = duckdb.execute('''
        SELECT DISTINCT station_code,station_name FROM read_parquet(?)
    ''',[route_path]) # distinct on the pair so if station_name diff even though 
                                # station_code duplicate get both the result 
    if result:
        return result.fetchall()
    else:
        return

