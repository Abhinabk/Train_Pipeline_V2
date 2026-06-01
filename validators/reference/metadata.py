
from datetime import date

from pydantic import BaseModel

class ReferenceMetadata(BaseModel):
    run_date: date    
    matched_key: str 
    missing_key: str
    matched_count: int
    missing_count:int
