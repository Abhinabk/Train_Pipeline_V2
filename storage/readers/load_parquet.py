import duckdb

def load_parquet(path:str,local_cache:bool=True):
    return duckdb.execute('''
        SELECT * FROM read_parquet(?)
    ''',[path])