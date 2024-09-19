import sqlite3
from datetime import datetime
import os

# Definir o caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "estoque.db")

def conectar():
    conn = sqlite3.connect(db_path)
    return conn
    # Criação da tabela materiais se não existir
   

# Função para criar as tabelas necessárias
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Criação da tabela de materiais
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        unidade TEXT NOT NULL,
        estoque_minimo INTEGER NOT NULL
    )
    ''')

    # Criação da tabela de movimentações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY(material_id) REFERENCES materiais(id)
    )
    ''')

    conn.commit()
    conn.close()

# Função para adicionar um material ao banco de dados
def adicionar_material(nome, quantidade, unidade, estoque_minimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO materiais (nome, quantidade, unidade, estoque_minimo) VALUES (?, ?, ?, ?)",
        (nome, quantidade, unidade, estoque_minimo)
    )
    conn.commit()
    conn.close()

# Função para registrar movimentação de estoque
def registrar_movimentacao(material_id, quantidade, tipo):
    conn = conectar()
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO movimentacoes (material_id, quantidade, tipo, data) VALUES (?, ?, ?, ?)",
        (material_id, quantidade, tipo, data_atual)
    )
    # Atualiza a quantidade de material no estoque
    cursor.execute(
        "UPDATE materiais SET quantidade = quantidade + ? WHERE id = ?",
        (quantidade if tipo == 'Entrada' else -quantidade, material_id)
    )
    conn.commit()
    conn.close()

# Função para obter todos os materiais
def obter_materiais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materiais")
    materiais = cursor.fetchall()
    conn.close()
    return materiais

# Função para obter movimentações
def obter_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movimentacoes")
    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes

# Função para editar um material
def editar_material(material_id, nome, quantidade, unidade, estoque_minimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE materiais SET nome = ?, quantidade = ?, unidade = ?, estoque_minimo = ? WHERE id = ?",
        (nome, quantidade, unidade, estoque_minimo, material_id)
    )
    conn.commit()
    conn.close()

# Função para deletar um material
def deletar_material(material_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materiais WHERE id = ?", (material_id,))
    cursor.execute("DELETE FROM movimentacoes WHERE material_id = ?", (material_id,))
    conn.commit()
    conn.close()

# Função para deletar uma movimentação específica
def deletar_movimentacao(movimentacao_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimentacoes WHERE id = ?", (movimentacao_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
