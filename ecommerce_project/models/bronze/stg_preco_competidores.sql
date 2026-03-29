select
    id_produto,
    nome_concorrente,
    preco_concorrente,
    data_coleta
from {{ source('raw_data', 'preco_competidores') }}
