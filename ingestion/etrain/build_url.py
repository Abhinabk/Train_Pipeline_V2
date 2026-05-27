import yaml
from config.settings import SOURCES_YML

with open(SOURCES_YML,'r') as file:
    config = yaml.safe_load(file)

BASE_URL = config.get("etrain", {}).get("base_url")

def build_train_url(train_no:str,train_name:str,time:str="1y"):
    safe_train_name = train_name.strip().replace(" ", "-")
    url = f"{BASE_URL}/{safe_train_name}-{train_no}/history?d={time}"
    return url
