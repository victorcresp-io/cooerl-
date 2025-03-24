from my_app.db import get_db
import time

'''Função somente para filtragem usando o parâmetro EMPRESA'''


def buscar_contratos( empresa, data, cursor):
    cursor.execute("""
        SELECT COUNT(*) AS total_contratos FROM contratos WHERE fornecedor = ? AND data_adicao = ?
""", (empresa, data))
    resultado = cursor.fetchone()
    print('Total de contratos: ', resultado[0])
    resultado = resultado[0]
    return resultado


def buscar_compras(empresa, data, cursor): 
    inicio = time.time()
    cursor.execute("""
        SELECT COUNT(*) AS total_compras FROM compras_diretas WHERE fornecedor_vencedor = ? AND data_adicao = ?
        UNION ALL
        SELECT COUNT(*) FROM outras_compras WHERE fornecedor_vencedor = ? AND data_adicao = ?
""", (empresa, data, empresa, data))
        
    resultado = cursor.fetchall()

    total_diretas = resultado[0]['total_compras']       
    total_outras = resultado[1]['total_compras']
    print('O total de compras diretas foi de: ', total_diretas)
    print('O total de outras compras foi de: ', total_outras)

    resultado_contratos = buscar_contratos(empresa, data, cursor)
    fim =  time.time()
    tempo = fim - inicio
    print(f'Tempo gasto na função BUSCAR_COMPRAS: {tempo:.6f} segundos')              
    return total_diretas, total_outras, resultado_contratos

def ultima_compra_direta(cursor, empresa, data):
    inicio = time.time()

    cursor.execute("SELECT data_aprovacao, id_processo FROM compras_diretas WHERE (data_adicao = ? AND fornecedor_vencedor = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, empresa))
    res = cursor.fetchone()
    data_ultima_compra_diretas, processo_diretas = res   
    fim = time.time()
    tempo_gasto = fim - inicio
    print(f'Tempo gasto total na função ULTIMA_COMPRA_DIRETA: {tempo_gasto:.6f} segundos')
    return data_ultima_compra_diretas, processo_diretas



def ultima_compra_outra(cursor, empresa, data):
    print('Iniciando a busca pela última compra usando empresa como parâmetro')
    cursor.execute("SELECT data_aprovacao, id_processo FROM outras_compras WHERE (data_adicao = ? AND fornecedor_vencedor = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, empresa))
    res = cursor.fetchone()
    data_ultima_compra_outras, processo_outras = res   
    return data_ultima_compra_outras, processo_outras
    

    '''Funções para filtragem através do parâmetro CNPJ'''

def buscar_contratos_cnpj(cursor, cnpj, data):
    cursor.execute("SELECT COUNT(*) AS total_contratos FROM contratos WHERE cpf_cnpj = ? AND data_adicao = ?" ,(cnpj, data))
    resultado = cursor.fetchone()
    return resultado

def buscar_compras_cnpj(cursor, cnpj, data):
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

    resultado_contratos = buscar_contratos_cnpj(cursor, cnpj, data)
    total_contratos = resultado_contratos[0]

    return total_diretas, total_outras, total_contratos    

def ultima_compra_direta_cnpj(cursor, cnpj, data):
    cursor.execute("SELECT data_aprovacao, id_processo FROM compras_diretas WHERE (data_adicao = ? AND cpf_cnpj = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, cnpj))
    res = cursor.fetchone()
    data_ultima_compra_diretas, processo_diretas = res 
    return data_ultima_compra_diretas, processo_diretas 

def ultima_compra_outra_cnpj(cursor, cnpj, data):
    cursor.execute("SELECT data_aprovacao, id_processo FROM outras_compras WHERE (data_adicao = ? AND cpf_cnpj = ?) ORDER BY data_aprovacao DESC LIMIT 1", (data, cnpj))
    res = cursor.fetchone()
    data_ultima_compra_outras, processo_outras = res
    return data_ultima_compra_outras, processo_outras


'''Função para comparar DATA'''

def comparar_data(data1, data2):
    if data1 > data2:
        data_antiga = data1
    else:
        data_antiga = data2
    return data_antiga