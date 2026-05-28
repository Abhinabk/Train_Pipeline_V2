from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def running_days(soup:BeautifulSoup)->list[str]:
    tr = soup.find('tr',class_='even dborder')
    td = tr.find('td',class_='nobl').get_text(strip=True)
    days = td.split(":")[-1].strip(" ")
    return days.split()


if __name__ == "__main__":
    html = get_station_html('15959')
    print(running_days(html))




        
    