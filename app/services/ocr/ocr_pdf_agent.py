from openai import AsyncOpenAI
from io import BytesIO
import boto3
import fitz  # PyMuPDF
import os
from app.core.config import settings
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

s3 = boto3.client("s3",
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION)

def download_pdf_from_s3(s3_path: str) -> bytes:
    if not s3_path.startswith("s3://"):
        raise ValueError("Invalid S3 path")

    bucket_key = s3_path.replace("s3://", "")
    bucket, key = bucket_key.split("/", 1)

    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


async def process_pdf_with_gpt(file_path: str) -> str:
    print('file_path in ocr_pdf_agent: ', file_path)
    try:
        if file_path.startswith("s3://"):
            pdf_bytes = download_pdf_from_s3(file_path)
            doc = fitz.open("pdf", pdf_bytes)
        else:
            doc = fitz.open(file_path)

        text = ""
        for page in doc:
            text += page.get_text()

    except Exception as e:
        return f"Erro ao processar PDF: {str(e)}"

    prompt = f"Extraia e organize o texto do seguinte documento:\n\n{text}"

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
