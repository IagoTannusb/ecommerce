# 📊 E-commerce Analytics Project: Business Requirements Document (BRD)

**Stakeholders:** Head of Sales, CFO, Marketing Manager.
**Data Source:** Legacy Sales System & Competitor Scraping.
**Status:** In Preparation (Strategy Phase).

---

## 1. Contexto do Projeto
A empresa está expandindo sua operação digital e precisa de uma visão clara sobre a saúde financeira e o posicionamento de mercado. Atualmente, os dados estão fragmentados e não permitem uma análise rápida de rentabilidade e competitividade.

## 2. Objetivos Estratégicos (Solicitações dos Stakeholders)

### 📈 Módulo A: Visibilidade de Receita & Performance (CFO)
*O foco é entender o "Top-Line" e a eficiência operacional.*
- **KPIs Financeiros:** Necessitamos do Faturamento Total, Ticket Médio e Volume de Pedidos por Canal (E-commerce vs Outros).
- **Análise Geográfica:** Quais estados (UF) estão gerando maior receita? Precisamos disso para otimizar a logística.
- **Performance de Marca:** Quais marcas estão tracionando mais volume?

### 🎯 Módulo B: Inteligência de Preços & Competitividade (Head of Sales)
*A área comercial precisa reagir às mudanças do mercado.*
- **Gap de Preço:** Qual a nossa diferença percentual média em relação aos principais concorrentes por categoria?
- **Elasticidade Simples:** Identificar se produtos onde somos mais caros que a média do mercado apresentam queda significativa no volume de vendas.
- **Monitoramento de SKU:** Relatório comparativo (Nós vs Mercado) para os 20 produtos de maior faturamento.

### 👥 Módulo C: CRM & Comportamento do Cliente (Marketing)
*O objetivo é aumentar o LTV (Lifetime Value) e a retenção.*
- **Segmentação ABC:** Quem são os clientes que representam os top 20% do faturamento? (Princípio de Pareto).
- **Análise de Recorrência:** Qual o intervalo médio de recompra (Time Between Purchases)?
- **Churn Preventivo:** Identificar clientes que não compram há mais de 60 dias (atrito).

### 📦 Módulo D: Saúde de Portfólio e Inventário (Operações)
- **Produtos "Zumbis":** Identificar SKUs sem movimentação nos últimos 180 dias para ações de queima de estoque.
- **Concentração de Receita:** Qual a dependência do faturamento sobre o Top 10 produtos?

---

## 3. Entregáveis Esperados (The Big Picture)

1. **Camada de Processamento (Engenharia):** Transformação dos dados brutos em um modelo colunar (Parquet) otimizado para custo e performance na AWS.
2. **Data Warehouse (Gold Layer):** Tabelas consolidadas no Supabase prontas para consumo.
3. **Dashboard Executivo:** Interface interativa (Streamlit) consolidando os KPIs de todos os módulos acima.
4. **Relatório de Insights:** Uma View SQL consolidada que classifique cada produto como: *Abaixo da Média, Na Média ou Acima da Média* da concorrência.
