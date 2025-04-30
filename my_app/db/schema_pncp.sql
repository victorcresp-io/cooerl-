-- Criação do SCHEMA relacionado a rota PNCP.


CREATE TABLE IF NOT EXISTS tipo_contrato (
    tipo_contrato_id INT UNIQUE,
    nome VARCHAR 
);

CREATE TABLE IF NOT EXISTS categoria_processo (
    categoria_processo_id INT UNIQUE,
    nome VARCHAR 
);

CREATE TABLE IF NOT EXISTS esfera_adm(
    esfera_adm_id INT UNIQUE,
    esfera_nome VARCHAR
);

CREATE TABLE IF NOT EXISTS esfera_poder(
    esfera_poder_id INTEGER UNIQUE,
    esfera_poder_nome VARCHAR
);

CREATE TABLE IF NOT EXISTS contrato_pncp (
    numero_controle_pncp_compra VARCHAR,
    numero_controle_pncp VARCHAR UNIQUE,
    ano_contrato INT,
    data_assinatura DATETIME,
    data_vigencia_inicio DATETIME,
    data_vigencia_fim DATETIME,
    data_publicacao_pncp TIMESTAMP,
    processo VARCHAR,
    objeto_contrato VARCHAR,
    valor_inicial FLOAT,
    valor_parcela INT,
    valor_global FLOAT,
    valor_acumulado FLOAT
);

CREATE TABLE IF NOT EXISTS informacao_contrato(
    data_atualizacao TIMESTAMP,
    informacao_complementar VARCHAR,
    receita BOOLEAN,
    numero_alteracao_pncp INT, -- Quantidade de vezes que o registro foi alterado no PNCP
    tipo_contrato_id INT REFERENCES tipo_contrato(tipo_contrato_id),
    categoria_processo_id INT REFERENCES categoria_processo(categoria_processo_id),
    empenho_contrato VARCHAR,
    data_atualizacao_global TIMESTAMP,
    identificar_cipi VARCHAR, --Verificar
    url_cipi VARCHAR,
    usuario_nome VARCHAR,
    numero_controle_pncp VARCHAR REFERENCES contrato_pncp(numero_controle_pncp)

);



CREATE TABLE IF NOT EXISTS unidade_orgao(
    unidade VARCHAR,
    codigo_ibge INT,
    codigo_unidade INT,
    uf VARCHAR,
    sigla_uf VARCHAR,
    municipio VARCHAR,
    numero_controle_pncp VARCHAR REFERENCES contrato_pncp(numero_controle_pncp)
    

);
CREATE TABLE IF NOT EXISTS unidade_subrogada(
    unidade VARCHAR,
    codigo_ibge INT,
    codigo_unidade INT,
    uf VARCHAR,
    sigla_uf VARCHAR,
    municipio VARCHAR,
    numero_controle_pncp VARCHAR REFERENCES contrato_pncp(numero_controle_pncp)
    
);

CREATE TABLE IF NOT EXISTS fornecedor(
    tipo_pessoa VARCHAR,
    codigo_pais VARCHAR,
    nome VARCHAR,
    cnpj BIGINT,
    numero_controle_pncp VARCHAR REFERENCES contrato_pncp(numero_controle_pncp)

);


CREATE TABLE IF NOT EXISTS fornecedor_sub(
    nome VARCHAR,
    cnpj BIGINT,
    numero_controle_pncp VARCHAR REFERENCES contrato_pncp(numero_controle_pncp)
);

CREATE TABLE IF NOT EXISTS orgao(
    orgao VARCHAR,
    cnpj BIGINT,
    poder_id INT REFERENCES esfera_poder(esfera_poder_id),
    esfera_id INT REFERENCES esfera_adm(esfera_adm_id),
    numero_controle_pncp VARCHAR REFERENCES contrato_pncp(numero_controle_pncp)
);

CREATE TABLE IF NOT EXISTS orgao_subrogado(
    orgao VARCHAR,
    cnpj BIGINT,
    poder_id INT REFERENCES esfera_poder(esfera_poder_id),
    esfera_id INT REFERENCES esfera_adm(esfera_adm_id),
    numero_controle_pncp VARCHAR REFERENCES contrato_pncp(numero_controle_pncp)
);