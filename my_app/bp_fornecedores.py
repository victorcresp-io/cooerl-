from flask import Blueprint, request, send_file, render_template, flash, redirect, url_for, jsonify
from my_app.db import get_db
from my_app.funcao_fornecedores import tratar_cnpj, tratar_empresa
import pandas as pd
from io import BytesIO
from sqlalchemy import text
import time
from datetime import datetime




bp = Blueprint('siga', __name__)

@bp.route('/')
def rota():
    return 'oi'

@bp.route('/rota1', methods=['GET', 'POST'])
def rota1():
    resumo = None
    empresa_html = None
    situacao = None
    empresa_filtro = None
    cnpj_filtro = None



    """ Rota para processar a requisição e redirecionar para o download """
    if request.method == 'POST':
        empresa_filtro = request.form.get('empresa')
        empresa_filtro = tratar_empresa(empresa_filtro)
        cnpj_filtro = request.form.get('cnpj')
        cnpj_filtro = tratar_cnpj(cnpj_filtro)
        print(f'Empresa recebida: {empresa_filtro}')
        print(f'CNPJ recebido {cnpj_filtro}')

        #Verificando se a empresa está na base FORNECEDORES.
        db = get_db()
        cursor = db.cursor()
        print('aqui deu certo')
        data_obj = datetime.now().date()
        print(data_obj)
        try: 
            cursor.execute('SELECT fornecedor, cpf_cnpj FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
            resultado = cursor.fetchone()

            if not resultado:
                flash('Empresa não encontrada', 'error')
                return redirect(url_for('siga.rota1'))
            
            empresa_db, cnpj_db = resultado  #Empresa no banco de dados.
            print('Empresa recebida', empresa_db)
            print('CNPJ RECEBIDO', cnpj_db)


            inicio = time.time()

            cursor.execute('SELECT fornecedor, situacao FROM fornecedores WHERE cpf_cnpj = ? AND data_adicao = ?', (cnpj_db, data_obj))
            resultado = cursor.fetchone()
            empresa_html, situacao = resultado
            print(empresa_html)
            print(situacao)
            cursor.execute('SELECT COUNT(*) FROM compras_diretas WHERE cpf_cnpj = ? AND data_adicao = ?', 
            (cnpj_db, data_obj))
            teste  = cursor.fetchone()
            total_compras_diretas = teste[0]
            print('Compras_diretas passou')
            cursor.execute('SELECT COUNT(*) FROM outras_compras WHERE cpf_cnpj = ? AND data_adicao = ?', (cnpj_db, data_obj))
            resultado = cursor.fetchone()
            total_outras_compras = resultado[0]
            print('Outras_compras passou')
            cursor.execute('SELECT COUNT(*) FROM contratos WHERE cpf_cnpj = ? AND  data_adicao = ?', (cnpj_db, data_obj))
            resultado = cursor.fetchone()
            total_contratos = resultado[0]
            
            print('aqui tbm ok')
            resumo = {
                    'empresa': empresa_html,
                    'situacao': situacao,
                    'total_contratos': total_contratos,
                    'total_compras_diretas': total_compras_diretas,
                    'total_outras_compras': total_outras_compras
                }
            print('oi')
            fim = time.time()
            tempo_gasto = fim - inicio
            print(f'Tempo gasto: {tempo_gasto:.6f} segundos')

                
            return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_db, cnpj_filtro = cnpj_db)
        except Exception as e:
            print('Aconteceu o seguinte erro:', e)


    


    return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_filtro, cnpj_filtro = cnpj_filtro)


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
    #empresa = request.args.get('empresa_filtro')
    cnpj = request.args.get('cnpj_filtro')
    data = datetime.now().date()
    #print(empresa)
    print(cnpj)

    db = get_db()
    cursor = db.cursor()


    query_fornecedores = 'SELECT * FROM fornecedores WHERE data_adicao = ? AND cpf_cnpj = ?'

    query_contratos = 'SELECT * FROM contratos WHERE data_adicao = ? AND cpf_cnpj = ?'

    query_compras_diretas = 'SELECT * FROM compras_diretas WHERE data_adicao = ? AND cpf_cnpj = ?'

    query_outras_compras = 'SELECT * FROM outras_compras WHERE data_adicao = ? AND cpf_cnpj = ?'




    # Consultar dados diretamente do banco
    df_fornecedores = pd.read_sql_query(query_fornecedores, db, params = (data, cnpj))
    df_contratos = pd.read_sql_query(query_contratos, db, params = (data, cnpj))
    df_compras_diretas = pd.read_sql_query(query_compras_diretas, db, params = (data, cnpj))
    df_outras_compras = pd.read_sql_query(query_outras_compras, db, params = (data, cnpj))


    if df_fornecedores.empty:
        flash('Verifique o nome da empresa')
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
        download_name='dados.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
