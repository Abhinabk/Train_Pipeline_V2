from parsing.station_coordinates.normalize_names import normalize_names
from storage.readers.load_json import load_json
from validators.silver.coordinates import StationCoordinates
from config.logger import silver_logger

def station_names_coordinates(s3_key:str)->dict[str,StationCoordinates]:
    coordinates_file =  load_json(s3_key)
    lookup = {}
    for feature_dict in coordinates_file['features']:
        try:
            station_name = feature_dict['properties']['name']
            station_coords = StationCoordinates(
                longitude=float(feature_dict['geometry']['coordinates'][0]),
                latitude=float(feature_dict['geometry']['coordinates'][1])
            )
        except(KeyError,TypeError) as e:
            silver_logger.warning(f"skipped GeoJSON feature: {e}")
            continue
        # if station_name in lookup:
        #     silver_logger.warning(f"duplicate station name, overwriting: {station_name}")
        key= normalize_names(station_name)
        lookup[key] = station_coords
    return lookup