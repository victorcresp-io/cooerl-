DROP TABLE compras_diretas;

CREATE TABLE IF NOT EXISTS fornecedores (
    fornecedor TEXT NOT NULL,
    cpf_cnpj VARCHAR(18),
    crc CHAR(3),
    tipo_empresarial TEXT,
    me_epp CHAR(3),
    situacao VARCHAR(40),
    data_cadastro DATETIME,
    cidade VARCHAR(40),
    UF CHAR(2)
);


CREATE TABLE IF NOT EXISTS contratos (
    codigo_contrato INT,
    id_processo INT,
    id_licitacao INT,
    contrato INT,
    status_contratacao TEXT,
    data_contratacao DATETIME,
    unidade TEXT,
    processo TEXT,
    objeto TEXT,
    tipo_aquisicao TEXT,
    criterio_julgamento TEXT,
    data_inicio_vigencia DATETIME,
    data_fim_vigencia DATETIME,
    fornecedor TEXT,
    cpf_cnpj VARCHAR(18),
    valor_total_contrato FLOAT,
    valor_total_empenhado FLOAT,
    valor_total_liquidado FLOAT,
    valor_total_pago FLOAT,
    data_publicacao_deorj DATETIME,
    regime_juridico TEXT,
    url_pncp TEXT
);

CREATE TABLE IF NOT EXISTS compras_diretas ( 
    unidade TEXT,
    id_processo INT,
    processo TEXT,
    objeto TEXT,
    afastamento TEXT,
    enquadramento_legal TEXT,
    data_aprovacao DATETIME,
    valor_processo FLOAT,
    cpf_cnpj VARCHAR(18),
    fornecedor_vencedor TEXT,
    id_item INT,
    item TEXT,
    quantidade INT,
    valor_unitario FLOAT,
    ped VARCHAR(3),
    regime TEXT,
    unidade_medida TEXT
);

