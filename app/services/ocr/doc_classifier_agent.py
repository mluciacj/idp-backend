import json
from app.core.config import settings
import google.generativeai as genai
from openai import AsyncOpenAI


client1 = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def classify_document_text(text: str) -> str:
    prompt = f"""
    A partir do conteúdo abaixo, classifique o tipo de documento.
    Categorias possíveis:
    - Nota Fiscal Eletrônica (NF-e)
    - Nota Fiscal de Serviço Eletrônica (NFS-e)
    - Nota Fiscal do Consumidor Eletrônica (NFC-e)
    - Orçamento / Proposta Comercial
    - Boleto Bancário
    - Pix

    Responda com apenas uma dessas categorias.

    Conteúdo:
    {text}

    Retorne apenas a categoria, sem nenhum outro texto.
    """
    response = await client1.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
