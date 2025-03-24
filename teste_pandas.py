import pandas as pd
pd.set_option('display.max_columns', None)

#caminho2 = r'C:\Users\victor.crespo\Downloads\cooerl\OUTRAS_COMPRAS.CSV'


#caminho = r'C:\Users\victor.crespo\Downloads\cooerl\FORNECEDOR_SANCOES.CSV'
#df = pd.read_csv(caminho2, sep = ';', encoding = 'latin1')



#print(df.info())
#df['Data de Aprovação'] = pd.to_datetime(df['Data de Aprovação'], format = '%d/%m/%Y')
#df['Data de Aprovação'] = df['Data de Aprovação'].dt.date
#print(df.iloc[0])

from datetime import datetime

data = datetime.now().date()

data_antiga = '21/01/2020'

data_antiga = datetime.strptime(data_antiga, '%d/%m/%Y').date()
print(data_antiga)
if data > data_antiga:
    print('ok')