{{ config(
    materialized='table',
    format='parquet'
) }}

with dados_vendas as (
    select
        id_cliente,
        count(distinct id_venda) as total_pedidos,
        sum(receita_total) as faturamento_total,
        max(data_venda_date) as data_ultima_compra
    from {{ ref('int_vendas') }}
    group by 1
), 

clientes_base as (
    select
        id_cliente,
        nome_cliente,
        estado as uf_cliente,
        data_cadastro_date
    from {{ ref('int_clientes') }}
), 

calculo_rfm as (
    select
        c.id_cliente,
        c.nome_cliente,
        c.uf_cliente,
        c.data_cadastro_date,
        v.total_pedidos,
        v.faturamento_total,
        v.data_ultima_compra,
        -- Sintaxe Athena: Diferença em dias entre a última compra e HOJE
        date_diff('day', v.data_ultima_compra, current_date) as dias_sem_comprar
    from clientes_base c 
    inner join dados_vendas v on c.id_cliente = v.id_cliente
),

segmentacao as (
    select
        id_cliente,
        nome_cliente,
        uf_cliente,
        data_cadastro_date,
        total_pedidos,
        faturamento_total,
        data_ultima_compra,
        dias_sem_comprar,
        -- Ranking de faturamento para Curva ABC (0.0 a 1.0)
        percent_rank() over (order by faturamento_total desc) as ranking_faturamento
    from calculo_rfm
)

select
    id_cliente,
    nome_cliente,
    uf_cliente,
    data_cadastro_date,
    total_pedidos,
    faturamento_total,
    data_ultima_compra,
    dias_sem_comprar,
    case
        when ranking_faturamento <= 0.2 then 'Classe A (Top 20%)'
        when ranking_faturamento <= 0.5 then 'Classe B (30%)'
        else 'Classe C (50%)'
    end as curva_abc,
    case 
        when dias_sem_comprar > 60 then 'Churn'
        when dias_sem_comprar > 30 then 'Risco'
        else 'Ativo'
    end as status_fidelidade
from segmentacao