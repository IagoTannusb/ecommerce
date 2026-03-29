select
    id_cliente,
    nome_cliente,
    estado,
    pais,
    data_cadastro
from {{source('raw_data','clientes') }}