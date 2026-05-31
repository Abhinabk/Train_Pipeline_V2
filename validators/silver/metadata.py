from datetime import date

from pydantic import BaseModel 

class SilverTrainMetadata(BaseModel):
    run_date:date
    station_delay_path:str|None
    route_path:str|None
    fare_path:str|None
    running_days_path:str|None

#have to make object after paths are known to be path or None 