# Attribute meaning map
from bs4 import BeautifulSoup
from storage.readers.load_html import get_station_html


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

def fare_details(soup:BeautifulSoup):
    #train classes
    table = soup.find('table',class_='fullw nocps nolrborder')
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

    return result

if __name__ == "__main__":
    html = get_station_html('15959')
    fare_details(html)
    