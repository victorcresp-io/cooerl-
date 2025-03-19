#Funções responsáveis por transformar Dataframes e disponibiliza-los no SQLITE3.

import pandas as pd
from my_app.funcao_fornecedores import tratar_fornecedores
from my_app import funcao_contratos
from my_app import funcao_compras
from my_app import db
from my_app import create_app

app = create_app()

caminho_compras_diretas = r'C:\Users\victor.crespo\Downloads\cooerl\instance\data\COMPRAS_DIRETAS (12).CSV'
#caminho_excel = r'C:\Users\victor.crespo\Downloads\cooerl\instance\data\FORNECEDORES (3).CSV'
#caminho_contratos = r'C:\Users\victor.crespo\Downloads\cooerl\instance\data\CONTRATOS (2).CSV'
#df_fornecedores = pd.read_csv(caminho_excel, sep = ';', encoding = 'latin1')
#df_contrato = pd.read_csv(caminho_contratos, sep = ';', encoding = 'latin1')
df_outras = pd.read_csv(caminho_compras_diretas, sep = ';', encoding = 'latin1')

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

def transformar_sqlite_compras_diretas(df):
  with app.app_context():
      print(f'teste {{df}}')
      df = funcao_compras.tratar_compras(df)

      conn  = db.get_db()

      cursor = conn.cursor()
      print(df)
      df.to_sql('compras_diretas', conn, if_exists = 'append', index = False)
 
      conn.close()

      print(f'Dados inseridos na tabela compras_diretas com sucesso!')



def transformar_sqlite_outras_compras(df):
  with app.app_context():
    df = funcao_compras.tratar_outras_compras(df)

    conn = db.get_db()

    df.to_sql('outras_compras', conn, if_exists = 'append', index = False)
    print(f'Dados inseridos na tabela compras_diretas com sucesso!')

transformar_sqlite_compras_diretas(df_outras)


