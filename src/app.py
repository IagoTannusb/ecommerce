import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import plotly.express as px

# 1. Configurações Iniciais e Estilo
st.set_page_config(page_title="E-commerce Analytics - Umbrel", layout="wide")
load_dotenv()

# 2. Conexão com Supabase (Postgres)
@st.cache_resource
def get_connection():
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    # URL do Pooler conforme configurado no .env
    conn_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
    return create_engine(conn_url)

engine = get_connection()

# 3. Funções de Carga de Dados
@st.cache_data
def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# 4. Título Principal
st.title("📊 E-commerce Executive Dashboard")
st.markdown("---")

# 5. Sidebar para Navegação (As 4 Abas do BRD)
tabs = st.tabs(["💰 Financeiro (CFO)", "🎯 Comercial (Vendas)", "👥 Marketing (CRM)", "📦 Operações"])

# --- ABA FINANCEIRA ---
with tabs[0]:
    st.header("📈 Performance de Receita e Operacional")
    df_finance = load_data("fct_vendas_performance")
    
    # KPIs de Topo
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_revenue = df_finance['receita_total'].sum()
        st.metric("Faturamento Total", f"R$ {total_revenue:,.2f}")
    with col2:
        total_orders = df_finance['id_venda'].nunique()
        st.metric("Volume de Pedidos", f"{total_orders:,}")
    with col3:
        avg_ticket = total_revenue / total_orders if total_orders > 0 else 0
        st.metric("Ticket Médio", f"R$ {avg_ticket:,.2f}")
    with col4:
        # Pergunta: Volume/Faturamento por Canal
        top_canal = df_finance['canal_venda'].mode()[0]
        st.metric("Canal Principal", top_canal)
    
    st.markdown("---")
    
    # Respostas de Negócio (Geografia e Marca)
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Receita por UF (Logística)")
        uf_rev = df_finance.groupby('uf_cliente')['receita_total'].sum().reset_index().sort_values('receita_total', ascending=False)
        fig_uf = px.bar(uf_rev, x='uf_cliente', y='receita_total', color='receita_total', labels={'uf_cliente': 'Estado', 'receita_total': 'Receita (R$)'})
        st.plotly_chart(fig_uf, width='stretch')
        
    with col_right:
        st.subheader("Faturamento por Canal")
        canal_rev = df_finance.groupby('canal_venda')['receita_total'].sum().reset_index()
        fig_canal = px.pie(canal_rev, values='receita_total', names='canal_venda', hole=0.4)
        st.plotly_chart(fig_canal, width='stretch')
    
    st.subheader("Performance por Marca")
    brand_rev = df_finance.groupby('marca_produto')['receita_total'].sum().reset_index().sort_values('receita_total', ascending=False)
    fig_brand = px.bar(brand_rev, x='marca_produto', y='receita_total', color='marca_produto')
    st.plotly_chart(fig_brand, width='stretch')

# --- ABA COMERCIAL ---
with tabs[1]:
    st.header("🎯 Inteligência Competitiva e Gap de Preços")
    df_comm = load_data("fct_competitividade_precos")
    
    # Tratamento de NaNs para evitar erro no Plotly (Size property)
    df_comm['volume_vendas_total'] = df_comm['volume_vendas_total'].fillna(0)
    df_comm['receita_vendas_total'] = df_comm['receita_vendas_total'].fillna(0)
    
    # KPI de Gap Médio
    avg_gap = df_comm['percentual_gap_preco'].mean()
    st.metric("Gap Médio vs Mercado (%)", f"{avg_gap:.2f}%", delta=f"{avg_gap:.2f}%", delta_color="inverse")
    
    # NOVO: Gap por Categoria (Requisito BRD)
    st.subheader("Gap de Preço Médio por Categoria")
    gap_cat = df_comm.groupby('categoria')['percentual_gap_preco'].mean().reset_index().sort_values('percentual_gap_preco', ascending=False)
    fig_gap_cat = px.bar(gap_cat, x='categoria', y='percentual_gap_preco', 
                         color='percentual_gap_preco', 
                         color_continuous_scale='RdYlGn_r', # Vermelho para caro, Verde para barato
                         labels={'percentual_gap_preco': 'Gap (%)', 'categoria': 'Categoria'})
    st.plotly_chart(fig_gap_cat, width='stretch')

    # Pergunta: Elasticidade (Preço vs Volume)
    st.subheader("Análise de Elasticidade: Preço vs Volume de Vendas")
    st.markdown("*Objetivo: Identificar se preços altos estão derrubando o volume de vendas.*")
    
    # Filtramos apenas produtos com alguma receita para o gráfico de bolhas ficar legível, 
    # ou mantemos todos com um tamanho mínimo fixo.
    fig_elastic = px.scatter(df_comm, x='preco_nossas_lojas', y='volume_vendas_total', 
                             size=df_comm['receita_vendas_total'] + 1, # +1 garante que zeros apareçam como pontos pequenos
                             color='posicionamento_preco',
                             hover_data=['nome_produto'], 
                             labels={'preco_nossas_lojas': 'Nosso Preço (R$)', 'volume_vendas_total': 'Volume Vendido'})
    st.plotly_chart(fig_elastic, width='stretch')
    
    # Top 20 SKUs Relatório
    st.subheader("Monitoramento de SKU (Top 20 Faturamento)")
    st.dataframe(df_comm.sort_values('receita_vendas_total', ascending=False).head(20), width='stretch')

# --- ABA MARKETING ---
with tabs[2]:
    st.header("👥 CRM, Retenção e Curva ABC")
    df_mkt = load_data("fct_segmentacao_clientes")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        # Pergunta: Quem são os Top 20% (Classe A)
        faturamento_a = df_mkt[df_mkt['curva_abc'] == 'Classe A (Top 20%)']['faturamento_total'].sum()
        share_a = (faturamento_a / df_mkt['faturamento_total'].sum()) * 100
        st.metric("Share Classe A (Pareto)", f"{share_a:.1f}%", help="Percentual do faturamento vindo dos top 20% clientes")
    with col_m2:
        # Pergunta: Recorrência/Frequência
        avg_orders = df_mkt['total_pedidos'].mean()
        st.metric("Média Pedidos/Cliente", f"{avg_orders:.1f}")
    with col_m3:
        # Pergunta: Churn Preventivo
        churn_count = len(df_mkt[df_mkt['status_fidelidade'] == 'Churn'])
        st.metric("Clientes em Churn (>60 dias)", churn_count)

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Distribuição por Curva ABC")
        seg_counts = df_mkt['curva_abc'].value_counts().reset_index()
        fig_seg = px.bar(seg_counts, x='curva_abc', y='count', color='curva_abc')
        st.plotly_chart(fig_seg, width='stretch')
    
    with col_chart2:
        st.subheader("Lista de Clientes em Risco")
        st.dataframe(df_mkt[df_mkt['status_fidelidade'] == 'Churn'][['nome_cliente', 'faturamento_total', 'dias_sem_comprar']].head(10), width='stretch')

# --- ABA OPERAÇÕES ---
with tabs[3]:
    st.header("📦 Saúde de Portfólio e Giro de Estoque")
    df_ops = load_data("fct_saude_portfolio")
    
    # Pergunta: Concentração Top 10
    top10_revenue = df_ops.sort_values('receita_total_produto', ascending=False).head(10)['receita_total_produto'].sum()
    total_revenue_ops = df_ops['receita_total_produto'].sum()
    concentracao_10 = (top10_revenue / total_revenue_ops) * 100 if total_revenue_ops > 0 else 0
    
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        st.metric("Concentração Top 10 SKUs", f"{concentracao_10:.1f}%", help="Dependência do faturamento sobre os 10 maiores produtos")
    with col_o2:
        zombies_count = len(df_ops[df_ops['status_estoque'] == 'Zumbi (Sem Giro)'])
        st.metric("Produtos Zumbis", zombies_count)
    
    st.subheader("Curva ABC de SKUs (Concentração)")
    df_ops = df_ops.sort_values('percentual_participacao_faturamento', ascending=False)
    df_ops['receita_acumulada'] = df_ops['percentual_participacao_faturamento'].cumsum()
    fig_abc = px.line(df_ops, x=list(range(len(df_ops))), y='receita_acumulada', 
                      labels={'x': 'Quantidade de SKUs', 'y': '% Faturamento Acumulado'})
    st.plotly_chart(fig_abc, width='stretch')
    
    st.subheader("Ação Recomenda: Itens para Queima de Estoque")
    st.dataframe(df_ops[df_ops['status_estoque'] == 'Zumbi (Sem Giro)'][['nome_produto', 'categoria', 'dias_sem_venda']].sort_values('dias_sem_venda', ascending=False), width='stretch')
