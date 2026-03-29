# 📊 Roadmap: E-commerce Serverless Data Lakehouse

Este documento é o guia definitivo para a implementação, manutenção e evolução da infraestrutura de Analytics do E-commerce, utilizando **AWS**, **dbt**, **Supabase** e **Streamlit**.

---

## 🎯 Objetivo & Visão Geral
Demonstrar competência em **Data Engineering**, **Cloud (AWS)** e **Analytics Engineering (dbt)**, utilizando o paradigma **ELT** (Extract, Load, Transform) e a **Arquitetura Medalhão** segmentada em **Data Marts**.

---

## 🏗️ Arquitetura Técnica (Paradigma ELT)

### 🥉 Camada Bronze (Raw)
- **Local:** Dados originais em CSV.
- **S3:** Armazenamento fiel ao original em `s3://ecommerce-datalake-26/bronze/`.
- **Objetivo:** Histórico e Auditoria.

### 🥈 Camada Silver (Cleansed & Modeled)
- **Local:** Conversão de CSV para **Parquet** (Otimização colunar).
- **S3:** Armazenamento otimizado em `s3://ecommerce-datalake-26/silver/`.
- **dbt:** Limpeza, tipagem (Cast) e criação de tabelas de interface (`stg_`) e intermediárias (`int_`).

### 🥇 Camada Gold (Curated & Data Marts)
- **Tecnologia:** dbt + AWS Athena.
- **Estrutura:** Tabelas agregadas e prontas para consumo de BI.

### 🚀 Serving Layer (Data Delivery)
- **Tecnologia:** Supabase (PostgreSQL).
- **Estratégia:** **Connection Pooler (Transaction Mode)** via porta 6543 para suporte total a redes IPv4.
- **Objetivo:** Oferecer latência de milissegundos para o Dashboard final, isolando o custo de processamento do Athena da experiência de navegação do usuário.

---

## 💰 FinOps & Segurança de Custos (Configurações Ativas)
1. **AWS Budgets:** Alerta configurado para **$0.01** (Gasto Zero).
2. **Athena Workgroup:** Configurar `analytics-safe` com limite de 50MB por query.
3. **IAM Roles:** Utilização da `LabGlueServiceRole` com permissões de privilégio mínimo.
4. **Data Integrity:** Testes dbt (`not_null`, `unique`) aplicados na camada Gold para evitar sync de dados corrompidos.

---

## 🚀 Guia de Execução (Passo a Passo)

### 1. Setup do Ambiente Local
- [x] Configurar `.env` (AWS, Supabase e Credenciais Athena).
- [x] Instalar dependências via `uv`.

### 2. Orquestração do Pipeline (Full Stack)
Para simplificar a execução, o arquivo `main.py` centraliza todas as etapas do pipeline:
- [x] **Execução Unificada:** `uv run main.py`.
    - **Passo 2.1 (Ingestão):** Executa `src/upload_to_s3.py` (Local Parquet -> S3 Bronze).
    - **Passo 2.2 (Transformação):** Executa `dbt run` e `dbt test` (Athena/Presto SQL).
    - **Passo 2.3 (Serving):** Executa `src/athena_to_supabase.py` (Sync Athena -> Postgres).

### 3. Data Catalog (AWS Glue)
- [x] Executar crawler para mapear esquemas e criar metadados no banco `raw` (Manual via Console AWS ou CLI).

### 4. Dashboard (Streamlit & Umbrel)
- [x] **Desenvolvimento:** Criar `src/app.py` respondendo a 100% do `PERGUNTAS_NEGOCIO.md`.
- [x] **Execução Local:** `uv run streamlit run src/app.py`.
- [ ] **Deployment:** Dockerizar a aplicação e subir no Umbrel via Docker Compose.


---

## 💎 Detalhamento da Camada Gold (Business Intelligence)

### 📈 Módulo A: Finance (`fct_vendas_performance`)
*Foco: Receita e Eficiência Geográfica.*
- **KPIs:** Faturamento Total, Ticket Médio por Marca e Canal.

### 🎯 Módulo B: Commercial (`fct_competitividade_precos`)
*Foco: Inteligência Competitiva e Elasticidade.*
- **KPIs:** Gap de Preço por Categoria e Relação Preço vs Volume Vendido.

### 👥 Módulo C: Marketing (`fct_segmentacao_clientes`)
*Foco: CRM e Retenção.*
- **KPIs:** Classificação ABC (Pareto) e Churn Preventivo (>60 dias).

### 📦 Módulo D: Operations (`fct_saude_portfolio`)
*Foco: Gestão de Inventário e Concentração.*
- **KPIs:** Produtos Zumbis (>180 dias) e Concentração de Receita nos Top 10 SKUs.

---

## 🛠️ Padrões de Engenharia Adotados
1. **SQLAlchemy & NullPool:** Robustez na conexão com poolers de transação.
2. **Streamlit Tabs & Cache:** Experiência de usuário fluida com `@st.cache_data`.
3. **Plotly Express:** Visualizações interativas e responsivas.
4. **Sintaxe Athena/Presto:** Uso de `date_diff` e `percent_rank` para cálculos complexos.
