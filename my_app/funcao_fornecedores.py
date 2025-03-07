import pandas as pd
import re

#Funções para tratar a base FORNECEDORES.
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

def tratar_cnpj(cnpj):
    # Substitui caracteres indesejados como hífens, barras, pontos, espaços e vírgulas.
    cnpj = re.sub(r'[^\d]', '', cnpj)  # Remove tudo que não for número.
    cnpj = cnpj.strip()  # Remove espaços antes e depois do CNPJ.
    return cnpj

def tratar_empresa(empresa):
      empresa = empresa.replace('-', '')
      empresa = empresa.replace('  ', ' ')
      empresa = empresa.replace('/', '')
      empresa = empresa.replace('.', '')
      empresa = empresa.replace(r'\s+', '')
      empresa = empresa.replace(',', '')
      empresa = empresa.strip()
      empresa = empresa.upper()
      return empresa

def tratar_nome_fornecedores(df):
    df['Nome/Razão Social'] = df['Nome/Razão Social'].str.replace(r'\s+', ' ', regex=True)
    df['Nome/Razão Social'] = df['Nome/Razão Social'].str.replace(',','')
    df['Nome/Razão Social'] = df['Nome/Razão Social'].str.replace('.','')
    df['Nome/Razão Social'] = df['Nome/Razão Social'].str.strip()
    return df

def alterar_colunas_fornecedores(df):
    dados = {
         'Nome/Razão Social': 'fornecedor',
         'CPF/CNPJ': 'cpf_cnpj',
         'CRC': 'crc',
         'Tipo Empresarial': 'tipo_empresarial',
         'ME/EPP': 'me_epp',
         'Situação da Empresa': 'situacao',
         'Data de Cadastro': 'data_cadastro',
         'Cidade': 'cidade',
    }

    df.rename(columns=dados, inplace=True)
    print('df_alterado')
    print(df.info())
    return df

def tratar_fornecedores(df): # Função para tratamento da tabela FORNECEDORES.
    df['Data de Cadastro'] = pd.to_datetime(df['Data de Cadastro'], format = '%d/%m/%Y')
    df.drop('Data_extracao', axis = 1, inplace = True)
    df = tratar_nome_fornecedores(df)
    df = alterar_colunas_fornecedores(df)
    print('olha o df')
    print(df)
    df = tratar_cnpj_df(df)
    return df




