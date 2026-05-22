CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SEQUENCE IF NOT EXISTS bronze.metadata_seq START 1;

CREATE TABLE IF NOT EXISTS bronze.metadata(
    metadata_id BIGINT PRIMARY KEY DEFAULT nextval('bronze.metadata_seq'),
    train_no INT,
    train_name VARCHAR,
    source_url VARCHAR,
    file_path VARCHAR,
    fetched_at TIMESTAMP,
    response_status_code INT,
    success BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message VARCHAR
);