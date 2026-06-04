CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SEQUENCE IF NOT EXISTS bronze.train_metadata_seq START 1;

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
                                -- new data just appends insed of updating ista a surrogate key
                                -- no meing uisng natural key key to geive meaninig and do
                                -- update on new runs rather then appends
);
