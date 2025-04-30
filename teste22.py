import duckdb 


conn = duckdb.connect('banco.duckdb4')



'''with open('my_app/db/schema_pncp.sql', 'r') as f:
    sql_query = f.read()
    conn.execute(sql_query)'''

'''palavra = '%pessoas%'
teste = conn.execute("""
    WITH primeira_consulta AS (
        SELECT * FROM contrato_pncp
        WHERE objeto_contrato ILIKE ?
    )
    SELECT 
        p.*,
        o.*,
        d.nome,
        f.tipo_pessoa,
        f.nome,
        f.cnpj
    FROM primeira_consulta p
    JOIN informacao_contrato o
        ON p.numero_controle_pncp = o.numero_controle_pncp
    JOIN categoria_processo d
        ON o.categoria_processo_id = d.categoria_processo_id
    JOIN fornecedor f
        ON o.numero_controle_pncp = f.numero_controle_pncp

    
""", (palavra,)).df()

print(teste.info())

teste.to_excel('sadji.xlsx', engine = 'xlsxwriter')'''


def buscar_dados_pncp(conn, termo):
    teste = conn.execute("""
    WITH primeira_consulta AS (
        SELECT * FROM contrato_pncp
        WHERE objeto_contrato ILIKE ?
    )
    SELECT 
        p.*,
        o.*,
        d.nome,
        f.tipo_pessoa,
        f.nome,
        f.cnpj
    FROM primeira_consulta p
    JOIN informacao_contrato o
        ON p.numero_controle_pncp = o.numero_controle_pncp
    JOIN categoria_processo d
        ON o.categoria_processo_id = d.categoria_processo_id
    JOIN fornecedor f
        ON o.numero_controle_pncp = f.numero_controle_pncp

    
""", (f'%{termo}%',)).fetchall()
    total_valores = len(teste)
    return total_valores



buscar_dados_pncp(conn, 'pessoas')