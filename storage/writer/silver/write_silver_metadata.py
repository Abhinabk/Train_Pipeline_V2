def insert_silver_metadata(con, metadata: dict):

    con.execute(
        """
        INSERT INTO silver.parse_metadata (
            run_date,
            station_delay_path,
            route_path,
            fare_path,
            running_days_path
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT (run_date) DO UPDATE SET
            station_delay_path= EXCLUDED.station_delay_path,
            route_path =  EXCLUDED.route_path,
            fare_path =  EXCLUDED.fare_path,
            running_days_path =  EXCLUDED.running_days_path
        """,
        [
            metadata["run_date"],
            metadata["station_delay_path"],
            metadata["route_path"],
            metadata["fare_path"],
            metadata["running_days_path"]
        ],
    )