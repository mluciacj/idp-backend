from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.document import Document
from app.services.storage.s3 import upload_to_s3
from app.services.ocr.orchestrator_agent import ocr_orchestrator
import uuid
import os
import asyncio
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def process_and_save_document(file: UploadFile, client_id: str, country: str, db: Session, semaphore: asyncio.Semaphore):
    async with semaphore:
        file_extension = os.path.splitext(file.filename)[-1].lower()
        document_id = str(uuid.uuid4())
        filename = f"{client_id}/{document_id}{file_extension}"

        file_content = await file.read()
        s3_url = save_file_to_s3(file_content, filename)

        # Cria objeto no banco
        doc = Document(
            id=document_id,
            client_id=client_id,
            country=country,
            s3_url=s3_url,
            created_at=datetime.utcnow()
        )
        db.add(doc)
        db.commit()

        try:
            ocr_result = await ocr_orchestrator(s3_url, country)
            doc.ocr_result = ocr_result
            db.commit()
            return {"document_id": document_id, "status": "success"}
        except Exception as e:
            doc.ocr_result = {"error": str(e)}
            db.commit()
            return {"document_id": document_id, "status": "error", "error": str(e)}

@router.post("/upload", tags=["Upload"])
async def upload_documents(
    files: list[UploadFile] = File(...),
    client_id: str = Form(...),
    country: str = Form(...),
    db: Session = Depends(get_db)
):

    semaphore = asyncio.Semaphore(5)  # Máximo de 5 OCRs em paralelo

    tasks = [
        process_and_save_document(file, client_id, country, db, semaphore)
        for file in files
    ]
    results = await asyncio.gather(*tasks)
    return {"status": "completed", "results": results}

"""
@router.post("/documents/upload", tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
    country: str = Form(...),
    client_id: str = Form(...),
    source: str = Form("web"),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("application/pdf"):
        return {"status": "error", "detail": "Only PDF files are allowed."}
        
    try:
        s3_url = upload_to_s3(file, client_id)
    except Exception as e:
        return {"status": "error", "detail": f"Error uploading file to S3: {str(e)}"}
    try:
        doc = Document(
            client_id=client_id,
            document_type=file.content_type,
            country=country,
            language = "pt-BR",
            source=source,
            s3_url=s3_url
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
    except Exception as e:
        return {"status": "error", "detail": f"Error saving data into postgress: {str(e)}"}
  
    try:
        print('s3_url', s3_url)
        ocr_result = await ocr_orchestrator(s3_url, country)
    except Exception as e:
        return {"status": "error", "detail": f"Error processing OCR: {str(e)}"}
    try:
        doc.ocr_result = ocr_result
        db.commit()
        db.refresh(doc)
    except Exception as e:
        return {"status": "error", "detail": f"Error saving OCR result into database: {str(e)}"}
   
    return {"status": "success", "document_id": str(doc.id), "s3_url": s3_url, "ocr_result": ocr_result}
"""