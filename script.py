import psutil
import os
import time
import sqlite3
import pandas as pd
from my_app.db import get_db
from my_app import create_app



# Obter o processo atual
process = psutil.Process(os.getpid())

# Antes de executar o código
memory_before = process.memory_info().rss

# Código a ser testado
app = create_app()

with app.app_context():

# Conexão com o banco de dados SQLite
    conn = get_db()
    cursor = conn.cursor()
    tabela =  'contratos'
    # Consulta com o parâmetro, utilizando um placeholder
    cursor.execute('SELECT * FROM compras_diretas')

    # Obter os dados retornados pela consulta
    dados = cursor.fetchall()

    # Obter as colunas para mapear aos valores
    for linha in dados:
        print(linha[0])
    # Criar um dicionário para cada linha


    # Exibir o resultado

    # Fechar a conexão
    conn.close()

# Depois de executar o código
memory_after = process.memory_info().rss

print(f'Memória usada: {memory_after - memory_before} bytes')
