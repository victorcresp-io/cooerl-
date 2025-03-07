import sqlite3
from my_app import create_app
from my_app.db import get_db

app = create_app()




def alterando_banco(conn):
    cursor = conn.cursor()
    cursor.execute("VACUUM")
    conn.commit()

def teste_sqlite():
    with app.app_context():
        db = get_db()
        print('tudo ok', db)

        alterando_banco(db)


teste_sqlite()

