-- Criação do SCHEMA relacionado a rota PNCP.


CREATE TABLE IF NOT EXISTS contrato_pncp (
    numero_controle_pncp_compra BIGINT,
    numero_controle_pncp BIGINT,
    ano_contrato TIMESTAMP,
    data_assinatura TIMESTAMP,
    data_vigencia_inicio TIMESTAMP,
    data_vigencia_fim TIMESTAMP,
    data_publicacao_pncp TIMESTAMP,
    processo VARCHAR,
    objeto_contrato VARCHAR,
    valor_inicial FLOAT,
    valor_parcela INT,
    valor_global FLOAT,
    valor_acumulado FLOAT
)

CREATE TABLE IF NOT EXISTS informacao_contrato(
    data_atualizacao TIMESTAMP
    informacao_complementar VARCHAR,
    receita BOOLEAN,
    numero_alteracao_pncp INT, -- Quantidade de vezes que o registro foi alterado no PNCP
    tipo_contrato_id INT REFERENCES tipo_contrato(tipo_contrato_id),
    categoria_processo_id INT REFERENCES categoria_processo(categoria_processo_id),
    empenho_contrato INT,
    data_atualizacao_global TIMESTAMP
    identificar_cipi VARCHAR --Verificar
    url_cipi VARCHAR,
    usuario_nome VARCHAR,

)

CREATE TABLE IF NOT EXISTS tipo_contrato (
    tipo_contrato_id INT UNIQUE,
    nome VARCHAR 
)

CREATE TABLE IF NOT EXISTS categoria_processo (
    categoria_processo_id INT UNIQUE,
    nome VARCHAR 
)

CREATE TABLE IF NOT EXISTS orgao(
    orgao VARCHAR,
    cnpj BIGINT,
    poder_id INT,
    efera_id INT
)

CREATE TABLE IF NOT EXISTS orgao_subrogado(
    orgao VARCHAR,
    cnpj BIGINT,
    poder_id INT,
    efera_id INT
)

CREATE TABLE IF NOT EXISTS unidade_orgao(
    unidade VARCHAR,
    codigo_ibge INT,
    codigo_unidade INT,
    uf VARCHAR,
    sigla_uf VARCHAR,
    municipio VARCHAR,

)
CREATE TABLE IF NOT EXISTS unidade_subrogada(
    unidade VARCHAR,
    codigo_ibge INT,
    codigo_unidade INT,
    uf VARCHAR,
    sigla_uf VARCHAR,
    municipio VARCHAR,
    
)

CREATE TABLE IF NOT EXISTS fornecedor(
    tipo_pessoa VARCHAR,
    codigo_pais VARCHAR,
    nome VARCHAR,
    cnpj BIGINT,

)


CREATE TABLE IF NOT EXISTS fornecedor(
    nome VARCHAR,
    cnpj BIGINT,
)