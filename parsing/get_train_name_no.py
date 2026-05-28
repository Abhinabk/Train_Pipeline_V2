from config.settings import CACHE_DIR
from storage.object_store.local import save_dataframe_as_csv
from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def train_name_no(soup:BeautifulSoup):
    div = soup.find('div',class_='flexRow flexG1')
    span = div.find('span',class_='exp').get_text(strip=True)
    return span

if __name__ == "__main__":
    html = get_station_html('15959')
    print(train_name_no(html))




        
    