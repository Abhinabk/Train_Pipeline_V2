from config.settings import CACHE_DIR
from storage.object_store.local import save_dataframe_as_csv
from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def running_days(soup:BeautifulSoup):
    pass

if __name__ == "__main__":
    html = get_station_html('15959')
    running_days(html)




        
    