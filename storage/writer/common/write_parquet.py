from datetime import date
from io import BytesIO

import pandas as pd

from config.settings import S3_BUCKET, S3_PREFIX_SILVER_TRAIN
from storage.object_store.s3 import save_parquet_s3


def write_parquet_to_s3(df:pd.DataFrame,file_name:str,
                        date:date,bucket:str=S3_BUCKET,
                        prefix:str=S3_PREFIX_SILVER_TRAIN)->str:
    buffer = BytesIO()
    df.to_parquet(buffer,index=False)
    key = (
    f"{prefix}/{file_name}/"
    f"{date}/"
    f"{file_name}.parquet"
    )
    return save_parquet_s3(bucket=bucket,file_name=key,content=buffer.getvalue())


    