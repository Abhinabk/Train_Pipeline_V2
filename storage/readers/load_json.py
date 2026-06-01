import json
from pathlib import Path
from config.settings import CACHE_DIR 
from config.settings import S3_BUCKET
from storage.object_store.s3 import get_object

def load_json(data:str,local_cache:bool=True)->dict:
    cache_file = CACHE_DIR/f"{Path(data).stem}.geojson"
    station_full_key = data
    if local_cache:
        if cache_file.is_file():
            return json.loads(cache_file.read_text())
        else:
            CACHE_DIR.mkdir(exist_ok=True)
            raw_data = get_object(bucket=S3_BUCKET, key=station_full_key)
            cache_file.write_text(raw_data)
            return json.loads(raw_data)
        
    return json.loads(get_object(bucket=S3_BUCKET, key=station_full_key))
