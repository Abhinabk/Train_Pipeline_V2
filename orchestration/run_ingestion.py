from ingestion.etrain.build_url import build_train_url
from ingestion.etrain.scraper import fetch_train_history
from storage.writer.write_bronze_metadata import insert_bronze_train_metadata
from config.logger import bronze_logger
import requests


def run_train_ingestion(session,con,train_no,train_name):
    url = build_train_url(train_no,train_name,time="1y") # type: ignore
    safe_train_name = train_name.strip().replace(" ", "-") # type: ignore
    #metadata template
    metadata = {
        "train_no":train_no,
        "train_name":safe_train_name,
        "source_url":url,
        "file_path":None,
        "response_status_code":None,
        "success":None,
        "error_message":None
    }
    try:
        result = fetch_train_history(url,session,train_no,safe_train_name,storage="s3")
        metadata.update(result)
        metadata["success"] = True
        bronze_logger.info(f"{metadata.get('train_name',None)}_{metadata.get('train_no',None)}\
                            ingested-> {result['file_path']}")

    except requests.exceptions.RequestException as err:
        metadata['success'] = False
        metadata['error_message'] = getattr(err.response,'reason', str(err))
        metadata['response_status_code'] = getattr(err.response,'status_code',None)
        bronze_logger.warning(f"{metadata.get('train_name',None)}_{metadata.get('train_no',None)} \
                {metadata.get('source_url',None)} {err}"
        )
    
    insert_bronze_train_metadata(con,metadata)
