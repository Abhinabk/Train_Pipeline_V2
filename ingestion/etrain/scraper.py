
from datetime import date

from config.settings import BRONZE_HTML_DIR,S3_BUCKET,S3_PREFIX_BRONZE_TRAIN 
from ingestion.etrain.fetch import fetch_html
from storage.object_store.local import save_html
from storage.object_store.s3 import save_html_s3

def fetch_train_history(url,session,train_no,train_name,year="1y",storage="local"):
    '''Fetches train data and returns the metadata
        have to updte response code , success and error_message
        on excpetion
        ** fetch already does raise_for_status() 
    '''
    response = fetch_html(session, url)
    html = response.get('html',"")
    if storage == "local":
        file_path = (BRONZE_HTML_DIR/f"{date.today()}_{train_name}_{train_no}.html")
        save_html(file_path, html)     
      
    elif storage == "s3":
        #buck alraedy given in argument no need to append to key path
        key = f"{S3_PREFIX_BRONZE_TRAIN}/{date.today()}_{train_name}_{train_no}.html"
        file_path = save_html_s3(S3_BUCKET,key,html)

    else:
        raise ValueError(f"Unknown storage type: {storage}")
    
    return {
        "file_path":str(file_path),
        "response_status_code": response.get("status_code",None),
    }
    




