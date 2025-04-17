import duckdb 

caminho = r"C:\Users\victor.crespo\Downloads\Nova pasta\pncp_contratos.duckdb"
conectar = duckdb.connect(caminho)

teste = conectar.execute("SHOW TABLES").fetchall()


print(teste)