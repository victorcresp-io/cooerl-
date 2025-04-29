import duckdb 

caminho = r"Y:\database_siga\teste.duckdb2"

conn = duckdb.connect(caminho)



with open('my_app/db/schema_pncp.sql', 'r') as f:
    sql_query = f.read()
    conn.execute(sql_query)

teste = conn.execute("SHOW TABLES").fetchall()

for item in teste:
    print(item)

