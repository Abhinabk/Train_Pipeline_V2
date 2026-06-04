import yaml
from config.settings import SOURCES_YML 

def build_weather_url():
    with open(SOURCES_YML,'r') as file:
        config = yaml.safe_load(file)

    base_url = config.get("open-meteo",{}).get("base_url")
    if not base_url:
        raise ValueError("url:not found in sources.yaml")
    
    return base_url
