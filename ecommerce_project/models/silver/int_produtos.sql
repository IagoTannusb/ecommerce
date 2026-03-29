with source_data as (
    select
        id_produto,
        nome_produto,
        categoria,
        marca,
        preco_atual,
        data_criacao
    from {{ ref('stg_produtos') }}
),

-- Limpeza e Tipagem
cleaned as (
    select
        id_produto,
        nome_produto,
        categoria,
        marca,
        cast(preco_atual as double) as preco_atual,
        cast(data_criacao as timestamp) as data_criacao
    from source_data
),

-- Regras de Negócio e Colunas Calculadas
final as (
    select
        id_produto,
        nome_produto,
        categoria,
        marca,
        preco_atual,
        data_criacao,
        case
            when preco_atual > 1000 then 'PREMIUM'
            when preco_atual > 500 then 'MEDIO'
            else 'BASICO'
        end as faixa_preco
    from cleaned
)

select
    id_produto,
    nome_produto,
    categoria,
    marca,
    preco_atual,
    data_criacao,
    faixa_preco
from final