from pydantic import BaseModel 

class BronzeTrainMetadata(BaseModel):
    train_no: str
    train_name: str
    source_url: str 
    file_path: str 
    response_status_code: int
    success: bool
    error_message: str
    