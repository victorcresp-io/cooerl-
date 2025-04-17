from flask import Blueprint, request, send_file, render_template, flash, redirect, url_for, jsonify
from my_app.db import get_db, get_db2
from my_app.funcao_buscadb import buscar_compras, ultima_compra_direta, ultima_compra_outra, buscar_compras_cnpj, ultima_compra_direta_cnpj, ultima_compra_outra_cnpj, comparar_data, consulta_contratos, consulta_fornecedores, consulta_compras_diretas, consulta_outras_compras
from my_app.funcao_fornecedores import tratar_cnpj, tratar_empresa
from my_app.funcao_pncp import buscar_pncp_termo
import pandas as pd
from io import BytesIO
import time
from datetime import datetime




bp = Blueprint('siga', __name__)

@bp.route('/')
def rota():
    return 'oi'

@bp.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    resumo = None
    empresa_db = None
    situacao = None
    empresa_filtro = None
    cnpj_db = None
    data = '22/03/2025'
    data = datetime.strptime(data, '%d/%m/%Y').date()
    time_inicio = time.time()

    """ Rota para processar a requisição e redirecionar para o download """
    if request.method == 'POST':
        empresa_filtro = request.form.get('empresa')
        empresa_filtro = tratar_empresa(empresa_filtro)
        cnpj_filtro = request.form.get('cnpj')
        cnpj_filtro = tratar_cnpj(cnpj_filtro)
        print(f'Empresa recebida no formulário: {empresa_filtro}')
        print(f'CNPJ recebido no formulário: {cnpj_filtro}')

        #Verificando se a empresa está na base FORNECEDORES.
        db = get_db()
        cursor = db.cursor()
        tempo1 = time.time()
        print('Conexão com banco de dados feita com sucesso!')
        print('Data usada como parâmetro: ', data)
        try:
            cursor.execute('SELECT cpf_cnpj, situacao FROM fornecedores WHERE fornecedor = ? AND data_adicao = ?' , (empresa_filtro, data))
            resultado = cursor.fetchone()
            cnpj_db, situacao = resultado
            print(f'Tudo ok por aqui. CNPJ_DB : {cnpj_db} e a situação é {situacao}')

            if cnpj_db:

                resultado = buscar_compras_cnpj(cursor, cnpj_db, data)
                total_compras_diretas = resultado[0]
                total_outras_compras = resultado[1]
                total_contratos = resultado[2]
                ultima_compra = resultado[3]


                resumo = {
                        'empresa': empresa_filtro,
                        'situacao': situacao,
                        'total_compras_diretas': total_compras_diretas,
                        'total_outras_compras': total_outras_compras,
                        'total_contratos': total_contratos,
                        'ultima_compra': ultima_compra
                        }
                print('Resumo feito')
                tempo2 = time.time()

                tempo_total = tempo2 - tempo1
                print(f'Tempo total gasto foi de {tempo_total:.6f}')
            else:

                resultado = buscar_compras(empresa_filtro, data, cursor)
                data_ultima_compra_direta = ultima_compra_direta(cursor, empresa_filtro, data)
                data_ultima_compra_outra = ultima_compra_outra(cursor, empresa_filtro, data)

                total_compras_diretas, total_outras_compras, total_contratos = resultado
                data_ultima_direta, processo_ultima_direta =data_ultima_compra_direta
                data_ultima_outra, processo_ultima_outra = data_ultima_compra_outra

                data_recente = comparar_data(data_ultima_direta, data_ultima_outra)


                resumo = {
                        'empresa': empresa_db,
                        'situacao': situacao,
                        'total_compras_diretas': total_compras_diretas,
                        'total_outras_compras': total_outras_compras,
                        'total_contratos': total_contratos,
                        'ultima_compra': data_recente
                        }
                print('Resumo feito')    

        except Exception as e:
            flash('Empresa não encontrada, verifique o nome ou cnpj', category= 'error')
        

                
            return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_filtro, cnpj_filtro = cnpj_db)
        except Exception as e:
            print('Aconteceu o seguinte erro:', e)


    
    print('até aqui ok', empresa_filtro)

    return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_filtro, cnpj_filtro = cnpj_db, data_recente = data)


@bp.route('/get_fornecedores', methods=['GET'])
def get_fornecedores():
    termo = request.args.get('termo', '').strip().upper()

    if not termo:
        return jsonify([])  # Se o usuário não digitou nada, retorna lista vazia

    try:
        # Conectar ao banco de dados SQLite
        conn = get_db()
        cursor = conn.cursor()

        # Consulta para buscar fornecedores que contêm o termo digitado
        cursor.execute("SELECT DISTINCT(fornecedor) FROM fornecedores WHERE fornecedor LIKE ? LIMIT 5", (f"%{termo}%",))
        fornecedores = [row[0] for row in cursor.fetchall()]  # Converte os resultados para uma lista

        conn.close()  # Fecha a conexão
        return jsonify(fornecedores)

    except Exception as e:
        print(f"Erro ao buscar fornecedores: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500

@bp.route('/excel_download')
def excel_download():
    """ Rota para gerar o arquivo Excel diretamente do banco """
    empresa = request.args.get('empresa_filtro')
    print('termo empresa', empresa)
    cnpj = request.args.get('cnpj_filtro')
    data = request.args.get('data_recente')
    print(data)
    #print(empresa)
    print(cnpj)

    db = get_db()
    cursor = db.cursor()


    query_fornecedores = 'SELECT * FROM fornecedores WHERE data_adicao = ? AND (cpf_cnpj = ? OR fornecedor = ?)' 

    query_contratos = 'SELECT * FROM contratos WHERE data_adicao = ? AND (cpf_cnpj = ? OR fornecedor = ?)'

    query_compras_diretas = 'SELECT * FROM compras_diretas WHERE data_adicao = ? AND (cpf_cnpj = ? OR fornecedor_vencedor = ?)'

    query_outras_compras = 'SELECT * FROM outras_compras WHERE data_adicao = ? AND (cpf_cnpj = ? OR fornecedor_vencedor = ?)'




    # Consultar dados diretamente do banco
    df_fornecedores = pd.read_sql_query(query_fornecedores, db, params = (data, cnpj, empresa))
    df_contratos = pd.read_sql_query(query_contratos, db, params = (data, cnpj, empresa))
    df_compras_diretas = pd.read_sql_query(query_compras_diretas, db, params = (data, cnpj, empresa))
    df_outras_compras = pd.read_sql_query(query_outras_compras, db, params = (data, cnpj, empresa))

    nome = empresa.split()
    primeiro_nome = nome[0]
    segundo_nome = nome[1]

    nome_todo = primeiro_nome + '_' + segundo_nome + '.xlsx'
    nome_todo = nome_todo.lower()
    # Criar o arquivo Excel na memória
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_fornecedores.to_excel(writer, index=False, sheet_name='Fornecedores')
        df_contratos.to_excel(writer, index=False, sheet_name='Contratos')
        df_compras_diretas.to_excel(writer, index = False, sheet_name = 'Compras Diretas')
        df_outras_compras.to_excel(writer, index = False, sheet_name = 'Outras Compras')
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=nome_todo,
        mimetype='application/vnds.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@bp.route('/acompanhamento_siga', methods = ['GET'])
def acompanhamento_siga():
    conn = get_db2()
    data1 = '11/04/2025' #data recente 
    data2 = '10/04/2025'

    data1_att = datetime.strptime(data1, '%d/%m/%Y').date()
    data2_att = datetime.strptime(data2, '%d/%m/%Y').date()

    consultas = {
        'contratos' : lambda: consulta_contratos(conn, data2_att, data1_att),
        'fornecedores': lambda: consulta_fornecedores(conn, data2_att, data1_att),
        'compras_diretas': lambda: consulta_compras_diretas(conn, data2_att, data1_att),
        'outras_compras' : lambda: consulta_outras_compras(conn, data2_att, data1_att)
    
    }

    filtro = request.args.getlist('filtro') #capturando do javascript
    print(consultas['contratos'])
    df = ''

    print(f"Filtro clicado: {filtro}")
    resultado = {}
    data_frames = {}
    for item in filtro:
        resultado[item] = consultas[item]()
        conn.execute('')
    print('o resultado está aqui', resultado)
    print(type(resultado))

    


    
    return render_template('acompanhamento_siga.html', resultado = resultado, filtro = filtro, df = df)


@bp.route('/excel_download_acompanhamento_siga')
def excel_download_acompanhamento():
    filtros_selecionados = request.args.getlist('filtro')
    df = request.args.get('df')
    print(df)
    conn = get_db2()
    resultado = conn.execute('SELECT * FROM t1_contratos WHERE data_adicao_db = ?',  ).df()
    resultado['data_adicao_db'] = resultado['data_adicao_db'].astype(str) #mostrar a data no excel sem hora, minuto, segundo

    resultado_fornecedores = conn.execute('SELECT * FROM t1_fornecedores').df()
    resultado_fornecedores['data_adicao_db'] = resultado_fornecedores['data_adicao_db'].astype(str)
    print(resultado_fornecedores)
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine = 'openpyxl') as writer:
        resultado.to_excel(writer, index = False, sheet_name = 'Contratos')
        resultado_fornecedores.to_excel(writer, index = False, sheet_name = 'Fornecedores')
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name = 'teste.xlsx',
        mimetype='application/vnds.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@bp.route('/financeiro_siga', methods = ['POST', 'GET'])
def financeiro_siga():
    data_inicio = '01/01/2024'
    data_fim = '15/04/2025'
    data_inicio_att = datetime.strptime(data_inicio, '%d/%m/%Y').year
    data_fim_att = datetime.strptime(data_fim, '%d/%m/%Y').year
    termo = request.form.get('busca')
    if request.method == 'POST':
        buscar_pncp_termo(termo, data_inicio_att, data_fim_att)
        print(termo)
    return render_template('pncp.html')

@bp.route('/excel_download_pncp')
def excel_download_pncp():
    con = get_db2()

    resultado_df = con.execute("SELECT * FROM teste_pncp").df()
    print(resultado_df.info())
    
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine = 'openpyxl') as writer:
        resultado_df.to_excel(writer, index = False, sheet_name = 'Contratos-PNCP')
    buffer.seek(0)
    con.execute('TRUNCATE teste_pncp')
    return send_file(
        buffer,
        as_attachment=True,
        download_name='pncp-teste.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


