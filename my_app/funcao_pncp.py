# Funções relacionadas à base da API do Portal Nacional de Contratações Públicas (PNCP)

from my_app.db import get_db2
import pandas as pd
from datetime import datetime

data1 = '01/01/2024'
data2 = '31/12/2024'

data1_att = datetime.strptime(data1, '%d/%m/%Y').year
data2_att = datetime.strptime(data2, '%d/%m/%Y')


def buscar_pncp_termo(termo, ano1, ano2):
    conexao = get_db2()

    res = conexao.execute("""
    SELECT * FROM TESTE WHERE objetoContrato ILIKE ?
        AND ano_consulta IN (?,?)
    """, (f'%{termo}%', ano1, ano2)).df()
    

    conexao.execute("""
        INSERT INTO teste_pncp
            SELECT * FROM res     
    """)
    
    return res






