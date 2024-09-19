import sqlite3

#cria duas tabelas: uma para os materiais e outra para registrar as movimentações de estoque.
def conectar():
    conn = sqlite3.connect('estoque.db')
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        unidade TEXT NOT NULL,
        estoque_minimo INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER,
        quantidade INTEGER,
        tipo TEXT,
        data TEXT,
        FOREIGN KEY(material_id) REFERENCES materiais(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
