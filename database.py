import sqlite3

def get_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            concluido INTEGER DEFAULT 0,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

def buscar_usuario_por_email(email):
    conn = get_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
    conn.close()
    return usuario

def criar_usuario(nome, email, senha):
    conn = get_connection()
    conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
    conn.commit()
    conn.close()

def listar_treinos_por_usuario(usuario_id):
    conn = get_connection()
    treinos = conn.execute('SELECT * FROM treinos WHERE usuario_id = ?', (usuario_id,)).fetchall()
    conn.close()
    return treinos

def buscar_treino_por_id(id):
    conn = get_connection()
    treino = conn.execute('SELECT * FROM treinos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return treino

def criar_treino(titulo, descricao, usuario_id):
    conn = get_connection()
    conn.execute('INSERT INTO treinos (titulo, descricao, usuario_id) VALUES (?, ?, ?)', (titulo, descricao, usuario_id))
    conn.commit()
    conn.close()

def atualizar_treino(id, titulo, descricao):
    conn = get_connection()
    conn.execute('UPDATE treinos SET titulo = ?, descricao = ? WHERE id = ?', (id, titulo, descricao))
    conn.commit()
    conn.close()

def marcar_concluido(id):
    conn = get_connection()
    conn.execute('UPDATE treinos SET concluido = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def deletar_treino(id):
    conn = get_connection()
    conn.execute('DELETE FROM treinos WHERE id = ?', (id,))
    conn.commit()
    conn.close()