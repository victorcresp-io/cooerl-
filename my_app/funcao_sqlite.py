#Funções responsáveis por transformar Dataframes e disponibiliza-los no SQLITE3.

import pandas as pd
import sqlite3
from my_app import funcao_fornecedores
from my_app import db
from my_app import create_app

app = create_app()

caminho_excel = r'C:\Users\victor.crespo\Downloads\cooerl\instance\data\FORNECEDORES (3).CSV'

df = pd.read_csv(caminho_excel, sep = ';', encoding = 'latin1')

print(df.info())

def transformar_sqlite_fornecedores(df):
  with app.app_context():

    df = funcao_fornecedores.tratar_fornecedores(df) #Tratando o Dataframe FORNECEDORES

    conn = db.get_db()

    cursor = conn.cursor()

    df.to_sql('fornecedores', conn, if_exists = 'append', index = False)

    conn.close()

    print(f'Dados inseridos na tabela fornecedores com sucesso')


transformar_sqlite_fornecedores(df)