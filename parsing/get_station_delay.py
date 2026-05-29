from datetime import date
from pprint import pprint
import re

from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def station_delay(soup:BeautifulSoup,train_no:str)->list[dict]|dict:
    '''return dalay data in wide format have to tranform to'''
    pattern = re.compile(r'et\.rsStat\.tooltipData\s*=\s*(\[[\s\S]*?\]);',re.DOTALL)
    full_block = None
    for script in soup.find_all('script'):
        text = script.get_text()
        if 'tooltipData' in text:
            full_block = re.search(pattern,text)
            break
    if not full_block:
        return {}
    block = full_block.group(1)
    labels = re.findall(r"'label':'(\w+)'",block)
    rows = re.findall(r'\[new Date\((\d{4}),(\d{1,2}),(\d{1,2})\)((?:,(?:-?\d+|null))+)\]',block)
    time_data = []
    for year,month,days,value_str in rows:
        values = [None if v == 'null' else int(v) for v in value_str.split(',') if v]
        time_data.append({
            'train_no':train_no,
            'date':date(int(year),int(month)+1,int(days)),
            **dict(zip(labels,values))
        })
    return time_data 


if __name__ == "__main__":
    html = get_station_html('15959')
    pprint(station_delay(html,'15959'))




        
    