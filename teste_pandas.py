import pandas as pd
pd.set_option('display.max_columns', None)

caminho2 = r'C:\Users\victor.crespo\Downloads\cooerl\OUTRAS_COMPRAS.CSV'


caminho = r'C:\Users\victor.crespo\Downloads\cooerl\FORNECEDOR_SANCOES.CSV'
df = pd.read_csv(caminho2, sep = ';', encoding = 'latin1')



print(df.info())
df['Data de Aprovação'] = pd.to_datetime(df['Data de Aprovação'], format = '%d/%m/%Y')
df['Data de Aprovação'] = df['Data de Aprovação'].dt.date
print(df.iloc[0])