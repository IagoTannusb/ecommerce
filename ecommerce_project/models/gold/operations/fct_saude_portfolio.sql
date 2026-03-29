{{ config(
    materialized='table',
    format='parquet'
) }}

with resumo_vendas as (
    select
        id_produto,
        sum(quantidade) as total_unidades_vendidas,
        sum(receita_total) as receita_total_produto,
        max(data_venda_date) as data_ultima_venda
    from {{ ref('int_vendas') }}
    group by 1
),

cadastro_produtos as (
    select
        id_produto,
        nome_produto,
        categoria,
        marca,
        preco_atual
    from {{ ref('int_produtos') }}
),

faturamento_global as (
    select 
        sum(receita_total) as receita_total_empresa 
    from {{ ref('int_vendas') }}
),

final as (
    select
        p.id_produto,
        p.nome_produto,
        p.categoria,
        p.marca,
        p.preco_atual,
        coalesce(v.total_unidades_vendidas, 0) as total_unidades_vendidas,
        coalesce(v.receita_total_produto, 0) as receita_total_produto,
        v.data_ultima_venda,
        -- Sintaxe Athena: Coalesce para evitar NULLs (999 dias para produtos sem venda)
        coalesce(date_diff('day', v.data_ultima_venda, current_date), 999) as dias_sem_venda,
        -- Subquery de faturamento global
        (coalesce(v.receita_total_produto, 0) / (select receita_total_empresa from faturamento_global)) * 100 as percentual_participacao_faturamento
    from cadastro_produtos p 
    left join resumo_vendas v on p.id_produto = v.id_produto
)

select 
    id_produto,
    nome_produto,
    categoria,
    marca,
    preco_atual,
    total_unidades_vendidas,
    receita_total_produto,
    data_ultima_venda,
    dias_sem_venda,
    percentual_participacao_faturamento,
    case 
        when dias_sem_venda > 180 or data_ultima_venda is null then 'Zumbi (Sem Giro)'
        when dias_sem_venda > 90 then 'Baixo Giro'
        else 'Ativo'
    end as status_estoque
from final
