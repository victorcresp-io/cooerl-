import duckdb 

caminho = r"C:\Users\55219\Downloads\teste\banco.duckdb2"

conn = duckdb.connect(caminho)



'''with open('my_app/db/schema_pncp.sql', 'r') as f:
    sql_query = f.read()
    conn.execute(sql_query)'''

palavra = '%pessoas%'
teste = conn.execute("""
    WITH primeira_consulta AS (
        SELECT * FROM contrato_pncp
        WHERE objeto_contrato ILIKE ?
    )
    SELECT 
        p.*,
        o.*,
        d.nome
    FROM primeira_consulta p
    JOIN informacao_contrato o
        ON p.numero_controle_pncp = o.numero_controle_pncp
    JOIN categoria_processo d
        ON o.categoria_processo_id = d.categoria_processo_id
    
""", (palavra,)).df()

print(teste.info())

teste.to_excel('assd.xlsx', engine = 'xlsxwriter')