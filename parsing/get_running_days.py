from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def running_days(soup:BeautifulSoup,train_no:str)->list[dict]:
    tr = soup.find('tr',class_='even dborder')
    td = tr.find('td',class_='nobl').get_text(strip=True)
    days = td.split(":")[-1].strip(" ")
    result = []
    result.append({
        'train_no':train_no,
        'days':days.split()
        })
    return result

if __name__ == "__main__":
    html = get_station_html('15959')
    print(running_days(html,'15959'))




        
    