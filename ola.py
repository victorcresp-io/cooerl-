import sqlite3


conn = sqlite3.connect('teste.db')

cursor = conn.cursor()



cursor.execute("""INSERT INTO testando2 VALUES
               ('2020-01-01'),
               ('2021-01-02'),
               ('2022-02-01'),
               ('2021-02-02'),
               ('2024-01-03')""")

conn.commit()

cursor.execute("SELECT data FROM testando2 ORDER BY data DESC")
resultado = cursor.fetchall()

for item in resultado:
    print(item)
