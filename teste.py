from my_app import create_app
from my_app.db import get_db
import pandas as pd


app = create_app()

with app.app_context():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(data_adicao) FROM compras_diretas')
    max_data_adicao = cursor.fetchone()[0]
    cnpj_db = '04050750000129'
    res = cursor.execute('SELECT COUNT(cpf_cnpj) FROM contratos WHERE cpf_cnpj = ? AND data_adicao = ?', (cnpj_db, max_data_adicao))
    show = res.fetchall()
    for row in show:
        print(dict(row))