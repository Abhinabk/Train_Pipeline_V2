import boto3 
from botocore.exceptions import ClientError, NoCredentialsError
from config.logger import bronze_logger

_client = None
def get_client():
    #without global python will just crete a 
    #local var call client and will need to crete a connection for each call
    #gloab is used to make it a single connection as for next call _client 
    # is not null is a connection to boto3.client("s3")
    global _client
    if _client is None:
        _client = boto3.client("s3")
    return _client

def put_object(bucket:str,key:str,content:str|bytes):
    client = get_client()
    try:
        client.put_object(
            Bucket = bucket,
            Key = key,#file name
            Body = content
        )
        return f"s3://{bucket}/{key}"
    except NoCredentialsError as err:
        bronze_logger.error(f"{err}")
        raise RuntimeError("AWS credentials not configured")
    except ClientError as e:
        bronze_logger.error(f"{e.response['Error']}")
        raise RuntimeError(f"S3 upload failed: {e.response['Error']['Code']}")

def save_html_s3(bucket:str,file_name:str,content:str)->str:
    return put_object(bucket,file_name,content)

def save_parquet_s3(bucket:str,file_name:str,content:bytes)->str:
    return put_object(bucket,file_name,content)
    