import sqlite3

def init_db():
    conn = sqlite3.connect('comercio.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chamada direta ao rodar
if __name__ == '__main__':
    init_db()
