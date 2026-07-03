from datetime import datetime

from dotenv import load_dotenv
from orchestration.train_ingestion.run_ingestion import ingest_all_trains
from orchestration.weather.run_weather import ingest_all_stations
from orchestration.parser.run_parser import parse_all_trains
from orchestration.reference.run_route_to_coords import write_route_coords_all
from orchestration.weather.weather_table import load_weather_to_bronze
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.init_db import init_db
from argparse import ArgumentParser 

load_dotenv(override=True) 

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-f","--force",
        action="store_true",
        help="forced run of the pipeline"
    )
    parser.add_argument(
        "-fp","--force-parse",
        action="store_true",
        help="forced reparse for same day run"
    )
    parser.add_argument(
        "-fi","--force-ingest",
        action="store_true",
        help="forced ingestion for same day run"
    )
    parser.add_argument(
        "-fw","--force-weather",
        action="store_true",
        help="forced weather api for same day run"
    )
    parser.add_argument(
        "-fr","--force-reference",
        action="store_true",
        help="forced to rerun reference"
    )

    parser.add_argument(
        "-p", "--parser-only",
        action="store_true",
        help="run only parser stage"
    )
    args = parser.parse_args()

    with get_connection() as con: 
        #single shared conn passed through flows/tasks
        #better way is to let each task ahve its own connection
        run_date = datetime.today().date()
        init_db(con)

        if args.force:
            ingest_all_trains(con,run_date,force=True) #sequential scraper
            parse_all_trains(con,run_date,force=True) #parallel parser
            write_route_coords_all(con,run_date,force=True) # creates the refernce table
            ingest_all_stations(con,run_date,force= True) # fetches the weather per station
            load_weather_to_bronze(con)
        else: 
            ingest_all_trains(con,run_date, force=args.force_ingest) #sequential scraper
            parse_all_trains(con,run_date,force=args.force_parse) #parallel parser
            if args.force_reference: #this runs only for force-refernce flag
                write_route_coords_all(con,run_date,force=True) # creates the refernce table
            ingest_all_stations(con,run_date,force=args.force_weather) # fetches the weather per station
            load_weather_to_bronze(con,run_date)