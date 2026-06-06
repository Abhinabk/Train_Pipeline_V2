from datetime import date
from pprint import pprint

import requests

from ingestion.openmeteo.build_url import build_weather_url
from storage.duckdb.duckdb_con import get_connection
from storage.duckdb.queries import  get_min_max_date, get_station_coords
from validators.bronze.open_meteo_return import OpenMeteoDataDaily
def fetch_weather_daily(session:requests.Session,station_code:str,longitude:float,latitude:float,start_date:str,end_date:str)->OpenMeteoDataDaily:
    '''return the station_code with a json of weather variables'''
    url = build_weather_url()
    params = {
    "latitude": latitude,
	"longitude": longitude,
	"start_date": start_date,
	"end_date": end_date,
	"daily": [
        "temperature_2m_mean", #mean temp in C
        "precipitation_sum", #rain + snow all lizuid accumulated in mm
        "rain_sum", #total liquid rainfall for the day, in millimeters
        "daylight_duration", #in sec
        "wind_gusts_10m_max", 
        "weather_code"],
    } #values are indexed by date so returns a data for index implicitly defaults to utc bucketing
    response = session.get(url=url,params=params,timeout=40) 
    response.raise_for_status() #will raise http code if error None if success
    data = OpenMeteoDataDaily(
        status_code=response.status_code,
        station_code = station_code,
        weather_data=response.json()['daily']
    )
    return data 
if __name__ == "__main__":
    with get_connection() as con:
        print(con.execute("SELECT current_database()").fetchone())
        min_max = get_min_max_date(con,run_date=date.today())
        station_code,longitude,latitude  = get_station_coords(con,date.today())[0]
    if min_max:
        min_date,max_date = min_max
    with requests.Session() as session:
        data = fetch_weather_daily(session,station_code,longitude,latitude,min_date,max_date)
        pprint(data)
            
