# 1. Imagem Base leve e estável
FROM python:3.12-slim

# 2. Configurações de ambiente para evitar arquivos .pyc e garantir logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Definir diretório de trabalho dentro do container
WORKDIR /app

# 4. Instalar dependências de sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar apenas o arquivo de requisitos primeiro (otimização de cache do Docker)
COPY pyproject.toml .

# 6. Instalar dependências via pip (Como estamos no Docker, o pip é suficiente e simples)
RUN pip install --no-cache-dir streamlit pandas plotly sqlalchemy psycopg2-binary python-dotenv

# 7. Copiar o restante do código do projeto
COPY . .

# 8. Expor a porta padrão do Streamlit
EXPOSE 8501

# 9. Comando para rodar a aplicação
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
