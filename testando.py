import sqlite3
from datetime import datetime

tempo = datetime.now()

conn = sqlite3.connect('bancoteste.db')

cursor = conn.cursor()






'''res = cursor.execute("INSERT INTO teste ('date') VALUES (?)", (tempo,))
conn.commit()'''

res = cursor.execute("SELECT * FROM teste WHERE date = '2025-03-07 10:52:36.477708'")
show = res.fetchall()

print(show)


'''res = cursor.execute("SELECT name FROM sqlite_master")
show = res.fetchone()
print(show)'''
'''cursor.execute("""
        INSERT INTO teste VALUES
               ('Victor', 12)
""")

conn.commit()'''


'''cursor.execute('ALTER TABLE teste ADD COLUMN date TEXT')
conn.commit()'''

'''res = cursor.execute("SELECT *  FROM pragma_table_info('teste')")
show = res.fetchall()
print(show)'''

'''res = cursor.execute("SELECT nome FROM teste")
show = cursor.fetchone()'''


'''meu_nome = 'Victor'
age = 12

res = cursor.execute("SELECT COUNT(nome) FROM teste WHERE nome = ? OR idade = ?", (meu_nome, age))
show = cursor.fetchone()
print(show)'''

