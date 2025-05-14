CREATE TABLE IF NOT EXISTS fornecedor (
    fornecedor VARCHAR,
    dataCadastro DATETIME,
    cidade VARCHAR,
    id_meEpp INT REFERENCES meEpp(id_meEpp),
    id_crc INT REFERENCES crc(id_crc),
    id_crc INT REFERENCES uf(id_uf)
)


CREATE TABLE IF NOT EXISTS crc(
    crc VARCHAR,
    id_crc UNIQUE VARCHAR
)

CREATE TABLE IF NOT EXISTS meEpp(
    me_epp VARCHAR,
    id_meEpp UNIQUE VARCHAR
)


CREATE TABLE IF NOT EXISTS uf (
    uf VARCHAR,
    id_uf UNIQUE VARCHAR
)

'''CREATE TABLE IF NOT EXISTS situacaoFornecedor (
    situacao_empresa VARCHAR,
    id BIGINT
)'''


#Crc contém 2 ('sim', 'nao')
# ME/EPP contém 2 ('sim', 'nao')


# Tipo empresarial contém 76

# UF contém 28

# Situação da empresa contém 5

# Cidade contém 2671