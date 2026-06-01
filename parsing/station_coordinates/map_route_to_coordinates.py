
from pprint import pprint

from config.settings import REFERENCE_JSON_S3_KEY 
from parsing.station_coordinates.get_station_name_coordinates import station_names_coordinates
from parsing.get_route import route_order
from parsing.station_coordinates.normalize_names import normalize_names
from storage.readers.load_html import get_station_html
from config.logger import silver_logger


def route_to_coords(route_stations:list[dict],coords:dict)->dict[str,list[dict]]:
    matched,missing = [],[]
    for s in route_stations:
        key = normalize_names(s['station_name'])
        if key in coords:
            item = coords[key]
            matched.append({
                'station_code':s['station_code'],
                'station_name':s['station_name'],
                'longitude':item.longitude,
                'latitude':item.latitude
            })
        else:
            missing.append({
                'station_code':s['station_code'],
                'station_name':s['station_name'],
            })
            silver_logger.warning(f"no coordinate match: {s['station_code']} {s['station_name']}")
    return {"matched": matched, "missing": missing}

if __name__ == "__main__":
    html = get_station_html('15959')
    ref_coordinates = station_names_coordinates(str(REFERENCE_JSON_S3_KEY)) 
    route_stations = route_order(html,'15959')
    result = route_to_coords(route_stations,ref_coordinates)
    print("matched")
    pprint(result['matched'])
    print("missing")
    pprint(result['missing'])



