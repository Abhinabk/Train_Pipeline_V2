CREATE SCHEMA IF NOT EXISTS silver;
CREATE SEQUENCE IF NOT EXISTS silver.parse_metadata_seq START 1;
CREATE TABLE IF NOT EXISTS silver.parse_metadata(
    metadata_id BIGINT PRIMARY KEY DEFAULT nextval('silver.parse_metadata_seq'),
    run_date DATE UNIQUE,
    parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    station_delay_path  VARCHAR,
    route_path VARCHAR,
    fare_path VARCHAR,
    running_days_path VARCHAR
)