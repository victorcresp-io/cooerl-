from flask import Blueprint, request, send_file, render_template, flash, redirect, url_for
from my_app.db import get_db
from my_app.funcao_fornecedores import tratar_cnpj, tratar_empresa
import pandas as pd
from io import BytesIO

import time

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
        try: 
            cursor.execute('SELECT fornecedor, cpf_cnpj FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
            resultado = cursor.fetchone()
            

            if not resultado:
                flash('Empresa não encontrada', 'error')
                return redirect(url_for('siga.rota1'))
            
            empresa_db, cnpj_db = resultado  #Empresa no banco de dados.
            print('Empresa recebida', empresa_db)
            print('CNPJ RECEBIDO', cnpj_db)
 
            if empresa_filtro == empresa_db or cnpj_filtro == cnpj_db:
                cursor.execute('SELECT fornecedor, situacao FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_db, cnpj_db))
                resultado = cursor.fetchone()
                empresa_html, situacao = resultado
                print(empresa_html)
                print(situacao)
                cursor.execute('SELECT COUNT(cpf_cnpj)  FROM compras_diretas WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?', (empresa_db, cnpj_db))
                teste  = cursor.fetchone()
                total_compras_diretas = teste[0] 
                print('TD OK')
                cursor.execute('SELECT COUNT(cpf_cnpj) FROM outras_compras WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?', (empresa_db, cnpj_db))
                resultado = cursor.fetchone()
                total_outras_compras = resultado[0]
                print('aqui passou tbm')
                cursor.execute('SELECT COUNT(cpf_cnpj) FROM contratos WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_db, cnpj_db))
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
                
                return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_db, cnpj_filtro = cnpj_db)
            else:
                flash('Empresa fornecida não corresponde ao CNPJ informado', 'error')
                return redirect(url_for('siga.rota1'))
        except Exception as e:
            print('Aconteceu o seguinte erro:', e)


            '''if empresa_filtro == empresa_db or cnpj_filtro == cnpj_db:
                cursor.execute('SELECT fornecedor, situacao FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                resultado = cursor.fetchone()
                empresa_html, situacao = resultado
                cursor.execute('SELECT COUNT(cpf_cnpj) FROM compras_diretas WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                total_compras_diretas = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(cpf_cnpj), situacao FROM outras_compras WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                total_outras_compras = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(cpf_cnpj), situacao FROM contratos WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                total_contratos = cursor.fetchone()[0]
                resumo = {
                    'empresa': empresa_html,
                    'situacao': situacao,
                    'total_contratos': total_contratos,
                    'total_compras_diretas': total_compras_diretas,
                    'total_outras_compras': total_outras_compras
                }
            else:
                flash('Empresa fornecida não corresponde ao CNPJ informado', 'error')
                return redirect(url_for('siga.rota1'))
            
            elif cnpj_filtro != cnpj_db: 
                flash('CNPJ fornecido não corresponde a empresa informada', 'error')
                return redirect(url_for('siga.rota1'))
            
            start_time = time.time()


            if empresa_filtro or cnpj_filtro:
                cursor.execute('SELECT fornecedor, situacao FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                resultado = cursor.fetchone()
                empresa_html, situacao = resultado
                cursor.execute('SELECT COUNT(cpf_cnpj) FROM compras_diretas WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                total_compras_diretas = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(cpf_cnpj), situacao FROM outras_compras WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                total_outras_compras = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(cpf_cnpj), situacao FROM contratos WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                total_contratos = cursor.fetchone()[0]
                resumo = {
                    'empresa': empresa_html,
                    'situacao': situacao,
                    'total_contratos': total_contratos,
                    'total_compras_diretas': total_compras_diretas,
                    'total_outras_compras': total_outras_compras
                }
            
            end_time = time.time()
            execution_time = end_time - start_time
            print(f'Tempo de execução: {execution_time} segundos')

        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'error')
            return redirect(url_for('siga.rota1'))'''


    return render_template('fornecedores.html', resumo = resumo, empresa_filtro = empresa_filtro, cnpj_filtro = cnpj_filtro)


@bp.route('/excel_download')
def excel_download():
    """ Rota para gerar o arquivo Excel diretamente do banco """
    empresa = request.args.get('empresa_filtro')
    cnpj = request.args.get('cnpj_filtro')
    print(empresa)
    print(cnpj)

    db = get_db()
    cursor = db.cursor()


    query_fornecedores = 'SELECT * FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?'

    query_contratos = 'SELECT * FROM contratos WHERE fornecedor = ? OR cpf_cnpj = ?'

    query_compras_diretas = 'SELECT * FROM compras_diretas WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?'

    query_outras_compras = 'SELECT * FROM outras_compras WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?'




    # Consultar dados diretamente do banco
    df_fornecedores = pd.read_sql_query(query_fornecedores, db, params = (empresa, cnpj))
    df_contratos = pd.read_sql_query(query_contratos, db, params = (empresa, cnpj))
    df_compras_diretas = pd.read_sql_query(query_compras_diretas, db, params = (empresa, cnpj))
    df_outras_compras = pd.read_sql_query(query_outras_compras, db, params = (empresa, cnpj))


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
