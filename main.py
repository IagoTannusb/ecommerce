import subprocess, sys
from src.upload_to_s3 import upload_parquet_to_s3
from src.athena_to_supabase import sync_athena_to_supabase

def run_dbt(cmd):
    """Executa dbt no diretório correto."""
    print(f"🚀 dbt {cmd}...")
    # Executa via uv conforme definido no roadmap do projeto
    subprocess.run(["uv", "run", "dbt", cmd], cwd="ecommerce_project", check=True)

def main():
    try:
        # 1. Ingestão: Local Parquet -> AWS S3 Bronze
        print("--- 1. UPLOAD S3 (Bronze) ---")
        upload_parquet_to_s3()
        
        # 2. Transformação & Qualidade: dbt Core + AWS Athena
        print("\n--- 2. TRANSFORMAÇÃO & TESTES (dbt) ---")
        run_dbt("run")
        run_dbt("test")
        
        # 3. Serving: AWS Athena -> Supabase Postgres
        print("\n--- 3. SYNC SUPABASE (Gold) ---")
        sync_athena_to_supabase()
        
        print("\n✨ Pipeline executada com sucesso!")
    except Exception as e:
        print(f"\n❌ Falha na Pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
