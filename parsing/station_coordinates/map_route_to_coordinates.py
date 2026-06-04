
from pprint import pprint

from config.manual_coords import MANUAL_COORDS
from config.settings import REFERENCE_JSON_S3_KEY 
from parsing.station_coordinates.get_station_name_coordinates import station_names_coordinates
from parsing.station_coordinates.normalize_names import normalize_names
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.queries import get_route_path
from config.logger import silver_logger
from datetime import datetime

from storage.readers.load_parquet import load_distinct_route_stations_parquet

def route_to_coords(route_stations:list[tuple],coords:dict)->dict[str,list[dict]]:
    matched,missing = [],[]
    for station_code,station_name in route_stations:
        key = normalize_names(station_name) #the return key is noramlized not the station_name itself
        if key in coords:
            item = coords[key]
            matched.append({
                'station_code':station_code,
                'station_name':station_name,#saved as original station_name
                'longitude':item.longitude,
                'latitude':item.latitude
            })
        else:
            if station_code in MANUAL_COORDS:
                longitude,latitude = MANUAL_COORDS[station_code]
                missing.append({
                    'station_code':station_code,
                    'station_name':station_name,
                    'longitude':longitude,
                    'latitude':latitude
                })
            else:
                silver_logger.warning(f"no coordinate match: {station_code} {station_name}")
    return {"matched": matched, "missing": missing}

if __name__ == "__main__":
    ref_coordinates = station_names_coordinates(str(REFERENCE_JSON_S3_KEY)) 
    with get_connection() as con:
        route_stations_path = get_route_path(con,datetime.today().date())
        if route_stations_path:
            route_stations = load_distinct_route_stations_parquet(route_stations_path)
        if route_stations:
            result = route_to_coords(route_stations,ref_coordinates)

    print("matched")
    pprint(result['matched'])
    print("missing")
    pprint(result['missing'])



