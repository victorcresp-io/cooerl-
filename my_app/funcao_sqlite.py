#Funções responsáveis por transformar Dataframes e disponibiliza-los no SQLITE3.

import pandas as pd
from my_app.funcao_fornecedores import tratar_fornecedores
from my_app import funcao_contratos
from my_app import db
from my_app import create_app

app = create_app()

caminho_excel = r'C:\Users\victor.crespo\Downloads\cooerl\instance\data\FORNECEDORES (3).CSV'
caminho_contratos = r'C:\Users\victor.crespo\Downloads\cooerl\instance\data\CONTRATOS (2).CSV'
df_fornecedores = pd.read_csv(caminho_excel, sep = ';', encoding = 'latin1')
df_contrato = pd.read_csv(caminho_contratos, sep = ';', encoding = 'latin1')


def transformar_sqlite_fornecedores(df): #Função para transformar o Dataframe em SQL e inseri-los na tabela SQL 'fornecedores'
  with app.app_context():

    df = tratar_fornecedores(df) #Tratando o Dataframe FORNECEDORES

    conn = db.get_db()

    cursor = conn.cursor()

    df.to_sql('fornecedores', conn, if_exists = 'append', index = False)

    conn.close()

    print(f'Dados inseridos na tabela fornecedores com sucesso')


def transformar_sqlite_contratos(df): #Função para transformar o Dataframe em SQL e inseri-los na tabela SQL 'fornecedores'
  with app.app_context():

    df = funcao_contratos.tratar_contratos(df) #Tratando o Dataframe FORNECEDORES

    conn = db.get_db()

    cursor = conn.cursor()

    df.to_sql('contratos', conn, if_exists = 'append', index = False)

    conn.close()

    print(f'Dados inseridos na tabela fornecedores com sucesso')

transformar_sqlite_fornecedores(df_fornecedores)