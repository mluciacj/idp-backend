import sys
import os
from sqlalchemy import text
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.database import engine


def add_column_ocr_result():
    with engine.connect() as connection:
        print("Adicionando coluna 'ocr_result' na tabela 'documents' (se ainda não existir)...")
        connection.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS ocr_result JSONB;"))
        connection.commit()
        print("Coluna adicionada com sucesso.")

if __name__ == "__main__":
    add_column_ocr_result()