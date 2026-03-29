with source_data as (
    select 
        id_venda,
        data_venda,
        id_cliente,
        id_produto,
        canal_venda,
        quantidade,
        preco_unitario
    from {{ ref('stg_vendas') }}
),
-- Primeira limpeza: garantir que os tipos básicos estão corretos
cleaned as (
    select
        id_venda,
        id_cliente,
        id_produto,
        canal_venda,
        cast(quantidade as integer) as quantidade,
        cast(preco_unitario as double) as preco_venda,
        cast(data_venda as timestamp) as data_venda
    from source_data
),
-- Adição de colunas calculadas e dimensões temporais
final as (
    select
        id_venda,
        id_cliente,
        id_produto,
        canal_venda,
        quantidade,
        preco_venda,
        data_venda,
        -- Cálculo de receita
        quantidade * preco_venda as receita_total,
        -- Dimensões temporais (Sintaxe Athena/Presto)
        date(data_venda) as data_venda_date,
        extract(year from data_venda) as ano_venda,
        extract(month from data_venda) as mes_venda,
        extract(day from data_venda) as dia_venda,
        day_of_week(data_venda) as dia_semana,
        extract(hour from data_venda) as hora_venda
    from cleaned
)
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
    mes_venda,
    dia_venda,
    dia_semana,
    hora_venda
from final