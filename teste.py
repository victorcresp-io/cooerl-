from my_app import create_app
from my_app.db import get_db
import pandas as pd
from datetime import datetime

app = create_app()

with app.app_context():

    conn = get_db()
    cursor = conn.cursor()
    data = '2025-3-7'
    data = datetime.strptime(data, '%Y-%m-%d').date()
    cursor.execute("SELECT DISTINCT(data_adicao) FROM contratos")
    for linha in cursor.fetchall():
        print(dict(linha))


