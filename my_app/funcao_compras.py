#Função para tratar a base COMPRAS DIRETAS e OUTRAS COMPRAS.

import pandas as pd


def tratar_cnpj_df(df): #Função para tratar o CPF e CNPJ.

    if df['cpf_cnpj'].isna().any(): #Caso a coluna CPF/CNPJ não possua valor, ela retornará 0.
      df['cpf_cnpj'].fillna(0, inplace = True)

    if (df['cpf_cnpj'] != 0).any():
      df['cpf_cnpj'] = df['cpf_cnpj'].str.replace('-', '')
      df['cpf_cnpj'] = df['cpf_cnpj'].str.replace('/', '')
      df['cpf_cnpj'] = df['cpf_cnpj'].str.replace('.', '')
      df['cpf_cnpj'] = df['cpf_cnpj'].str.replace(r'\s+', '', regex=True)
      df['cpf_cnpj'] = df['cpf_cnpj'].str.replace(',', '')
      df['cpf_cnpj'] = df['cpf_cnpj'].str.strip()
      return df
      

def tratar_nome_fornecedores(df):
    df['Fornecedor Vencedor'] = df['Fornecedor Vencedor'].str.replace(r'\s+', ' ', regex=True)
    df['Fornecedor Vencedor'] = df['Fornecedor Vencedor'].str.replace(',','')
    df['Fornecedor Vencedor'] = df['Fornecedor Vencedor'].str.replace('.','')
    df['Fornecedor Vencedor'] = df['Fornecedor Vencedor'].str.strip()
    return df

def alterar_colunas_compras(df):
    dados = {
         'Unidade': 'unidade',
         'ID Processo': 'id_processo',
         'Processo': 'processo',
         'Objeto': 'objeto',
         'Afastamento': 'afastamento',
         'Enquadramento Legal': 'enquadramento_legal',
         'Data de Aprovação': 'data_aprovacao',
         'Valor do Processo (R$)': 'valor_processo',
         'CNPJ_CPF': 'cpf_cnpj',
         'Fornecedor Vencedor': 'fornecedor_vencedor',
         'ID Item': 'id_item',
         'Item': 'item',
         'Qtd.': 'quantidade',
         'Unidade de Medida': 'unidade_medida',
         'Vl. Unitário (R$)': 'valor_unitario',
         'PED': 'ped',
         'Regime': 'regime'
    }    

    df.rename(columns=dados, inplace=True)
    print('df_alterado')
    print(df.info())
    return df

def tratar_compras(df): # Função para tratamento da tabela FORNECEDORES.
    df.drop('Data_extracao', axis = 1, inplace = True)
    df.drop('Unnamed: 18', axis = 1, inplace = True)
    df = tratar_nome_fornecedores(df)
    df = alterar_colunas_compras(df)
    df = tratar_cnpj_df(df)
    return df