from pprint import pprint

from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def route_order(soup:BeautifulSoup,train_no:str)->list[dict]:
    select = soup.find('select',attrs={'name':'src'})
    routes = select.find_all('option')
    result = []
    order = 1
    for r in routes:
        station_code = r.get('value')
        station_name = r.get_text(strip=True)
        result.append(
            {'train_no':train_no,
             'station_code':station_code,
             'station_name':station_name,
             'order':order
             })
        order+=1
    return result


if __name__ == "__main__":
    html = get_station_html('15959')
    pprint(route(html,'15959'))




        
    