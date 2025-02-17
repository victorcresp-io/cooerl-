from flask import Blueprint, request, send_file, render_template, session, redirect, url_for
from my_app.db import get_db
from my_app.funcao_fornecedores import tratar_cnpj
import pandas as pd
from io import BytesIO

bp = Blueprint('siga', __name__)

@bp.route('/rota1', methods = ['GET', 'POST'])
def rota1():
    resultado = None
    if request.method == 'POST':
        empresa = request.form.get('empresa')
        cnpj = request.form.get('cnpj')
        cnpj = tratar_cnpj(cnpj)
        db = get_db()

        print(f'Empresa recebida: {cnpj}')

        error = None
        if not empresa and not cnpj:
            error = 'É preciso preencher pelo menos um campo.'

        if error is None:
                if cnpj:
                     cursor = db.execute(
                     'SELECT * FROM fornecedores WHERE cpf_cnpj = ?',(
                          cnpj,));
                     dados =  cursor.fetchall()
                     print(f'dados encontrados: {dados}')
                     resultado = [dict(row) for row in dados]
                     print(resultado)
                     colunas = [desc[0] for desc in cursor.description]
                     df = pd.DataFrame(dados, columns=colunas)
                     session['df'] = df.to_dict(orient='records')
                     print(df)
                else:
                    cursor = db.execute(
                    'SELECT * FROM  fornecedores WHERE fornecedor = ?',(
                        empresa,));
                    dados = cursor.fetchall()
                    print(f'dados encontrados: {dados}')
                    resultado = [dict(row) for row in dados]
                    print(resultado)
                    colunas = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(dados, columns=colunas)
                    session['df'] = df.to_dict(orient='records')
                    print(df)



        if resultado:
             return redirect(url_for('siga.rota2'))
    return render_template('fornecedores.html', resultado = resultado)

@bp.route('/rota2')

def rota2():
    return render_template('rota2.html')

@bp.route('/excel_download')
def excel():
     df = session.get('df')
     if not df:
          return 'nenhum dado encontrado'
     
     df = pd.DataFrame(df)
     buffer = BytesIO()

     with pd.ExcelWriter(buffer, engine = 'xlsxwriter') as writer:
          df.to_excel(writer, index = False, sheet_name = 'Fornecedores')


     buffer.seek(0)

     return send_file(
          buffer,
          as_attachment=True,
          download_name = 'fornecedores.xlsx',
          mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          )