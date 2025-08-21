import os, boto3
from botocore.client import Config
def get_s3_client():
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        config=Config(signature_version="s3v4"),
    )
def create_presigned_put_url(key: str, content_type: str, expires: int):
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": os.getenv("AWS_S3_BUCKET"), "Key": key, "ContentType": content_type, "ACL": "private"},
        ExpiresIn=expires,
        HttpMethod="PUT",
    )
