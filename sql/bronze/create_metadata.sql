CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SEQUENCE IF NOT EXISTS bronze.train_metadata_seq START 1;
CREATE SEQUENCE IF NOT EXISTS bronze.open_meteo_metadata_seq START 1
CREATE TABLE IF NOT EXISTS bronze.train_metadata(
    metadata_id BIGINT PRIMARY KEY DEFAULT nextval('bronze.train_metadata_seq'),
    run_date DATE,
    train_no VARCHAR,
    train_name VARCHAR,
    source_url VARCHAR,
    file_path VARCHAR,
    response_status_code INT,
    success BOOLEAN,
    error_message VARCHAR,
    UNIQUE (train_no, run_date) --cause metadata_id will create new id for reruns so no 
                                -- new data just appends insed of updating its a surrogate key
                                -- has no meaning using natural key  to give meaning and so
                                -- updates on new runs rather then appends
);
CREATE TABLE IF NOT EXISTS bronze.open_meteo_metadata(
    metadata_id BIGINT PRIMARY KEY DEFAULT nextval('bronze.train_metadata_seq'),
    run_date DATE,
    station_code VARCHAR,
    file_path VARCHAR,
    response_status_code INT,
    success BOOLEAN,
    error_message VARCHAR,
    UNIQUE (station_code, run_date) --run date couse just staion_code will crete conflict
                                    -- for different day also
);

