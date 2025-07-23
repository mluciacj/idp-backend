from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.document import Document
from app.services.storage.s3 import upload_to_s3
from app.services.ocr.orchestrator_agent import ocr_orchestrator

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/documents/upload", tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    country: str = Form(...),
    language: str = Form(None),
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
            document_type=document_type,
            country=country,
            language=language,
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
        ocr_result = await ocr_orchestrator(s3_url)
    except Exception as e:
        return {"status": "error", "detail": f"Error processing OCR: {str(e)}"}
   
    return {"status": "success", "document_id": str(doc.id), "s3_url": s3_url, "ocr_result": ocr_result}
