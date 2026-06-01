from pydantic import BaseModel

class StationCoordinates(BaseModel):
    longitude:float
    latitude: float 

