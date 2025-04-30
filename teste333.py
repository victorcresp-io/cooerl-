import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import duckdb
import json
import urllib3
import time
from datetime import datetime
from funcao_etl import tipo_contrato, inserir_dados_contrato, inserir_dados_informacao_contrato, inserir_dados_fornecedor, tratar_dados 


# Desativa o aviso de HTTPS inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Nome do banco e tabela
db_path = "pncp_contratos.duckdb"
table_name = "contratos"

# Parâmetros base da API
URL = "https://pncp.gov.br/pncp-consulta/v1/contratos"
params_base = {
    "dataInicial": "20240425",
    "dataFinal": "20240429"
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "accept": "application/json"
}


# Função para buscar dados de uma página
def fetch_page(pagina):
    params = params_base.copy()
    params["pagina"] = pagina
    tentativas = 3
    for tentativa in range(tentativas):
        try:
            response = requests.get(URL, params=params, headers=headers, verify=False, timeout=60)
            response.raise_for_status()
            data = response.json()
            print(f"✅ Página {pagina} processada")
            return data.get("data", [])
        except Exception as e:
            print(f"⚠️ Erro na página {pagina}, tentativa {tentativa + 1}: {e}")
            time.sleep(2)
    print(f"❌ Falha definitiva na página {pagina}")
    return []


# Descobrir total de páginas
try:
    res = requests.get(URL, params={**params_base, "pagina": 1}, headers=headers, verify=False)
    res.raise_for_status()
    total_paginas = res.json().get("totalPaginas", 1)
    print(f"🔢 Total de páginas: {total_paginas}")
except Exception as e:
    print("Erro ao buscar total de páginas:", e)
    total_paginas = 1

# Buscar os dados em paralelo
dados = []
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = {executor.submit(fetch_page, pagina): pagina for pagina in range(1, total_paginas + 1)}
    for future in as_completed(futures):
        pagina = futures[future]
        try:
            result = future.result()
            dados.extend(result)
        except Exception as e:
            print(f"❌ Exceção inesperada na página {pagina}: {e}")

# Converte para DataFrame
df = pd.json_normalize(dados)
caminho = r"C:\Users\55219\Downloads\teste\banco.duckdb2"
con = duckdb.connect(caminho)
df = tratar_dados(df)
res=con.execute("SHOW TABLES").fetchall()
print(res)

con.execute("""
    INSERT INTO esfera_adm VALUES
        (1, 'Federal'),
        (2, 'Estadual'),
        (3, 'Municipal'),
        (4, 'Distrital'),
        (5, 'N')          
""")

con.execute("""
    INSERT INTO categoria_processo VALUES
        (1, 'Cessão'),
        (2, 'Compras'),
        (3, 'Informática (TIC)'),
        (4, 'Internacional'),
        (5, 'Locação Imóveis'),
        (6, 'Mão de Obra'),
        (7, 'Obras'),
        (8, 'Serviços'),
        (9, 'Serviços de Engenharia'),
        (10, 'Serviços de Saúde'),
        (11, 'Alienação de bens móveis/imóveis')
""")

con.execute("""
    INSERT INTO tipo_contrato VALUES
        (1, 'Contrato (Termo Inicial)'),
        (2, 'Comodato'),
        (3, 'Arrendamento'),
        (4, 'Concessão'),
        (5, 'Termo de Adesão'),
        (6, 'Convênio'),
        (7, 'Empenho'),
        (8, 'Outros'),
        (9, 'Termo de Execução Descentralizada (TED)'),
        (10, 'Acordo de Cooperação Técnica (ACT)'),
        (11, 'Termo de Compromisso'),
        (12, 'Carta Contrato')
""")


con.execute("""
    INSERT INTO esfera_poder VALUES
                  
        (1, 'Legislativo'),
        (2, 'Executivo'),
        (3, 'Judiciário'),
        (4, 'N')
""")

inserir_dados_contrato(con,df)
inserir_dados_fornecedor(con,df)
inserir_dados_informacao_contrato(con,df)