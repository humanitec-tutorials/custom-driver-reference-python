import boto3
from botocore.exceptions import ClientError


def create_bucket(access_key_id: str, secret_access_key: str, region: str, bucket_name: str):
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region
        )
        location = {'LocationConstraint': region}
        client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        raise ValueError(f"Failed creating s3 bucket {e.args}")
    return region


def delete_bucket(access_key_id: str, secret_access_key: str, region: str, bucket_name: str):
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region
        )
        client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        raise ValueError(f"Failed creating s3 bucket {e.args}")
    return region

