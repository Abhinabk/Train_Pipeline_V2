from storage.object_store.s3 import get_files 
from bs4 import BeautifulSoup
from pathlib import Path

def get_stations(train_no:str):
    html_file = get_files(date='2026-05-28',type='html',train_no=train_no)[0]
    soup = BeautifulSoup(html_file,'html.parser')
    return soup.prettify()

if __name__ == "__main__":
    print(get_stations('15959'))
    