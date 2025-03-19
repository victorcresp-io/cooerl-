from my_app.db import get_db


def buscar_contratos(cnpj, empresa, data, conn):
    cursor = conn.cursor()
    if cnpj:
        cursor.execute("""
            SELECT COUNT(*) AS total_contratos FROM contratos WHERE cpf_cnpj = ? AND data_adicao = ?
    """, (cnpj, data))
        resultado = cursor.fetchone()
        print('Total de contratos: ', resultado[0])
        resultado = resultado[0]
        print('aqui', resultado)
    else:
        cursor.execute("""
            SELECT COUNT(*) AS total_contratos FROM contratos WHERE fornecedor = ? AND data_adicao = ?
""", (empresa, data))
        resultado = cursor.fetchone()
        print('Total de contratos: ', resultado[0])
        resultado = resultado[0]
        print('aqui', resultado)
    return resultado

def buscar_compras(cnpj, empresa, data): 
    conn = get_db()
    cursor = conn.cursor()
    if cnpj:
        cursor.execute("""
            SELECT COUNT(*) AS total_compras FROM compras_diretas WHERE cpf_cnpj = ? AND data_adicao = ?
            UNION ALL
            SELECT COUNT(*)  FROM outras_compras WHERE cpf_cnpj = ? AND data_adicao = ?                                                         
    """, (cnpj, data, cnpj, data))
        
        resultado = cursor.fetchall()

        total_diretas = resultado[0]['total_compras']
        total_outras = resultado[1]['total_compras']
        print('O total de compras diretas foi de: ', total_diretas)
        print('O total de outras compras foi de: ', total_outras)
    else:
        cursor.execute("""
            SELECT COUNT(*) AS total_compras FROM compras_diretas WHERE fornecedor_vencedor = ? AND data_adicao ?
            UNION ALL
            SELECT COUNT(*) FROM outras_compras WHERE fornecedor_vencedor = ? AND data_adicao = ?
""", (empresa, data, empresa, data))
        
        resultado = cursor.fetchall()

        total_diretas = resultado[0]['total_compras']       
        total_outras = resultado[1]['total_compras']
        print('O total de compras diretas foi de: ', total_diretas)
        print('O total de outras compras foi de: ', total_outras)

    resultado_contratos = buscar_contratos(cnpj, empresa, data, conn)              
    return total_diretas, total_outras, resultado_contratos

def ultima_compra_direta(conn, cnpj, empresa, data,):
    cursor = conn.cursor()
    if cnpj:
        print('iniciando com cnpj')
        cursor.execute("SELECT data_aprovacao, id_processo FROM compras_diretas WHERE (data_adicao = ? AND cpf_cnpj = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, cnpj))
        res = cursor.fetchone()
        data_ultima_compra_diretas, processo_diretas = res
        print('compras diretas passou') 
        print(data_ultima_compra_diretas)
        print(processo_diretas)
    else:
        print('Iniciando a busca pela última compra usando empresa como parâmetro')
        cursor.execute("SELECT data_aprovacao, id_processo FROM compras_diretas WHERE (data_adicao = ? AND fornecedor_vencedor = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, empresa))
        res = cursor.fetchone()
        data_ultima_compra_diretas, processo_diretas = res   
    return data_ultima_compra_diretas, processo_diretas


def ultima_compra_outra(conn, cnpj, empresa, data):
    cursor = conn.cursor()
    if cnpj:
        print('iniciando com cnpj')
        cursor.execute("SELECT data_aprovacao, id_processo FROM outras_compras WHERE (data_adicao = ? AND cpf_cnpj = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, cnpj))
        res = cursor.fetchone()
        data_ultima_compra_diretas, processo_diretas = res
        print('compras diretas passou') 
        print(data_ultima_compra_diretas)
        print(processo_diretas)
    else:
        print('Iniciando a busca pela última compra usando empresa como parâmetro')
        cursor.execute("SELECT data_aprovacao, id_processo FROM compras_diretas WHERE (data_adicao = ? AND fornecedor_vencedor = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, empresa))
        res = cursor.fetchone()
        data_ultima_compra_diretas, processo_diretas = res   
    return data_ultima_compra_diretas, processo_diretas
        