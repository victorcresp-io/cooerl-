import pandas as pd
pd.set_option('display.max_columns', None)

caminho2 = r'C:\Users\victor.crespo\Downloads\cooerl\FORNECEDORES (5).CSV'


caminho = r'C:\Users\victor.crespo\Downloads\cooerl\FORNECEDOR_SANCOES.CSV'
df = pd.read_csv(caminho, sep = ';', encoding = 'latin1')

df2 = pd.read_csv(caminho2, sep = ';', encoding = 'latin1')

#print(df2.info())

#resultado = df2[df2['Nome/Razão Social'].str.contains('CALADO GUEDES', case=False)]

#print(resultado)

teste = df2[df2['CPF/CNPJ'].isna()]
#print(teste)


#lista = teste['Nome/Razão Social'].iloc[0:].tolist()


#print(lista)


#print(df2[df2['Nome/Razão Social'] == 'MDPI AG'])



nome = 'trivale ltda'

teste = nome.split()
print(teste)