import pandas as pd
pd.set_option('display.max_columns', None)


caminho = r'C:\Users\victor.crespo\Downloads\cooerl\FORNECEDOR_SANCOES.CSV'
df = pd.read_csv(caminho, sep = ';', encoding = 'latin1')


print(df.info())
print(df)