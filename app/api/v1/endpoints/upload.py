from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.document import Document
from app.services.storage.s3 import upload_to_s3

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

    return {"status": "success", "document_id": str(doc.id), "s3_url": s3_url}
