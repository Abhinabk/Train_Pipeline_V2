CREATE SCHEMA IF NOT EXISTS reference;
CREATE TABLE IF NOT EXISTS reference.metadata(
    run_date     DATE PRIMARY KEY,
    matched_key  TEXT,
    missing_key  TEXT,
    matched_count INT,
    missing_count INT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);