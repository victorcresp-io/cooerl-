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
            COALESCE(TRY_CAST(niFornecedorSubContratado AS BIGINT), 0)
        FROM df
""")

def inserir_dados_orgao(con, df):
    con.execute("""
    INSERT INTO orgao BY POSITION
        SELECT
            orgaoEntidade_razaoSocial,
            orgaoEntidade_cnpj,
            orgaoEntidade.poderId,
            orgaoEntidade.esferaId
        FROM df
            
""")
    
def inserir_dados_orgao_subrogado(con, df):
    con.execute("""
    INSERT INTO orgao_subrogado BY POSITION
        SELECT
            orgaoSubRogado.razaoSocial,
            orgaoSubRogado.cnpj,
            orgaoSubRogado.poderId,
            orgaoSubRogado.esferaId
        FROM df
""")
    
def inserir_dados_unidade_orgao(con, df):
    con.execute("""
    INSERT INTO unidade_orgao BY POSITION
        SELECT
            unidadeOrgao.nomeUnidade,
            unidadeOrgao.codigoIbge,
            unidadeOrgao.codigoUnidade,
            unidadeOrgao.ufNome,
            unidadeOrgao.ufSigla,
            unidadeOrgao.municipioNome
        FROM df
""")
    
def inserir_dados_unidade_orgao_subrogada(con, df):
    con.execute("""
    INSERT INTO unidade_subrogada BY POSITION
        SELECT
            unidadeSubRogada.nomeUnidade,
            unidadeSubRogada.codigoIbge,
            unidadeSubRogada.codigoUnidade,
            unidadeSubRogada.ufNome
            unidadeSubRogada.ufSigla,
            unidadeOrgao.ufSigla,
            unidadeSubRogada.municipioNome
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
            tipoContrato.id,
            tipoContrato.nome
        FROM df
""")
    

def esfera_poder(con, df):
    con.execute("""
    INSERT INTO esfera_poder BY POSITION
        SELECT
            orgaoEntidade.poderId,
            tipoContrato.nome
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
    print('df depois das duplicas')
    print(df.info())
    return df