from io import BytesIO
import boto3
import fitz  # PyMuPDF
from app.core.config import settings

s3 = boto3.client("s3",
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION)

def download_object_from_s3(s3_path: str) -> bytes:
    if not s3_path.startswith("s3://"):
        raise ValueError("Invalid S3 path")

    bucket_key = s3_path.replace("s3://", "")
    bucket, key = bucket_key.split("/", 1)

    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()

def read_text_from_pdfobject(object_) -> str:
    pdf_doc = fitz.open("pdf", object_)
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    
    return text
