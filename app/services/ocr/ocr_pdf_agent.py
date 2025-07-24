from openai import AsyncOpenAI
from io import BytesIO
import boto3
import fitz  # PyMuPDF
import os
from app.core.config import settings
from app.services.ocr.utils import download_object_from_s3, read_text_from_pdfobject
from dotenv import load_dotenv
import json
import ast

load_dotenv()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def extract_fields_from_pdf(text: str, country: str, doc_class: str) -> str:
    if country == "Brazil":
        if doc_class == "Nota Fiscal Eletrônica (NF-e)":
            fields_data = json.load(open('app/models/documents_models/Brazil/nfe.json'))
        elif doc_class == "Nota Fiscal de Serviço Eletrônica (NFS-e)":
            fields_data = json.load(open('app/models/documents_models/Brazil/nfse.json'))
        elif doc_class == "Nota Fiscal do Consumidor Eletrônica (NFC-e)":
            fields_data = json.load(open('app/services/models/document_models/Brazil/nfce.json'))
        elif doc_class == "Orçamento / Proposta Comercial":
            fields_data = json.load(open('app/models/documents_models/Brazil/proposta_comercial.json'))
        elif doc_class == "Boleto Bancário":
            fields_data = json.load(open('app/models/documents_models/Brazil/boleto_bancario.json'))
        elif doc_class == "Pix":
            fields_data = json.load(open('app/models/documents_models/Brazil/pix.json'))
        else:
            raise ValueError(f"Documento não suportado: {doc_class}")

    prompt = f"""Voce é um especialista em estrair dados de {doc_class}. 
                         Os campos a serem extraidos são: {fields_data} . Nesse json as chaves são os campos do tipo de documento {doc_class}, para cada campo temos:
                         - descricao: descrição do campo
                         - caracteristicas: caracteristicas do campo
                         - localizacao_tradicional: localizacao tradicional do campo dentro do documento

                         De acordo com a descrição, características e localização, localize todos esses campos no documento {text} e extraia os valores.
                         
                         Retorne um json com todos os campos extraidos e seus respectivos valores achados no documento.
                         Não retorne nenhum outro texto além do json.

                """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return ast.literal_eval(response.choices[0].message.content.strip().replace('```json', '').replace('```', ''))
