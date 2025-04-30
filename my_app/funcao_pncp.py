# Funções relacionadas à base da API do Portal Nacional de Contratações Públicas (PNCP)

from my_app.db import get_db2
import pandas as pd
from datetime import datetime

data1 = '01/01/2024'
data2 = '31/12/2024'

data1_att = datetime.strptime(data1, '%d/%m/%Y').year
data2_att = datetime.strptime(data2, '%d/%m/%Y')


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


