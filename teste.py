from my_app import create_app
from my_app.db import get_db
import pandas as pd
from datetime import datetime

app = create_app()

with app.app_context():
    data = datetime.now().date()
    conn = get_db()
    cursor = conn.cursor()
    cpf_cnpj = None
    empresa = 'BDM SERVICOS EM ORGANIZACAO ADMINISTRATIVA E INFORMATICA LTDA - ME'
    data = datetime.now().date()
    cursor.execute('VACUUM')
    conn.commit()

    print('td ok')

