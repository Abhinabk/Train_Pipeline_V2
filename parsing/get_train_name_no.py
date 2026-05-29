from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def train_name_no(soup:BeautifulSoup,train_no:str)->list[dict]:
    div = soup.find('div',class_='flexRow flexG1')
    span = div.find('span',class_='exp').get_text(strip=True)
    result = []
    result.append({
        'train_no':train_no,
        'train_name_no':"-".join(span.split(" "))
    })
    return result

if __name__ == "__main__":
    html = get_station_html('15959')
    print(train_name_no(html,'15959'))




        
    