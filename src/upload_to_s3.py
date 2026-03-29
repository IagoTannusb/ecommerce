import os
import boto3 
from dotenv import load_dotenv

load_dotenv()

def upload_parquet_to_s3():
    bucket_name = "ecommerce-datalake-26"
    region = os.getenv("AWS_REGION","us-east-1")

    s3_client = boto3.client( 
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region
    )

    # mapeamento: {"arquivo_local": "caminho_no_s3"}
    tables_to_upload = {
        "data/clientes.parquet": "database/clientes/clientes.parquet",
        "data/vendas.parquet": "database/vendas/vendas.parquet",
        "data/produtos.parquet": "database/produtos/produtos.parquet",
        "data/preco_competidores.parquet": "database/preco_competidores/preco_competidores.parquet"
    }

    print(f"Iniciando upload para o bucket: {bucket_name}\n")

    for local_path, s3_path in tables_to_upload.items():
        if os.path.exists(local_path):
            try:
                print(f"📤 Enviando {local_path} -> {s3_path}...")
                s3_client.upload_file(local_path, bucket_name, s3_path)
                print(f"✅ Sucesso!")
            except Exception as e:
                print(f"❌ Erro ao enviar {local_path}: {e}")
        else:
            print(f"⚠️ Arquivo local não encontrado: {local_path}")
    
    print("\n🏁 Processo de upload concluído!")

if __name__ == "__main__":
    upload_parquet_to_s3()