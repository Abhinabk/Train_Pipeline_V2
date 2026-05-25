
from datetime import date

from config.settings import BRONZE_HTML_DIR
from ingestion.etrain.fetch import fetch_html
from storage.object_store.local import save_html

def fetch_train_history(url,session,train_no,train_name,year="1y"):
    '''Fetches train data and returns the metadata
        have to updte response code , success and error_message
        on excpetion
        ** fetch already does raise_for_status() 
    '''
    output_path = (
        BRONZE_HTML_DIR
        /f"{date.today()}_{train_name}_{train_no}")
    
    response = fetch_html(session, url)
    save_html(output_path, response.get('html',{}))     
    return {
        "file_path": str(output_path),
        "response_status_code": response.get("status_code",None),
    }




