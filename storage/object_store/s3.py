from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from config.logger import bronze_logger
from config.settings import S3_BUCKET, S3_PREFIX_BRONZE_TRAIN
from urllib.parse import urlparse

_client = None


def get_client():
    # without global python will just crete a
    # local var call client and will need to crete a connection for each call
    # gloab is used to make it a single connection as for next call _client
    # is not null is a connection to boto3.client("s3")
    global _client
    if _client is None:
        _client = boto3.client("s3")
    return _client


def put_object(bucket: str, key: str, content: str | bytes):
    client = get_client()
    try:
        client.put_object(
            Bucket=bucket,
            Key=key,  # file name
            Body=content,
        )
        return f"s3://{bucket}/{key}"

    except NoCredentialsError as err:
        bronze_logger.error(f"{err}")
        raise RuntimeError("AWS credentials not configured")
    except ClientError as e:
        bronze_logger.error(f"{e.response['Error']}")
        raise RuntimeError(f"S3 upload failed: {e.response['Error']['Code']}")


def list_keys(
    bucket: str, prefix_key: str, date: str | None = None, train_no: str | None = None
) -> list[str | None]:
    client = get_client()
    prefix_key = f"{prefix_key}/{date}" if date else prefix_key
    try:
        response = client.list_objects_v2(Bucket=bucket, Prefix=prefix_key)
        contents = response.get("Contents", "")
        keys = [i.get("Key", " ") for i in contents]
        if train_no:
            # s3://train-pipeline-v2/bronze/bronze_raw_train_html/2026-05-27/Kamrup-Express_15959.html
            return [k for k in keys if Path(k).stem.split("_")[-1] == train_no]
        return keys

    except NoCredentialsError as err:
        bronze_logger.error(f"{err}")
        raise RuntimeError("AWS credentials not configured")
    except ClientError as e:
        bronze_logger.error(f"{e.response['Error']}")
        raise RuntimeError(f"S3 upload failed: {e.response['Error']['Code']}")


def get_object(bucket: str, key: str) -> str:
    client = get_client()
    try:
        response = client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read().decode("utf-8")
    except NoCredentialsError as err:
        bronze_logger.error(f"{err}")
        raise RuntimeError("AWS credentials not configured")
    except ClientError as e:
        bronze_logger.error(f"{e.response['Error']}")
        raise RuntimeError(f"S3 failed: {e.response['Error']['Code']}")


def get_files(
    bucket=S3_BUCKET,
    prefix=S3_PREFIX_BRONZE_TRAIN,
    date: str | None = None,
    type: str = "html",
    train_no: str | None = None,
)->list[str]:
    """
    Provide the S3_BUCKET and S3_PREFIX and date for the folder and file type and train_no \n
    DEFAULTS TO S3_BUCKET,S3_PREFIX_BRONZE_TRAIN,all dates,'html',None
    so \n
    get_file() -> return all files in s3://train-pipeline-v2/bronze/bronze_raw_train_html \n
    get_file(date = '2026-05-28') -> return all files in s3://train-pipeline-v2/bronze/bronze_raw_train_html/2026-05-28 \n
    get_file(date = '2026-05') -> return all files in s3://train-pipeline-v2/bronze/bronze_raw_train_html/2026-05
    all files int that month
    get_file(date = '2026-05-28',train_no='15959') -> return single train file in s3://train-pipeline-v2/bronze/bronze_raw_train_html/2026-05-28/Kamrup-Express_15959.html

    """
    keys = list_keys(bucket, prefix, date,train_no)
    results = []
    for key in keys:
        if key and key.endswith(f".{type}"):
            results.append(get_object(bucket, key))
        else:
            bronze_logger.warning(f"Skipping {key}")
    return results


def get_object_from_uri(uri: str) -> str:
    parsed = urlparse(uri)

    bucket = parsed.netloc #jsut the bucket part
    key = parsed.path.lstrip("/")

    return get_object(bucket, key)

def save_html_s3(bucket: str, file_name: str, content: str) -> str:
    return put_object(bucket, file_name, content)


def save_parquet_s3(bucket: str, file_name: str, content: bytes) -> str:
    return put_object(bucket, file_name, content)


if __name__ == "__main__":
    files = get_files()
    for file in files:
        print(file)
