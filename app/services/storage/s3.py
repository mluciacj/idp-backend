import boto3
import uuid
from botocore.exceptions import NoCredentialsError
from app.core.config import settings

s3 = boto3.client(
    's3',
    endpoint_url=settings.S3_ENDPOINT,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION
)

def upload_to_s3(file, client_id: str) -> str:
    filename = f"{client_id}/{uuid.uuid4()}.pdf"
    try:
        s3.upload_fileobj(file.file, settings.S3_BUCKET_NAME, filename)
        return f"s3://{settings.S3_BUCKET_NAME}/{filename}"
    except NoCredentialsError:
        raise RuntimeError("S3 credentials not found.")
