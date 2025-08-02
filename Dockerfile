# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Instala Rust e outras dependências do sistema necessárias para o maturin e wheel
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libssl-dev \
    pkg-config \
    python3-dev \
    rustc \
    cargo \
    && apt-get clean

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o requirements.txt e instala as dependências Python
COPY requirements.txt .

# Faz upgrade do pip e instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o restante do projeto para o container
COPY . .

# Define o comando padrão para iniciar o app
# Ajuste esse comando conforme o seu arquivo principal (main.py, app.py, etc)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

