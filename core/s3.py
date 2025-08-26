# core/s3.py
import os
import mimetypes
import boto3

AWS_REGION = os.getenv("AWS_REGION", "")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_PRESIGNED_EXPIRE_SECONDS = int(os.getenv("AWS_PRESIGNED_EXPIRE_SECONDS", "600"))
AWS_S3_AUDIO_PREFIX = os.getenv("AWS_S3_AUDIO_PREFIX", "").strip()

def _full_key(key: str) -> str:
    """환경변수에 prefix가 있으면 붙여준다 (예: 'audio/')."""
    if AWS_S3_AUDIO_PREFIX:
        return f"{AWS_S3_AUDIO_PREFIX.rstrip('/')}/{key.lstrip('/')}"
    return key.lstrip("/")

def _s3():
    return boto3.client(
        "s3",
        region_name=AWS_REGION or None,
        aws_access_key_id=AWS_ACCESS_KEY_ID or None,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY or None,
    )

def create_presigned_get_url(key: str, expires: int | None = None) -> str:
    """
    S3 객체에 대한 presigned GET URL 생성.
    """
    exp = int(expires or AWS_PRESIGNED_EXPIRE_SECONDS)
    return _s3().generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": AWS_S3_BUCKET, "Key": _full_key(key)},
        ExpiresIn=exp,
        HttpMethod="GET",
    )

def create_presigned_put_url(
    key: str,
    content_type: str | None = None,
    expires: int | None = None,
    acl: str | None = None,
) -> str:
    """
    S3 객체 업로드용 presigned PUT URL 생성.
    - content_type 미지정 시 파일 확장자로 추정, 그래도 없으면 'application/octet-stream'
    - 보통 프론트에서 fetch/axios로 PUT 업로드할 때 사용
    """
    exp = int(expires or AWS_PRESIGNED_EXPIRE_SECONDS)
    guess = None
    if not content_type:
        guess, _ = mimetypes.guess_type(key)
    ct = content_type or guess or "application/octet-stream"

    params = {
        "Bucket": AWS_S3_BUCKET,
        "Key": _full_key(key),
        "ContentType": ct,
    }
    # 필요 시 ACL을 private/public-read 등으로 지정
    if acl:
        params["ACL"] = acl

    return _s3().generate_presigned_url(
        ClientMethod="put_object",
        Params=params,
        ExpiresIn=exp,
        HttpMethod="PUT",
    )
