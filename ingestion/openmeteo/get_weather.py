import requests

from ingestion.openmeteo.build_url import build_weather_url

def fetch_weather_daily(session:requests.Session,longitude:float,latitude:float,start_date:str,end_date:str,station_code:str):
    url = build_weather_url()
    params = {
    "latitude": latitude,
	"longitude": longitude,
	"start_date": start_date,
	"end_date": end_date,
	"daily": [
        "temperature_2m_mean", 
        "precipitation_sum",
        "rain_sum", 
        "daylight_duration", 
        "wind_gusts_10m_max", 
        "weather_code"],
	    "timezone": "auto",
    }
    response = session.get(url=url,params=params)
    response.raise_for_status() #will raise http code if error
    return {
        "station_code":station_code,
        "weather_daily":response.json()
    }
    
            
