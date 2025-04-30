import pandas as pd
import duckdb


def inserir_dados_fornecedor(con, df):

    con.execute("""INSERT INTO fornecedor BY POSITION 
        SELECT
            tipoPessoa,
            codigoPaisFornecedor,
            nomeRazaoSocialFornecedor,
            COALESCE(TRY_CAST(niFornecedor AS BIGINT), 0),
            numeroControlePNCP
            
            
        FROM df
""")

def inserir_dados_fornecedor_sub(con, df):
    con.execute("""INSERT INTO fornecedor_sub BY POSITION 
        SELECT
            nomeFornecedorSubContratado,
            COALESCE(TRY_CAST(niFornecedorSubContratado AS BIGINT), 0),
            numeroControlePNCP
        FROM df
""")

def inserir_dados_orgao(con, df):
    con.execute("""
    INSERT INTO orgao BY POSITION
        SELECT
            orgaoEntidade_razaoSocial,
            orgaoEntidade_cnpj,
            orgaoEntidade_poderId,
            orgaoEntidade_esferaId,
            numeroControlePNCP
        FROM df
            
""")
    
def inserir_dados_orgao_subrogado(con, df):
    con.execute("""
    INSERT INTO orgao_subrogado BY POSITION
        SELECT
            orgaoSubRogado_razaoSocial,
            orgaoSubRogado_cnpj,
            orgaoSubRogado_poderId,
            orgaoSubRogado_esferaId,
            numeroControlePNCP
        FROM df
""")
    
def inserir_dados_unidade_orgao(con, df):
    con.execute("""
    INSERT INTO unidade_orgao BY POSITION
        SELECT
            unidadeOrgao_nomeUnidade,
            unidadeOrgao_codigoIbge,
            unidadeOrgao_codigoUnidade,
            unidadeOrgao_ufNome,
            unidadeOrgao_ufSigla,
            unidadeOrgao_municipioNome
        FROM df
""")
    
def inserir_dados_unidade_orgao_subrogada(con, df):
    con.execute("""
    INSERT INTO unidade_subrogada BY POSITION
        SELECT
            unidadeSubRogada_nomeUnidade,
            unidadeSubRogada_codigoIbge,
            unidadeSubRogada_codigoUnidade,
            unidadeSubRogada_ufNome
            unidadeSubRogada_ufSigla,
            unidadeOrgao_ufSigla,
            unidadeSubRogada_municipioNome
        FROM df
""")
    
def inserir_dados_informacao_contrato(con, df):
    con.execute("""
    INSERT INTO informacao_contrato BY POSITION
        SELECT
            dataAtualizacao,
            informacaoComplementar, 
            receita,
            numeroRetificacao,
            tipoContrato_id,
            categoriaProcesso_id,
            numeroContratoEmpenho,
            dataAtualizacaoGlobal,
            identificadorCipi,
            urlCipi,
            usuarioNome,
            numeroControlePNCP
        FROM df      
""")
    


def tipo_contrato(con, df):
    con.execute("""
    INSERT INTO tipo_contrato BY POSITION
        SELECT
            tipoContrato_id,
            tipoContrato_nome
        FROM df
""")
    

def esfera_poder(con, df):
    con.execute("""
    INSERT INTO esfera_poder BY POSITION
        SELECT
            orgaoEntidade_poderId,
            tipoContrato_nome
        FROM df
""")
    
def esfera_adm(con, df):
    con.execute("""
    INSERT INTO esfera_adm BY POSITION
        SELECT
            orgaoEntidade.esferaId,
            tipoContrato.nome
        FROM df
""")

def inserir_dados_contrato(con, df):
    con.execute("""
    INSERT INTO contrato_pncp BY POSITION
        SELECT
            numeroControlePncpCompra,
            numeroControlePNCP, 
            anoContrato,
            dataAssinatura,
            dataVigenciaInicio,
            dataVigenciaFim,
            dataPublicacaoPncp,
            processo,
            objetoContrato,
            valorInicial,
            valorParcela,
            valorGlobal,
            valorAcumulado
        FROM df
""")


def tratar_dados(df):
    df['numeroControlePncpCompra'] = df['numeroControlePncpCompra'].str.replace(r"[\/\-\"']", '', regex=True)
    df['numeroControlePNCP'] = df['numeroControlePNCP'].str.replace(r"[\/\-\"']", '', regex=True)
    df['dataPublicacaoPncp'] = df['dataPublicacaoPncp'].str.replace("T", ' ')
    df['dataAtualizacao'] = df['dataAtualizacao'].str.replace("T", ' ')
    df['dataAtualizacaoGlobal'] = df['dataAtualizacaoGlobal'].str.replace("T", ' ')
    df.columns = [col.replace('.', '_') for col in df.columns]
    print(df.columns)
    print('df antes da remoção de duplicadas')
    print(df.info())
    df = df.drop_duplicates()
    print('df depois das duplicadass')
    print(df.info())
    df['orgaoEntidade_poderId'] = df['orgaoEntidade_poderId'].replace({'L': 1, 'E': 2, 'J': 3, 'N': 4})
    df['orgaoEntidade_esferaId'] = df['orgaoEntidade_esferaId'].replace({'F': 1, 'E': 2, 'M': 3, 'D': 4, 'N': 5 })
    df['orgaoSubRogado_esferaId'] = df['orgaoSubRogado_esferaId'].replace({'F': 1, 'E': 2, 'M': 3, 'D': 4, 'N': 5 })
    df['orgaoSubRogado_poderId'] = df['orgaoSubRogado_poderId'].replace({'L': 1, 'E': 2, 'J': 3, 'N': 4})
    return df