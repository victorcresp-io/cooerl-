import sqlite3
import pandas as pd


# Conexão com o banco de dados SQLite
conn = sqlite3.connect(r'C:\Users\victor.crespo\Downloads\cooerl\instance\flaskr.sqlite')
cursor = conn.cursor()
tabela =  'contratos'
# Consulta com o parâmetro, utilizando um placeholder
cursor.execute('SELECT * FROM fornecedores')

# Obter os dados retornados pela consulta
dados = cursor.fetchall()

# Obter as colunas para mapear aos valores
colunas = [desc[0] for desc in cursor.description]

# Criar um dicionário para cada linha
resultado = [dict(zip(colunas, row)) for row in dados]

# Exibir o resultado
print(resultado)

# Fechar a conexão
conn.close()



