from app.services.ocr.ocr_pdf_agent import extract_fields_from_pdf
from app.services.ocr.doc_classifier_agent import classify_document_text
from app.services.ocr.ocr_image_agent import process_image_with_gemini
from app.services.ocr.utils import download_object_from_s3, read_text_from_pdfobject
import os
import asyncio
from dotenv import load_dotenv

async def ocr_orchestrator(file_path: str, country: str) -> str:
    print('file_path', file_path)
    ext = os.path.splitext(file_path)[1].lower()
    print('ext', ext)
    
    if ext == '.pdf':
        try:
            pdf_bytes = download_object_from_s3(file_path)
            text = read_text_from_pdfobject(pdf_bytes)
        except Exception as e:
            return f"Erro ao Extrair Texto do PDF: {str(e)}"
        try:
            classification = await classify_document_text(text)
            print('classification', classification)
        except Exception as e:
            return f"Erro ao Classificar Documento: {str(e)}"

        try:
            fields = await extract_fields_from_pdf(text, country, classification)
        except Exception as e:
            return f"Erro ao Extrair Campos do PDF: {str(e)}"
        
        return {'document_classification': classification, 'fields_extracted': fields}

    elif ext in ['.png', '.jpg', '.jpeg']:
        return await process_image_with_gemini(file_path)
    else:
        return "Unsupported file type"
