{{ config(
    materialized='table',
    format='parquet'
) }}

with vendas as (
    select
        id_venda,
        id_cliente,
        id_produto,
        canal_venda,
        quantidade,
        preco_venda,
        data_venda,
        receita_total,
        data_venda_date,
        ano_venda,
        mes_venda
    from {{ ref('int_vendas') }}
), 

clientes as (
    select
        id_cliente,
        nome_cliente,
        estado,
        pais
    from {{ ref('int_clientes') }}
), 

produtos as (
    select
        id_produto,
        nome_produto,
        categoria,
        marca
    from {{ ref('int_produtos') }}
), 

final as (
    select
        -- Chaves e Datas
        v.id_venda,
        v.data_venda,
        v.data_venda_date,
        v.ano_venda,
        v.mes_venda,
        
        -- Dimensões de Negócio
        v.canal_venda,
        c.nome_cliente,
        c.estado as uf_cliente,
        c.pais as pais_cliente,
        p.nome_produto,
        p.categoria as categoria_produto,
        p.marca as marca_produto,
        
        -- Métricas Financeiras
        v.quantidade,
        v.preco_venda,
        v.receita_total
    from vendas v 
    left join clientes c on v.id_cliente = c.id_cliente
    left join produtos p on v.id_produto = p.id_produto
)

select 
    id_venda,
    data_venda,
    data_venda_date,
    ano_venda,
    mes_venda,
    canal_venda,
    nome_cliente,
    uf_cliente,
    pais_cliente,
    nome_produto,
    categoria_produto,
    marca_produto,
    quantidade,
    preco_venda,
    receita_total
from final
