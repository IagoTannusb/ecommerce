{{ config(
    materialized='table',
    format='parquet'
) }}

with nossos_produtos as (
    select
        id_produto,
        nome_produto,
        categoria,
        marca,
        preco_atual as preco_nossas_lojas
    from {{ ref('int_produtos') }}
),

precos_concorrentes as (
    select
        id_produto,
        avg(preco_concorrente) as preco_medio_mercado,
        min(preco_concorrente) as preco_minimo_mercado,
        max(preco_concorrente) as preco_maximo_mercado,
        count(distinct nome_concorrente) as qtd_concorrentes_monitorados
    from {{ ref('int_preco_competidores') }}
    group by 1
),

vendas_resumo as (
    select
        id_produto,
        sum(quantidade) as volume_vendas_total,
        sum(receita_total) as receita_vendas_total
    from {{ ref('int_vendas') }}
    group by 1
),

final as (
    select
        p.id_produto,
        p.nome_produto,
        p.categoria,
        p.marca,
        p.preco_nossas_lojas,
        c.preco_medio_mercado,
        c.preco_minimo_mercado,
        c.preco_maximo_mercado,
        c.qtd_concorrentes_monitorados,
        v.volume_vendas_total,
        v.receita_vendas_total,
        -- Cálculo de Gap de Preço: (Nós / Mercado) - 1
        -- Positivo: Somos mais caros | Negativo: Somos mais baratos
        ((p.preco_nossas_lojas / nullif(c.preco_medio_mercado, 0)) - 1) * 100 as percentual_gap_preco
    from nossos_produtos p
    left join precos_concorrentes c on p.id_produto = c.id_produto
    left join vendas_resumo v on p.id_produto = v.id_produto
)

select 
    id_produto,
    nome_produto,
    categoria,
    marca,
    preco_nossas_lojas,
    preco_medio_mercado,
    preco_minimo_mercado,
    preco_maximo_mercado,
    qtd_concorrentes_monitorados,
    volume_vendas_total,
    receita_vendas_total,
    percentual_gap_preco,
    case 
        when percentual_gap_preco > 5 then 'Acima do Mercado'
        when percentual_gap_preco < -5 then 'Abaixo do Mercado'
        else 'Na Média'
    end as posicionamento_preco
from final

