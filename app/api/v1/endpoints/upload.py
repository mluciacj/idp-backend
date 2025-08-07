from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.data_models.document import Document
from app.services.ocr.orchestrator_agent import ocr_orchestrator
from app.services.storage.s3 import upload_to_s3
import asyncio
import uuid

router = APIRouter()

MAX_CONCURRENT_TASKS = 5  # semaphore limit


async def process_document(file: UploadFile, client_id: str, country: str, source: str, db: Session, semaphore: asyncio.Semaphore):
    if not file.content_type.startswith("application/pdf"):
        return {"status": "error", "detail": "Only PDF files are allowed.", "filename": file.filename}

    async with semaphore:
        try:
            s3_url = upload_to_s3(file, client_id)
        except Exception as e:
            return {"status": "error", "detail": f"Error uploading to S3: {str(e)}", "filename": file.filename}

        try:
            doc = Document(
                id=str(uuid.uuid4()),
                client_id=client_id,
                document_type=file.content_type,
                country=country,
                language="pt-BR",
                source=source,
                s3_url=s3_url
            )
            db.add(doc)
            db.commit()
            db.refresh(doc)
        except Exception as e:
            return {"status": "error", "detail": f"Error saving document to Postgres: {str(e)}", "filename": file.filename}

        try:
            ocr_result = await ocr_orchestrator(s3_url, country)
        except Exception as e:
            return {"status": "error", "detail": f"OCR error: {str(e)}", "filename": file.filename}

        try:
            doc.ocr_result = ocr_result
            db.commit()
            db.refresh(doc)
        except Exception as e:
            return {"status": "error", "detail": f"Failed saving OCR result: {str(e)}", "filename": file.filename}

        return {
            "status": "success",
            "document_id": str(doc.id),
            "s3_url": s3_url,
            "ocr_result": ocr_result,
            "filename": file.filename
        }


@router.post("/documents/upload", tags=["Documents"])
async def upload_documents(
    files: list[UploadFile] = File(...),
    country: str = Form(...),
    client_id: str = Form(...),
    source: str = Form("web"),
    db: Session = Depends(get_db)
):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    tasks = [process_document(file, client_id, country, source, db, semaphore) for file in files]
    results = await asyncio.gather(*tasks)
    return {"status": "completed", "results": results}
