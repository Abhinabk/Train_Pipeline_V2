from datetime import date

from pydantic import BaseModel 

class SilverTrainMetadata(BaseModel):
    run_date:date
    station_delay_path:str
    route_path:str
    fare_path:str
    running_days_path:str

#have to make object after paths are known to be path or None 