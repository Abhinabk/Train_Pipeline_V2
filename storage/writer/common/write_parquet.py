from datetime import date
from io import BytesIO

import pandas as pd

from config.settings import S3_BUCKET
from storage.object_store.s3 import save_parquet_s3


def write_parquet_to_s3(df:pd.DataFrame,file_name:str,parquet_name:str,
                        date:date,prefix:str,bucket:str=S3_BUCKET)->str:
    buffer = BytesIO()
    df.to_parquet(buffer,index=False)
    key = (f"{prefix}/{file_name}/"f"{date}/"f"{parquet_name}.parquet")
    return save_parquet_s3(bucket=bucket,file_name=key,content=buffer.getvalue())


    