import sqlite3
from . import create_app
from my_app.db import get_db

app = create_app()


def teste_sqlite():
    with app.app_context():
        db = get_db()
        print('tudo ok', db)


teste_sqlite()