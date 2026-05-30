def insert_silver_metadata(con, metadata: dict):

    con.execute(
        """
        INSERT INTO silver.parse_metadata (
            run_date,
            station_delay_path,
            route_path,
            fare_path
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            metadata["run_date"],
            metadata["station_delay_path"],
            metadata["route_path"],
            metadata["fare_path"]
        ],
    )