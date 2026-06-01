
import re

from config.settings import REFERENCE_JSON_S3_KEY 
from parsing.station_coordinates.get_station_name_coordinates import station_names_coordinates
from parsing.get_route import route_order
from storage.readers.load_html import get_station_html

def normalize_names(name:str)->str:
    '''Use UPPER CASE FOR ALL, strips JN/JUNCTION '''
    n = name.upper().strip()
    n = re.sub(r'\s+(JN|JUNCTION)$','',n) # $ represents the end of a string  so JN but only at end
    return n


if __name__ == "__main__":
    html = get_station_html('15959')
    coordinates = station_names_coordinates(str(REFERENCE_JSON_S3_KEY)) 
    print({normalize_names(names): coords for names,coords in coordinates.items()})
    routes_stations = route_order(html,'15959')
    # print(routes_stations)