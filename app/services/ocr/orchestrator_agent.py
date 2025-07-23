from app.services.ocr.ocr_pdf_agent import process_pdf_with_gpt
from app.services.ocr.ocr_image_agent import process_image_with_gemini
import os
import asyncio
from dotenv import load_dotenv

async def ocr_orchestrator(file_path: str) -> str:
    print('file_path', file_path)
    ext = os.path.splitext(file_path)[1].lower()
    print('ext', ext)
    
    if ext == '.pdf':
        return await process_pdf_with_gpt(file_path)
    elif ext in ['.png', '.jpg', '.jpeg']:
        return await process_image_with_gemini(file_path)
    else:
        return "Unsupported file type"
