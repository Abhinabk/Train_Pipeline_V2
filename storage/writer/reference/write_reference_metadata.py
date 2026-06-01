from duckdb import DuckDBPyConnection

from validators.reference.metadata import ReferenceMetadata
def insert_reference_metadata(con:DuckDBPyConnection,metadata:ReferenceMetadata):
    con.execute(
        """
        INSERT OR REPLACE INTO reference.metadata
            (run_date, matched_key, missing_key,matched_count,missing_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
        metadata.run_date,
        metadata.matched_key, 
        metadata.missing_key,
        metadata.matched_count,
        metadata.missing_count,
        ],
    )