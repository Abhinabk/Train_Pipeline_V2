from storage.object_store.local import save_dataframe_as_csv
from storage.object_store.s3 import get_files 
from bs4 import BeautifulSoup
from config.settings import CACHE_DIR
# Attribute meaning map
FARE_ATTR_MAP = {
    "ad0":  "Adult (Normal)",
    "ad1":  "Adult (Tatkal)",
    "ch0":  "Child (Normal)",
    "ch1":  "Child (Tatkal)",
    "srf0": "Senior Female (Normal)",
    "srf1": "Senior Female (Tatkal)",
    "srm0": "Senior Male (Normal)",
    "srm1": "Senior Male (Tatkal)",
}

def get_stations(train_no:str):
    cache_file = CACHE_DIR/f"{train_no}.html"
    if cache_file.is_file():
        html_file = cache_file.read_text(encoding='utf-8')
    else:
        CACHE_DIR.mkdir(exist_ok=True)
        html_file = get_files(date='2026-05-28',type='html',train_no=train_no)[0]
        cache_file.write_text(html_file,encoding='utf-8')

    soup = BeautifulSoup(html_file,'html.parser')
    return soup
       

def get_fare_details(soup):
    #train classes
    table = html.find('table',class_='fullw nocps nolrborder')
    header_row = table.find('tr',class_='odd lighthead1')
    train_classes = [td.get_text(strip=True) for td in header_row.find_all('td')]

    #fare rows
    fare_row = table.find('tr', class_='even')
    fare_tds = fare_row.find_all('td')
    result = {}
    for i ,td in enumerate(fare_tds):
        train_class = train_classes[i]
        fare_breakdown = {}
        for attr, label in FARE_ATTR_MAP.items():
            value = td.get(attr) #as bs4 internally implements as dict
            if value:
                fare_breakdown[label] = f"Rs {value}"

        result[train_class] = fare_breakdown

    save_dataframe_as_csv(CACHE_DIR/'csv'/'fare_details.csv',result,'Fare Type')


if __name__ == "__main__":
    html = get_stations('15959')
    get_fare_details(html)
    
        
    