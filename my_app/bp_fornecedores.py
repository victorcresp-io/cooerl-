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
    """ Rota para processar a requisição e redirecionar para o download """
    if request.method == 'POST':
        empresa = request.form.get('empresa')
        cnpj = request.form.get('cnpj')
        cnpj = tratar_cnpj(cnpj)
        print(f'Empresa recebida: {empresa}')

        #Verificando se a empresa está na base FORNECEDORES.
        db = get_db()
        cursor = db.cursor()
        try: 
            cursor.execute('SELECT COUNT(*) FROM fornecedores WHERE fornecedor == ?', (empresa,))
            resultado = cursor.fetchone()
            if resultado[0] == 0:
                flash('Empresa nao encontrada', 'error')
                return redirect(url_for('siga.rota1'))
        except Exception as e: 
            flash(f'Ocorreu um erro: {str(e)}', 'error')
            return render_template('siga.rota1')
        
        if not empresa and not cnpj:
            flash('preencha', 'error')
            return render_template('fornecedores.html', error="É preciso preencher pelo menos um campo.")

        # Armazenamos apenas os filtros na URL para buscar os dados no download
        if cnpj:
            return render_template('rota2.html', filtro=cnpj, tipo='cnpj')
        else:
            return render_template('rota2.html', filtro=empresa, tipo='empresa')

    return render_template('fornecedores.html')


@bp.route('/excel_download')
def excel_download():
    """ Rota para gerar o arquivo Excel diretamente do banco """
    filtro = request.args.get('filtro')
    tipo = request.args.get('tipo')

    if not filtro or not tipo:
        return "Erro: Falta de parâmetros", 400

    db = get_db()

    if tipo == 'cnpj':
        query_fornecedores = 'SELECT * FROM fornecedores WHERE cpf_cnpj = ?'
        query_contratos = 'SELECT * FROM contratos WHERE cpf_cnpj = ?'
        query_compras = 'SELECT * FROM compras_diretas WHERE cpf_cnpj = ?'
    else:
        query_fornecedores = 'SELECT * FROM fornecedores WHERE fornecedor = ?'
        query_contratos = 'SELECT * FROM contratos WHERE fornecedor = ?'
        query_compras = 'SELECT * FROM compras_diretas WHERE fornecedor_vencedor = ?'

    # Consultar dados diretamente do banco
    df_fornecedores = pd.read_sql_query(query_fornecedores, db, params=(filtro,))
    df_contratos = pd.read_sql_query(query_contratos, db, params=(filtro,))
    df_compras_diretas = pd.read_sql_query(query_compras, db, params = (filtro,))
    print(df_contratos)

    if df_fornecedores.empty:
        flash('Verifique o nome da empresa')
    # Criar o arquivo Excel na memória
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_fornecedores.to_excel(writer, index=False, sheet_name='Fornecedores')
        df_contratos.to_excel(writer, index=False, sheet_name='Contratos')
        df_compras_diretas.to_excel(writer, index = False, sheet_name = 'Compras Diretas')
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='dados.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
