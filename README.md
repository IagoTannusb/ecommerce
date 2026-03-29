# 📊 E-commerce Analytics: Serverless Data Lakehouse

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![dbt Version](https://img.shields.io/badge/dbt-1.8%2B-orange)](https://www.getdbt.com/)
[![AWS Athena](https://img.shields.io/badge/AWS-Athena-232F3E?logo=amazonaws)](https://aws.amazon.com/athena/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?logo=supabase)](https://supabase.com/)

Um ecossistema completo de **Analytics Engineering** que transforma dados brutos de e-commerce em insights estratégicos, utilizando a **Arquitetura Medalhão** e o paradigma **Modern Data Stack (MDS)**.

---

## 🎯 1. Contexto de Negócio
Este projeto resolve a fragmentação de dados em uma operação de e-commerce em expansão. O objetivo é fornecer aos stakeholders (CFO, Head de Vendas, Marketing e Operações) uma visão única e confiável sobre:
*   **Performance Financeira:** Faturamento e Ticket Médio por canal e região.
*   **Inteligência Competitiva:** Gap de preço em relação aos concorrentes.
*   **CRM & Retenção:** Segmentação ABC e prevenção de Churn.
*   **Saúde de Portfólio:** Identificação de produtos sem giro (Zumbis).

---

## 🏗️ 2. Arquitetura do Sistema (ELT Paradigm)

O projeto utiliza uma arquitetura **Serverless** na AWS para processamento pesado e **Supabase** para entrega de baixa latência (Serving Layer).

```mermaid
graph LR
    A[Dados Brutos .csv] -->|Python + Parquet| B[S3 Bronze]
    B -->|AWS Glue| C[S3 Silver]
    C -->|dbt + Athena| D[S3 Gold]
    D -->|Python Sync| E[Supabase Postgres]
    E -->|Streamlit| F[Executive Dashboard]
```

### **As Camadas (Medallion Architecture):**
1.  **🥉 Bronze (Raw):** Dados originais em CSV convertidos para Parquet para otimização de custo e IO.
2.  **🥈 Silver (Cleansed):** Limpeza, tipagem forte e normalização via dbt.
3.  **🥇 Gold (Curated):** Tabelas de negócio (Data Marts) agregadas e prontas para BI.
4.  **🚀 Serving Layer:** Supabase atuando como cache de alta performance para o Dashboard.

---

## 🛠️ 3. Decisões de Engenharia (Deep Dive)

*   **Parquet vs CSV:** Redução de **~80%** no volume de dados lidos no Athena, minimizando custos de processamento.
*   **Connection Pooling (Supavisor):** Utilização do modo `Transaction` (porta 6543) para garantir conectividade IPv4 estável em qualquer rede.
*   **SQLAlchemy + NullPool:** Configuração personalizada para evitar conflitos de cache de conexão entre o script Python e o Pooler do Supabase.
*   **Idempotência:** O pipeline de sincronização (`athena_to_supabase.py`) utiliza a estratégia de `replace` para garantir que o Dashboard sempre reflita a versão mais recente da camada Gold.

---

## 🚀 4. Como Executar

### **Pré-requisitos**
*   Python 3.12+ (Recomendado utilizar `uv`)
*   Conta AWS (S3, Athena, Glue)
*   Projeto Supabase ativo

### **Passo 1: Instalação**
```bash
git clone https://github.com/seu-usuario/ecommerce-analytics.git
cd ecommerce-analytics
uv venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
uv pip install -r pyproject.toml
```

### **Passo 2: Configuração (.env)**
Crie um arquivo `.env` na raiz com as credenciais:
```env
# AWS
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
S3_BUCKET=...

# Supabase (Pooler Mode)
DB_USER=postgres.[PROJECT_ID]
DB_PASSWORD=...
DB_HOST=aws-0-sa-east-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
```

### **Passo 3: Execução do Pipeline (Orquestração)**
O projeto utiliza um script centralizador que executa todo o fluxo ELT (Ingestão -> Transformação -> Serving):

```bash
# Executa o pipeline completo (Upload S3 + dbt Run/Test + Sync Supabase)
uv run main.py
```

### **Passo 4: Visualização no Dashboard**
```bash
# Inicializa o Dashboard Executivo
uv run streamlit run src/app.py
```

---

## 📂 5. Anatomia do Projeto
```text
├── data/                       # Datasets originais (Parquet)
│   ├── clientes.parquet
│   ├── preco_competidores.parquet
│   ├── produtos.parquet
│   └── vendas.parquet
├── ecommerce_project/          # Core de Analytics Engineering (dbt)
│   ├── dbt_project.yml         # Configurações do projeto dbt
│   ├── models/
│   │   ├── sources.yml         # Definição das fontes de dados (S3/Athena)
│   │   ├── bronze/             # Camada Raw (Staging)
│   │   │   ├── stg_clientes.sql
│   │   │   ├── stg_vendas.sql
│   │   │   └── ...
│   │   ├── silver/             # Camada de Integração (Intermediate)
│   │   │   ├── int_vendas.sql
│   │   │   └── ...
│   │   └── gold/               # Camada de Negócio (Data Marts)
│   │       ├── schema.yml      # Testes e Documentação
│   │       ├── finance/        # fct_vendas_performance.sql
│   │       ├── marketing/      # fct_segmentacao_clientes.sql
│   │       ├── commercial/     # fct_competitividade_precos.sql
│   │       └── operations/     # fct_saude_portfolio.sql
│   └── tests/                  # Testes customizados
├── src/                        # Scripts de Infra e Aplicação
│   ├── app.py                  # Dashboard Executivo (Streamlit)
│   ├── athena_to_supabase.py   # Orquestrador de Sync (Athena -> Postgres)
│   ├── upload_to_s3.py         # Ingestão de dados local -> AWS S3
│   └── utils/                  # Funções auxiliares
├── GEMINI.md                   # Roadmap detalhado do projeto
├── PERGUNTAS_NEGOCIO.md        # Guia de KPIs e Regras de Negócio
├── Dockerfile                  # Containerização da aplicação
└── docker-compose.yml          # Orquestração local
```

---

## 📊 6. Dicionário de Dados

Abaixo, a descrição dos quatro datasets principais que alimentam o Data Lakehouse:

### **1. Clientes (`clientes.parquet`)**
*Base cadastral para análises geográficas e segmentação.*
- **`id_cliente`**: Identificador único (PK).
- **`nome_cliente`**: Nome completo para identificação.
- **`estado`**: UF de residência (Análise regional).
- **`pais`**: País de origem.
- **`data_cadastro`**: Data de entrada na plataforma.

### **2. Produtos (`produtos.parquet`)**
*Catálogo de SKUs e precificação interna.*
- **`id_produto`**: Código identificador do SKU (PK).
- **`nome_produto`**: Descrição comercial.
- **`categoria`**: Segmento de mercado (ex: Eletrônicos, Moda).
- **`marca`**: Fabricante ou marca própria.
- **`preco_atual`**: Preço de venda vigente.

### **3. Vendas (`vendas.parquet`)**
*Fatos transacionais da operação.*
- **`id_venda`**: ID único da transação (PK).
- **`data_venda`**: Timestamp da confirmação do pedido.
- **`id_cliente`**: FK para a tabela de clientes.
- **`id_produto`**: FK para a tabela de produtos.
- **`canal_venda`**: Origem (App, Site, Marketplace).
- **`quantidade`**: Volume de itens vendidos.
- **`preco_unitario`**: Valor do item no momento da venda.

### **4. Preço Competidores (`preco_competidores.parquet`)**
*Dados de inteligência competitiva (External Data).*
- **`id_produto`**: ID do produto monitorado.
- **`nome_concorrente`**: Nome do competidor (ex: Amazon, Magalu).
- **`preco_concorrente`**: Preço praticado pelo mercado.
- **`data_coleta`**: Timestamp da captura do dado.

---

## 📈 7. Inteligência de Negócio (Perguntas Respondidas)

O projeto foi desenhado para responder diretamente aos requisitos do perguntas_negocio.md, entregando insights acionáveis para diferentes áreas:

### **A. Performance Financeira (CFO)**
- **Qual a saúde do faturamento?** Monitoramento de Receita Total, Ticket Médio e Volume de Pedidos.
- **Onde estamos vendendo mais?** Quebra geográfica por UF para otimização logística.
- **Qual o canal mais eficiente?** Comparativo de performance entre App, Site e Marketplace.

### **B. Inteligência Comercial (Sales)**
- **Quão competitivos somos?** Cálculo do Gap de Preço percentual médio em relação à concorrência por categoria.
- **Elasticidade de Preço:** Identificação de SKUs onde o preço acima do mercado está impactando diretamente o volume de vendas.
- **Top 20 Monitoramento:** Relatório detalhado comparativo de preços para os produtos que mais geram receita.

### **C. Marketing & CRM (Marketing)**
- **Quem são os clientes VIP?** Segmentação ABC (Pareto) identificando os 20% de clientes que geram 80% do faturamento.
- **Risco de Churn:** Alerta de clientes sem compras há mais de 60 dias para campanhas de reativação.
- **Ciclo de Vida:** Análise do intervalo médio de recompra para predição de demanda futura.

### **D. Eficiência Operacional (Operations)**
- **Onde há capital parado?** Identificação de "Produtos Zumbis" (sem vendas há >180 dias) para estratégias de queima de estoque.
- **Risco de Concentração:** Análise da dependência do faturamento sobre o Top 10 SKUs do portfólio.

---
