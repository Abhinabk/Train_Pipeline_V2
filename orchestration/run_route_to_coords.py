
from datetime import date, datetime

from duckdb import DuckDBPyConnection
import pandas as pd
from config.logger import generic_logger
from config.settings import REFERENCE_JSON_S3_KEY
from parsing.station_coordinates.get_station_name_coordinates import station_names_coordinates
from parsing.station_coordinates.map_route_to_coordinates import route_to_coords
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.queries import get_route_path
from storage.readers.load_parquet import load_distinct_route_stations_parquet
from prefect import flow,task

from storage.writer.reference.write_reference_metadata import insert_reference_metadata
from storage.writer.common.write_parquet import write_parquet_to_s3
from validators.reference.metadata import ReferenceMetadata

@task(name="write-route-coords")
def write_route_coords(rows: list[dict], file_name: str, run_date: date):
    df = pd.DataFrame(rows)
    key =  write_parquet_to_s3(df,file_name,run_date,prefix='reference')
    return key 

@flow(name="all-route-to-coords")
def write_route_coords_all(con:DuckDBPyConnection,run_date:date):
    ref_coordinates = station_names_coordinates(str(REFERENCE_JSON_S3_KEY)) 
    path = get_route_path(con,run_date)
    if path is None:
        generic_logger.error(f"Path not found: {path}")
        return
    distinct_stations = load_distinct_route_stations_parquet(path)
    if not distinct_stations:
        generic_logger.error("No stations found")
        return 
    
    result = route_to_coords(distinct_stations,ref_coordinates)
    records = [
        write_route_coords(result['matched'],"matched_coords",run_date),
        write_route_coords(result['missing'],"missing_coords",run_date)
    ]
    metadata = ReferenceMetadata(
        run_date=run_date,
        matched_key=records[0],
        missing_key=records[1],
        matched_count=len(result['matched']),
        missing_count=len(result['missing'])
    )
    if len(result['missing'])>0:
        codes = [s['station_code'] for s in result['missing']]
        generic_logger.warning(f"Missing coordinates {codes}")
    insert_reference_metadata(con,metadata)


if __name__ == "__main__":
    run_date = datetime.today().date()
    with get_connection() as con:
        write_route_coords_all(con,run_date)

