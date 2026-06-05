from datetime import date
import io

import pandas as pd

from config.settings import S3_BUCKET
from storage.object_store.s3 import save_csv_s3


def write_csv_to_s3(df:pd.DataFrame,file_name:str,csv_name:str,
                        date:date,prefix:str,bucket:str=S3_BUCKET)->str:
    buffer = io.StringIO()
    df.to_csv(buffer,index=False)
    key = (f"{prefix}/{file_name}/"f"{date}/"f"{csv_name}.csv")
    return save_csv_s3(bucket=bucket,file_name=key,content=buffer.getvalue())