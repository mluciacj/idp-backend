import google.generativeai as genai
from PIL import Image
import io
import base64
import os

GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
genai.configure(api_key=GOOGLE_GENAI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")

async def process_image_with_gemini(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))

    # Gemini exige imagens como base64 ou objetos PIL
    response = model.generate_content(
        [
            "Extraia o texto contido nesta imagem de documento de forma estruturada (OCR):",
            image
        ],
        stream=False
    )
    return response.text
