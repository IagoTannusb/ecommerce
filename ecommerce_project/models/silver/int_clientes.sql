with source_data as (
    select
        id_cliente,
        nome_cliente,
        estado,
        pais,
        data_cadastro
    from {{ ref('stg_clientes') }}
),

-- Limpeza e Tipagem
cleaned as (
    select
        id_cliente,
        nome_cliente,
        upper(estado) as estado, -- Padronização para consistência geográfica
        upper(pais) as pais,
        cast(data_cadastro as timestamp) as data_cadastro
    from source_data
),

-- Adição de Dimensões Temporais
final as (
    select
        id_cliente,
        nome_cliente,
        estado,
        pais,
        data_cadastro,
        date(data_cadastro) as data_cadastro_date
    from cleaned
)

select
    id_cliente,
    nome_cliente,
    estado,
    pais,
    data_cadastro,
    data_cadastro_date
from final