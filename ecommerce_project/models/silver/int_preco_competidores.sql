with source_data as (
    select
        id_produto,
        nome_concorrente,
        preco_concorrente,
        data_coleta
    from {{ ref('stg_preco_competidores') }}
),

-- Limpeza e Tipagem
cleaned as (
    select
        id_produto,
        nome_concorrente,
        cast(preco_concorrente as double) as preco_concorrente,
        cast(data_coleta as timestamp) as data_coleta
    from source_data
),

-- Adição de Dimensões Temporais
final as (
    select
        id_produto,
        nome_concorrente,
        preco_concorrente,
        data_coleta,
        date(data_coleta) as data_coleta_date
    from cleaned
)

select
    id_produto,
    nome_concorrente,
    preco_concorrente,
    data_coleta,
    data_coleta_date
from final