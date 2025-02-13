from flask import Blueprint, request
from my_app.db import get_db

bp = Blueprint('modulo', __name__)

@bp.route('/rota1')
def rota1():
    if request.method == 'POST':
        empresa = request.form['empresa']
        cnpj = request.form['cnpj']
        db = get_db()
        error = None

#definindo a blueprint para consulta dos fornecedores.
            
    return "Esta é a rota 1 do Blueprint"

@bp.route('/rota2')
def rota2():
    return "Esta é a rota 2 do Blueprint"