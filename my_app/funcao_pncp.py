''# Funções relacionadas à base da API do Portal Nacional de Contratações Públicas (PNCP)
import duckdb 
from my_app.db import get_db2
import pandas as pd
from datetime import datetime

data1 = '01/01/2024'
data2 = '31/12/2024'

data1_att = datetime.strptime(data1, '%d/%m/%Y').year
data2_att = datetime.strptime(data2, '%d/%m/%Y')

caminho = r"Y:\PNCP\contratacoes_parquet\pregao_eletronico\base2024ContratacoesPregoesEletronicosPncpCompleta.parquet"
caminho2 = r"Y:\PNCP\atas_parquet\*.parquet"


'''
def filtrar_contrato(conn, termo):
    df = conn.execute(f"""
            SELECT * FROM '{caminho}'
            WHERE objeto_contrato ILIKE ?
""", (f'%{termo}%',)).df()
    df_contratacao = df["numeroControlePncpCompra"]
    df_ata = conn.execute(f"""
    SELECT * FROM '{caminho2}'
    WHERE numeroControlePNCPCompra == df_ata
""").df()
    
def buscar_dados_pncp(conn, termo):
    teste = conn.execute("""
    WITH primeira_consulta AS (
        SELECT * FROM contrato_pncp
        WHERE objeto_contrato ILIKE ?
    )
    SELECT 
        p.*,
        o.*,
        d.nome,
        f.tipo_pessoa,
        f.nome,
        f.cnpj
    FROM primeira_consulta p
    JOIN informacao_contrato o
        ON p.numero_controle_pncp = o.numero_controle_pncp
    JOIN categoria_processo d
        ON o.categoria_processo_id = d.categoria_processo_id
    JOIN fornecedor f
        ON o.numero_controle_pncp = f.numero_controle_pncp

    
""", (f'%{termo}%',)).fetchall()
    total_valores = len(teste)
    return total_valores



def buscar_dados_pncp_excel(conn, termo):
    teste = conn.execute("""
    WITH primeira_consulta AS (
        SELECT * FROM contrato_pncp
        WHERE objeto_contrato ILIKE ?
    )
    SELECT 
        p.*,
        o.*,
        d.nome,
        f.tipo_pessoa,
        f.nome,
        f.cnpj
    FROM primeira_consulta p
    JOIN informacao_contrato o
        ON p.numero_controle_pncp = o.numero_controle_pncp
    JOIN categoria_processo d
        ON o.categoria_processo_id = d.categoria_processo_id
    JOIN fornecedor f
        ON o.numero_controle_pncp = f.numero_controle_pncp

    
""", (f'%{termo}%',)).df()
    total_valores = teste
    return teste
'''


def filtrar_contrato(con, termo):
    # Filtra contratos pelo termo
    df = con.execute(f"""
        SELECT * FROM contrato_pncp
        WHERE objetoContrato ILIKE ?
    """, (f'%{termo}%',)).df()

    # Extrai lista de contratos encontrados
    contratos = df["numeroControlePncpCompra"].tolist()
    contratos2 = df["numeroControlePNCP"].tolist()
    if not contratos:
        print("Nenhum contrato encontrado com esse termo.")
        return df, pd.DataFrame()

    # Prepara a lista para o SQL IN (...)
    placeholders = ','.join(f"'{c}'" for c in contratos)

    # Filtra as atas relacionadas
    query = f"""
        SELECT * FROM atas_pncp
        WHERE numeroControlePNCPCompra IN ({placeholders})
    """
    df_ata = con.execute(query).df()

    query2 = f"""
        SELECT * FROM contratacoes_pncp
        WHERE numeroControlePNCP IN ({placeholders})
    """
    df_contratacoes = con.execute(query2).df()

    return df, df_ata, df_contratacoes






'''with pd.ExcelWriter("resultado_filtradoAluguel.xlsx", engine = "xlsxwriter") as writer:
    df_contratos.to_excel(writer, sheet_name = "Contratos", index = False)
    df_atas.to_excel(writer, sheet_name = "Atas", index = False)
    df_contratacoes.to_excel(writer, sheet_name = "Contratações", index = False)
    
print("Arquivo Excel 'resultado_filtradoCastramovel2.xlsx' criado com sucesso!")
'''