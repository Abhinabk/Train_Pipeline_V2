from datetime import date
from pprint import pprint
import re
from config.logger import silver_logger
from storage.readers.load_html import get_station_html
from bs4 import BeautifulSoup


def station_delay(soup:BeautifulSoup,train_no:str)->list[dict]:
    '''return dalay data in wide format have to tranform to'''
    pattern = re.compile(r'et\.rsStat\.tooltipData\s*=\s*(\[[\s\S]*?\]);',re.DOTALL)
    block_text = None
    for script in soup.find_all('script'):
        text = script.get_text()
        if 'tooltipData' in text:
            block_text = text
            break

    if block_text is None:
        silver_logger.log('SKIP', f"no tooltipData for train {train_no}")
        return []

    full_block = re.search(pattern, block_text)
    if full_block is None:
        raise ValueError(f"tooltipData found but failed to parse for train {train_no}")
        #dropping 12097 (Agartala-Khongsang Jan Shatabdi) from config very sparse points tri-weelky
        #causing miss regex return None even tough samll amount of data present
    
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




        
    