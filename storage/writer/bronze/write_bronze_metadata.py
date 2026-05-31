from duckdb import DuckDBPyConnection

from validators.bronze.metadata import BronzeTrainMetadata
def insert_bronze_train_metadata(con:DuckDBPyConnection, metadata: BronzeTrainMetadata):

    con.execute(
        """
        INSERT INTO bronze.train_metadata (
            train_no,
            train_name,
            source_url,
            file_path,
            response_status_code,
            success,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        
        """,
        [
            metadata.train_no,
            metadata.train_name,
            metadata.source_url,
            metadata.file_path,
            metadata.response_status_code,
            metadata.success,
            metadata.error_message,
        ],
    )