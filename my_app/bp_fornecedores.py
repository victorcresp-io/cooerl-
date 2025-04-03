from flask import Blueprint, request, send_file, render_template, flash, redirect, url_for, jsonify
from my_app.db import get_db, get_db2
from my_app.funcao_buscadb import buscar_compras, ultima_compra_direta, ultima_compra_outra, buscar_compras_cnpj, ultima_compra_direta_cnpj, ultima_compra_outra_cnpj, comparar_data, consulta_contratos, consulta_fornecedores
from my_app.funcao_fornecedores import tratar_cnpj, tratar_empresa
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
        data = '22/03/2025'
        data = datetime.strptime(data, '%d/%m/%Y').date()
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


                
            return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_db, cnpj_filtro = cnpj_db)
        except Exception as e:
            print('Aconteceu o seguinte erro:', e)


    


    return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_db, cnpj_filtro = cnpj_db)


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
    print(empresa)
    cnpj = request.args.get('cnpj_filtro')
    data = datetime.now().date()
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
    data1 = '28/03/2025'
    data2 = '01/04/2025'

    data1_att = datetime.strptime(data1, '%d/%m/%Y').date()
    data2_att = datetime.strptime(data2, '%d/%m/%Y').date()

    consultas = {
        'contratos' : lambda: consulta_contratos(conn, data2_att, data1_att),
        'fornecedores': lambda: consulta_fornecedores(conn, data2_att, data1_att)
    }

    filtro = request.args.getlist('filtro')
    print(consultas['contratos'])

    print(f"Filtro clicado: {filtro}")
    resultado = {}
    for item in filtro:
        if item in consultas:
            print(consultas[item])
            consulta_sql = consultas[item]
            print(consulta_sql)
            print('Iniciando pelo comando de ', item)
            try: 
                resultado[item] = consultas[item]()
                
            except Exception as e:
                print(f'Erro ao executar consulta para {item}: {e}')
    print(resultado)
    return render_template('acompanhamento_siga.html', resultado = resultado)

@bp.route('/financeiro_siga')
def financeiro_siga():
    return 'td ok'


