import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from pyathena import connect
from dotenv import load_dotenv

# 1. Carregar variáveis do .env
load_dotenv()

def sync_athena_to_supabase():
    # Credenciais Supabase
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # Montar a URL de conexão (SSL é obrigatório no Supabase)
    SUPABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"

    # Configurações AWS / Athena
    S3_BUCKET = os.getenv("S3_BUCKET")
    AWS_REGION = os.getenv("AWS_REGION")
    SCHEMA_NAME = "ecommerce_db"
    
    # URL Athena via SQLAlchemy (pyathena)
    ATHENA_URL = f"awsathena+rest://@athena.{AWS_REGION}.amazonaws.com:443/{SCHEMA_NAME}?s3_staging_dir=s3://{S3_BUCKET}/athena-results/"

    # Tabelas Gold para sincronizar
    tables = [
         "fct_vendas_performance",
         "fct_competitividade_precos",
         "fct_segmentacao_clientes",
         "fct_saude_portfolio"
     ]
    
    print("🚀 Iniciando a sincronização: AWS Athena -> Supabase Postgres")

    try:
        # Criar engines do SQLAlchemy
        # Usando NullPool para o Supabase para evitar conflitos com o Pooler de Transações
        engine_supabase = create_engine(SUPABASE_URL, poolclass=NullPool)
        engine_athena = create_engine(ATHENA_URL)

        for table in tables:
            print(f"📦 Processando tabela: {table}...")
            
            # Query simples
            query = f"SELECT * FROM {table}"
            
            # Ler dados do Athena
            df = pd.read_sql(query, engine_athena)

            # Escrever no Supabase (replace garante dados atualizados)
            df.to_sql(table, engine_supabase, if_exists='replace', index=False)

            print(f"✅ Tabela {table} sincronizada com {len(df)} registros.")

        print("\n✨ Sincronização concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante a sincronização: {e}")
        print("\n💡 Dica: Se o erro persistir, verifique se a senha no seu .env está correta.")

if __name__ == "__main__":
    sync_athena_to_supabase()

if __name__ == "__main__":
    sync_athena_to_supabase()
