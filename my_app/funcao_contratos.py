import pandas as pd
import re

#Funções para tratar a base CONTRATOS.

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
    df['Fornecedor'] = df['Fornecedor'].str.replace(r'\s+', ' ', regex=True)
    df['Fornecedor'] = df['Fornecedor'].str.replace(',','')
    df['Fornecedor'] = df['Fornecedor'].str.replace('.','')
    df['Fornecedor'] = df['Fornecedor'].str.strip()
    return df

def alterar_colunas_fornecedores(df):
    dados = {
         'Código do Contrato': 'codigo_contrato',
         'ID Processo': 'id_processo',
         'ID Licitação': 'id_licitacao',
         'Contratação': 'contrato',
         'Data Contratação': 'data_contratacao',
         'Unidade': 'unidade',
         'Processo': 'processo',
         'Objeto': 'objeto',
         'Tipo de Aquisição': 'tipo_aquisicao',
         'Critério de Julgamento': 'criterio_julgamento',
         'Data Início Vigência': 'data_inicio_vigencia',
         'Data Fim Vigência': 'data_fim_vigencia',
         'Fornecedor': 'fornecedor',
         'CPF/CNPJ': 'cpf_cnpj',
         'Valor Total Contrato/Valor Estimado para Contratação (R$)': 'valor_total_contrato',
         'Valor Total Empenhado (R$)': 'valor_total_empenhado',
         'Valor Total Liquidado (R$)': 'valor_total_liquidado',
         ' Valor Total Pago (R$)': 'valor_total_pago',
         'Data Public DEORJ': 'data_publicacao_deorj',
         'regimejuridico': 'regime_juridico',
         'URL PNCP': 'url_pncp',
         'Status Contratação': 'status_contratacao'
    }

    df.rename(columns=dados, inplace=True)
    print('df_alterado')
    print(df.info())
    return df

def tratar_ids(df):
   df['ID Processo'] = pd.to_numeric(df['ID Processo'], errors = 'coerce').fillna(0).astype(int)
   df['ID Processo'] = pd.to_numeric(df['ID Processo'], errors = 'coerce').fillna(0).astype(int)
   return df

def tratar_contratos(df): # Função para tratamento da tabela FORNECEDORES.
    df.drop('data_extracao', axis = 1, inplace = True)
    df = tratar_nome_fornecedores(df)
    df = alterar_colunas_fornecedores(df)
    print('olha o df')
    print(df)
    df = tratar_cnpj_df(df)
    return df