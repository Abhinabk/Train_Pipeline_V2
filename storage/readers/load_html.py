from bs4 import BeautifulSoup
from config.settings import CACHE_DIR
from storage.object_store.s3 import get_files


def get_station_html(train_no:str,local_cache:bool=True)->BeautifulSoup:
    cache_file = CACHE_DIR/f"{train_no}.html"
    if local_cache:
        if cache_file.is_file():
            html_file = cache_file.read_text(encoding='utf-8')#pathlib file reader
        else:
            CACHE_DIR.mkdir(exist_ok=True)
            html_file = get_files(date='2026-05-28',type='html',train_no=train_no)[0]
            cache_file.write_text(html_file,encoding='utf-8')
        return BeautifulSoup(html_file,'html.parser')
    
    html_file = get_files(date='2026-05-28',type='html',train_no=train_no)[0]
    return BeautifulSoup(html_file,'html.parser')
