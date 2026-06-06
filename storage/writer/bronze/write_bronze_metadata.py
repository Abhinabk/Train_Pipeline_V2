from duckdb import DuckDBPyConnection

from validators.bronze.metadata import BronzeTrainMetadata,OpenMeteoMetadata
def insert_bronze_train_metadata(con:DuckDBPyConnection, metadata: BronzeTrainMetadata):

    con.execute(
        """
        INSERT INTO bronze.train_metadata (
            run_date,
            train_no,
            train_name,
            source_url,
            file_path,
            response_status_code,
            success,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(train_no,run_date) DO UPDATE SET
            train_name  = EXCLUDED.train_name,
            source_url  = EXCLUDED.source_url,
            file_path   = EXCLUDED.file_path,
            response_status_code = EXCLUDED.response_status_code,
            success = EXCLUDED.success,
            error_message   = EXCLUDED.error_message
        """,
        [   
            metadata.run_date,
            metadata.train_no,
            metadata.train_name,
            metadata.source_url,
            metadata.file_path,
            metadata.response_status_code,
            metadata.success,
            metadata.error_message,
        ],
    )

def insert_open_meteo_metadata(con:DuckDBPyConnection, rows:list[tuple]):

    con.executemany(
        """
        INSERT INTO bronze.open_meteo_metadata (
            run_date,
            weather_start,
            weather_end,
            station_code,
            file_path,
            response_status_code,
            success,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(station_code,run_date) DO UPDATE SET
            weather_start = EXCLUDED.weather_start,
            weather_end = EXCLUDED.weather_end,
            file_path = EXCLUDED.file_path,
            response_status_code = EXCLUDED.response_status_code,
            success = EXCLUDED.success,
            error_message = EXCLUDED.error_message
        """,
       rows,
    )