
from bs4 import BeautifulSoup
from duckdb import DuckDBPyConnection
import pandas as pd
from parsing.get_fare import fare_details
from parsing.get_route import route
from parsing.get_station_delay import station_delay
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.queries import get_successful_trains
from datetime import date, datetime
from config.logger import silver_logger
from storage.object_store.s3 import get_object_from_uri
from storage.writer.silver.write_silver_parquet import write_parquet_to_s3
from transformations.silver.station_delay import transform_station_delay_to_long


def parse_all_trains(con:DuckDBPyConnection,run_date:date):
    all_train_s3_url = get_successful_trains(con,run_date)
    all_station_delay = []
    all_route = []
    all_fare = []
    for train_no,s3_uri in all_train_s3_url:
        html = get_object_from_uri(s3_uri)
        soup = BeautifulSoup(html, "html.parser")
        all_station_delay.extend(
            station_delay(soup, train_no)
        )

        all_route.extend(
            route(soup, train_no)
        )

        all_fare.extend(
            fare_details(soup, train_no)
        )
        silver_logger.success(f"Processed train {train_no}")
        break
    #tranform to dataframe
    if all_station_delay:
        station_delay_df = transform_station_delay_to_long(
            all_station_delay
        )
    route_df = pd.DataFrame(
        all_route
    )

    fare_df = pd.DataFrame(
        all_fare
    )
    #to parquet
    write_parquet_to_s3(station_delay_df,'station_delay',run_date)
    write_parquet_to_s3(route_df,'route_order',run_date)
    write_parquet_to_s3(fare_df,'fare_details',run_date)

if __name__ == "__main__":
    with get_connection() as con:
        run_date = datetime.fromisoformat("2026-05-27").date()
        parse_all_trains(con,run_date)





