from datetime import date
import json
from config.logger import bronze_logger
from duckdb import DuckDBPyConnection
from config.settings import S3_BUCKET, S3_PREFIX_BRONZE_WEATHER
from storage.object_store.s3 import save_json_s3
from storage.writer.bronze.write_bronze_metadata import insert_open_meteo_metadata
from validators.bronze.metadata import OpenMeteoMetadata


def write_insert(con:DuckDBPyConnection,run_date:date,work:list[tuple],prefect_states):
    rows = []
    for  (code, _, _, start_date, end_date), state in zip(work, prefect_states):
        if state.is_completed():
            r = state.result()  # actual value returned by the task
            try:
                file_path = save_json_s3(
                    S3_BUCKET,
                    f"{S3_PREFIX_BRONZE_WEATHER}/{run_date}/{code}.json",
                    content=json.dumps(r.weather_data),
                )
            except RuntimeError as e:
                rows.append((run_date, None, None, code, None,
                             None, False, f"S3 write failed: {e}"))
                bronze_logger.warning(f"S3 write failed for {code}: {e}")
                continue 
            metadata = OpenMeteoMetadata(
                run_date=run_date,
                weather_start=start_date,
                weather_end=end_date,
                station_code=code,
                file_path=file_path,
                response_status_code=r.status_code,
                success=True,
                error_message=None
            ) 
            bronze_logger.success(f"Fetched {code} weather")
        else:
            metadata = OpenMeteoMetadata(
                run_date=run_date,
                weather_start=None,
                weather_end=None,
                station_code=code,
                file_path=None,
                response_status_code=None,
                success=False,
                error_message=str(state.message)
            )
            
            bronze_logger.warning(f"Failed {code} weather:{state.message}")

        #all completed metadata gets added 
        rows.append((metadata.run_date, metadata.weather_start, metadata.weather_end, metadata.station_code,
                    metadata.file_path,
                    metadata.response_status_code, metadata.success, metadata.error_message))
    if rows:
        insert_open_meteo_metadata(con, rows) #now a single trip to insert all 
