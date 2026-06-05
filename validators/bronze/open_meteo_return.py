from pydantic import BaseModel 

class OpenMeteoDataDaily(BaseModel):
    status_code:int|None
    station_code:str
    weather_data:dict|None