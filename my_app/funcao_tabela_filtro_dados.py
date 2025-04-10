import duckdb
import pandas as pd
from datetime import datetime
# Função para armazenar os dados excluídos e adicionados, além de aproveitar
# e armazenar os id_processo adicionados.

def dataframe_contratos(conn, data1, data2):

    res = conn.execute("""
        SELECT id_processo FROM contratos WHERE data_adicao_db = ?
        EXCEPT
        SELECT id_processo FROM contratos WHERE data_adicao_db = ?
""", (data1, data2)).df()
    

    resultado_df = conn.execute(f"""
        SELECT n.*, r.*
        FROM res n
        JOIN contratos r ON (n.id_processo = r.id_processo)
    """).df()
    data = datetime.now().date()
    print(data)
    resultado_df['data_adicao_db'] = data

    ids_adicionados = duckdb.execute("""
        SELECT * FROM res
""").fetchall()
    print('Total de ids adicionados', ids_adicionados)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS t1_contratos AS
            SELECT *
            FROM resultado_df
""")
    
    print("MOSTRANDO TODAS AS TABELAS")
    print(conn.execute("SHOW TABLES").fetchall())

    return ids_adicionados



def dataframe_fornecedores(conn, data1, data2):

    res = conn.execute("""
        SELECT cpf_cnpj FROM fornecedores WHERE data_adicao_db = ?
        EXCEPT
        SELECT cpf_cnpj FROM fornecedores WHERE data_adicao_db = ?
""", (data1, data2)).df()
    

    resultado_df = conn.execute(f"""
        SELECT n.*, r.*
        FROM res n
        JOIN fornecedores r ON (n.cpf_cnpj = r.cpf_cnpj)
    """).df()
    data = datetime.now().date()
    print(data)
    resultado_df['data_adicao_db'] = data

    ids_adicionados = duckdb.execute("""
        SELECT * FROM res
""").fetchall()
    print('Total de ids adicionados', ids_adicionados)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS t1_fornecedores AS
            SELECT *
            FROM resultado_df
""")
    
    print("MOSTRANDO TODAS AS TABELAS")
    print(conn.execute("SHOW TABLES").fetchall())

    return ids_adicionados