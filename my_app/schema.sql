DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS fornecedores;
DROP TABLE IF EXISTS minha_tabela;


CREATE TABLE fornecedores (
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




