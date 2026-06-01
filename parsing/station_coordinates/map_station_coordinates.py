
from config.settings import REFERENCE_JSON_S3_KEY 
from parsing.station_coordinates.get_station_name_coordinates import station_names_coordinates



if __name__ == "__main__":
    coordinates = station_names_coordinates(str(REFERENCE_JSON_S3_KEY))
    print(coordinates)