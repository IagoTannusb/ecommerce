select 
    id_produto,
    nome_produto,
    categoria,
    marca,
    preco_atual,
    data_criacao
from {{source('raw_data','produtos')}}