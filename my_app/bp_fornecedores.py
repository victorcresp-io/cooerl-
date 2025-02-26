from flask import Blueprint, request, send_file, render_template, flash, redirect, url_for
from my_app.db import get_db
from my_app.funcao_fornecedores import tratar_cnpj
import pandas as pd
from io import BytesIO

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
        cnpj_filtro = request.form.get('cnpj')
        cnpj_filtro = tratar_cnpj(cnpj_filtro)
        print(f'Empresa recebida: {empresa_filtro}')

        #Verificando se a empresa está na base FORNECEDORES.
        db = get_db()
        cursor = db.cursor()
        try: 

            cursor.execute('SELECT fornecedor, cpf_cnpj FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
            resultado = cursor.fetchone()

            if not resultado:
                flash('Empresa não encontrada', 'error')
                return redirect(url_for('siga.rota1'))
            
            empresa_db, cnpj_db = resultado


            if empresa_filtro and empresa_filtro != empresa_db:
                flash('Empresa fornecida não corresponde ao CNPJ informado', 'error')
                return redirect(url_for('siga.rota1'))
            
            if cnpj_filtro and cnpj_filtro != cnpj_db: 
                flash('CNPJ fornecido não corresponde a empresa informada', 'error')
                return redirect(url_for('siga.rota1'))
            
            if empresa_filtro and not cnpj_filtro:
                cursor.execute('SELECT fornecedor, situacao FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                resultado = cursor.fetchone()
                empresa_html, situacao = resultado
                cursor.execute('SELECT COUNT(*) FROM compras_diretas WHERE fornecedor_vencedor = ?', (empresa_filtro,))
                total_compras_diretas = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM outras_compras WHERE fornecedor_vencedor = ?', (empresa_filtro,))
                total_outras_compras = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM contratos WHERE fornecedor = ?', (empresa_filtro,))
                total_contratos = cursor.fetchone()[0]
                resumo = {
                    'empresa': empresa_html,
                    'situacao': situacao,
                    'total_contratos': total_contratos,
                    'total_compras_diretas': total_compras_diretas,
                    'total_outras_compras': total_outras_compras
                }


            else:
                cursor.execute('SELECT fornecedor, situacao FROM fornecedores WHERE fornecedor = ? OR cpf_cnpj = ?', (empresa_filtro, cnpj_filtro))
                resultado = cursor.fetchone()
                empresa_html, situacao = resultado
                cursor.execute('SELECT COUNT(*) FROM compras_diretas WHERE cpf_cnpj = ?', (cnpj_filtro,))
                total_compras_diretas = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM outras_compras WHERE cpf_cnpj = ?', (cnpj_filtro,))
                total_outras_compras = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM contratos WHERE cpf_cnpj = ?', (cnpj_filtro,))
                total_contratos = cursor.fetchone()[0]

                resumo = {
                    'empresa': empresa_html,
                    'situacao': situacao,
                    'total_contratos': total_contratos,
                    'total_compras_diretas': total_compras_diretas,
                    'total_outras_compras': total_outras_compras
                }
            

        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'error')
            return redirect(url_for('siga.rota1'))


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

    query_outras_compras = 'SELECT * FROM compras_diretas WHERE fornecedor_vencedor = ? OR cpf_cnpj = ?'




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
