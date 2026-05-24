from datetime import datetime

def insert_bronze_train_metadata(con, metadata: dict):

    con.execute(
        """
        INSERT INTO bronze.train_metadata (
            train_no,
            train_name,
            source_url,
            file_path,
            fetched_at,
            response_status_code,
            success,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            metadata["train_no"],
            metadata["train_name"],
            metadata["source_url"],
            metadata["file_path"],
            datetime.now(),
            metadata["response_status_code"],
            metadata["success"],
            metadata["error_message"],
        ],
    )