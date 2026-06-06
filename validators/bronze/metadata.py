from datetime import date

from pydantic import BaseModel 

class OpenMeteoMetadata(BaseModel):
    run_date: date
    weather_start: date|None
    weather_end: date|None
    station_code: str
    file_path: str|None
    response_status_code: int|None
    error_message: str|None
    success: bool
    
class BronzeTrainMetadata(BaseModel):
    run_date: date
    train_no: str
    train_name: str
    source_url: str 
    file_path: str|None
    response_status_code: int|None
    error_message: str|None
    success: bool

'''#|None allows the values to be None while 
=NOne allows to make a object without specifing the field at start 
but since i am making a object per branch(pass/fail) i will know the path
so no need for file_path: str|None = None
'''

