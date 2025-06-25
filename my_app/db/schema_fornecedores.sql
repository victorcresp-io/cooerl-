
CREATE TABLE IF NOT EXISTS fornecedores (
    fornecedor VARCHAR,
    cpf_cnpj BIGINT,
    crc VARCHAR,
    tipo_empresarial VARCHAR,
    me_epp VARCHAR,
    situacao VARCHAR,
    data_cadastro DATETIME,
    cidade VARCHAR,
    uf VARCHAR
);


CREATE TABLE IF NOT EXISTS contratos (
    codigo_contrato INT,
    id_processo INT,
    id_licitacao INT,
    contrato INT,
    status_contratacao VARCHAR,
    data_contratacao DATETIME,
    unidade VARCHAR,
    processo VARCHAR,
    objeto VARCHAR,
    tipo_aquisicao VARCHAR,
    criterio_julgamento VARCHAR,
    data_inicio_vigencia DATETIME,
    data_fim_vigencia DATETIME,
    cpf_cnpj BIGINT,
    valor_total_contrato FLOAT,
    valor_total_empenhado FLOAT,
    valor_total_liquidado FLOAT,
    valor_total_pago FLOAT,
    data_publicacao_deorj DATETIME,
    regime_juridico VARCHAR,
    url_pncp VARCHAR
);

CREATE TABLE IF NOT EXISTS compras_diretas ( 
    unidade VARCHAR,
    id_processo VARCHAR,
    processo VARCHAR,
    objeto VARCHAR,
    afastamento VARCHAR,
    enquadramento_legal VARCHAR,
    data_aprovacao DATETIME,
    valor_processo FLOAT,
    cpf_cnpj BIGINT,
    fornecedor_vencedor VARCHAR,  #Verificar se a coluna cpf_cnpj é do fornecedor_vencedor
    id_item INT,
    item VARCHAR,
    quantidade INT,
    valor_unitario FLOAT,
    ped VARCHAR,
    regime VARCHAR,
    unidade_medida VARCHAR
);

CREATE TABLE IF NOT EXISTS outras_compras ( 
    unidade VARCHAR,
    id_processo INT,
    processo VARCHAR,
    objeto VARCHAR,
    afastamento VARCHAR,
    enquadramento_legal VARCHAR,
    data_aprovacao DATETIME,
    valor_processo FLOAT,
    cpf_cnpj BIGINT,
    fornecedor_vencedor VARCHAR,
    id_item INT,
    item VARCHAR,
    quantidade INT,
    valor_unitario FLOAT,
    regime VARCHAR,
    unidade_medida VARCHAR
);


CREATE TABLE IF NOT EXISTS fornecedores_cpnjnull (
    fornecedor TEXT NOT NULL,
    crc CHAR(3),
    tipo_empresarial TEXT,
    me_epp CHAR(3),
    situacao VARCHAR(40),
    data_cadastro DATETIME,
    cidade VARCHAR(40),
    uf CHAR(2),
    data_adicao DATE DEFAULT (CURRENT_DATE)
)

'''CREATE TABLE IF NOT EXISTS situacaoFornecedor (
    situacao_empresa VARCHAR,
    id BIGINT    
)'''
# 1512 dados vazios tipo_empresarial

#Crc contém 2 ('sim', 'nao')
# ME/EPP contém 2 ('sim', 'nao')


# Tipo empresarial contém 76                                        

# UF contém 28

# Situação da empresa contém 5

# Cidade contém 2671