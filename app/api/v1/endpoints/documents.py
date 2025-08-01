from fastapi import APIRouter, HTTPException, Request, Query, Body, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO, BytesIO
import pandas as pd
from datetime import datetime
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.document import Document
from app.api.v1.endpoints.utils import export_documents_data
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/documents", tags=["Documents"])
def list_documents(
    client_id: str = Query(...),
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Document).filter(Document.client_id == client_id)

    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Document.created_at >= start)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Document.created_at <= end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")
    
    docs = query.order_by(Document.created_at.desc()).all()

    return [
        {
            "id": doc.id,
            "created_at": doc.created_at,
            "s3_url": doc.s3_url,
            "ocr_result": doc.ocr_result,
            "country": doc.country
        }
        for doc in docs
    ]
"""
@router.get("/documents/batch", tags=["Documents"])
def get_documents_batch(
    document_ids: str = Query(..., description="Comma-separated list of document IDs"),
    db: Session = next(get_db())
):
    ids = [doc_id.strip() for doc_id in document_ids.split(",") if doc_id.strip()]
    if not ids:
        raise HTTPException(status_code=400, detail="No valid document IDs provided.")

    docs = db.query(Document).filter(Document.id.in_(ids)).all()

    if not docs:
        raise HTTPException(status_code=404, detail="No documents found for the given IDs.")

    return [
        {
            "id": doc.id,
            "client_id": doc.client_id,
            "country": doc.country,
            "s3_url": doc.s3_url,
            "ocr_result": doc.ocr_result
        }
        for doc in docs
    ]

class DocumentBatchRequest(BaseModel):
    document_ids: list[str]

@router.post("/documents/batch", tags=["Documents"])
def get_documents_batch_post(
    request: DocumentBatchRequest,
    db: Session = next(get_db())
):
    ids = request.document_ids
    if not ids:
        raise HTTPException(status_code=400, detail="No document IDs provided.")

    docs = db.query(Document).filter(Document.id.in_(ids)).all()

    if not docs:
        raise HTTPException(status_code=404, detail="No documents found.")

    return [
        {
            "id": doc.id,
            "client_id": doc.client_id,
            "country": doc.country,
            "s3_url": doc.s3_url,
            "ocr_result": doc.ocr_result
        }
        for doc in docs
    ]

@router.get("/documents/{document_id}/download", tags=["Documents"])
def download_document(document_id: str, format: str = "json", db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not doc.ocr_result:
        raise HTTPException(status_code=400, detail="OCR not processed yet")

    data = doc.ocr_result  # deve ser dict

    if format == "json":
        return JSONResponse(content=data)

    df = pd.json_normalize(data)

    if format == "csv":
        stream = StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)
        return StreamingResponse(stream, media_type="text/csv", headers={
            "Content-Disposition": f"attachment; filename=document_{doc.id}.csv"
        })

    elif format == "excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={
            "Content-Disposition": f"attachment; filename=document_{doc.id}.xlsx"
        })

    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use json, csv, or excel.")

"""

@router.post("/documents/download/by-ids", tags=["Documents"])
def download_documents_by_ids(
    request: Request,
    format: str = "json",
    db: Session = Depends(get_db)
):
    body = request.json()  # expects: {"document_ids": ["id1", "id2", ...]}
    document_ids = body.get("document_ids", [])
    
    if not document_ids:
        raise HTTPException(status_code=400, detail="No document IDs provided.")

    docs = db.query(Document).filter(Document.id.in_(document_ids)).all()

    if not docs:
        raise HTTPException(status_code=404, detail="No documents found.")

    results = [doc.ocr_result for doc in docs if doc.ocr_result]

    return export_documents_data(results, format)

@router.get("/documents/download/by-client", tags=["Documents"])
def download_documents_by_client(
    client_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    format: str = "json",
    db: Session = Depends(get_db)
):
    query = db.query(Document).filter(Document.client_id == client_id)

    if start_date:
        query = query.filter(Document.created_at >= start_date)
    if end_date:
        query = query.filter(Document.created_at <= end_date)

    docs = query.all()
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found.")

    results = [doc.ocr_result for doc in docs if doc.ocr_result]

    return export_documents_data(results, format)

