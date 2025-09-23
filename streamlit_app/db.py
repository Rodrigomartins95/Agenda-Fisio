import sqlite3
import bcrypt
import os
from datetime import date, timedelta

# 🔧 Conexão com o banco
def conectar():
    caminho_db = os.path.join(os.path.dirname(__file__), "agenda.db")
    return sqlite3.connect(caminho_db)

# 🧱 Inicializar banco com estrutura correta
def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            senha BLOB,
            fisioterapeuta TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            observacoes TEXT,
            fisioterapeuta TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data TEXT,
            hora TEXT,
            tipo TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    """)

    conn.commit()
    conn.close()

# 📝 Salvar novo usuário com senha segura
def salvar_usuario(email, senha):
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha_hash))
    conn.commit()
    conn.close()

# 🔐 Autenticar usuário
def autenticar_usuario(email, senha_digitada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        senha_hash = resultado[0]
        return bcrypt.checkpw(senha_digitada.encode(), senha_hash)
    return False

# 👩‍⚕️ Inserir paciente
def inserir_paciente(nome, telefone, email, observacoes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pacientes (nome, telefone, email, observacoes)
        VALUES (?, ?, ?, ?)
    """, (nome, telefone, email, observacoes))
    conn.commit()
    paciente_id = cursor.lastrowid
    conn.close()
    return paciente_id

# 📋 Listar pacientes
def listar_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, telefone, observacoes
        FROM pacientes
        ORDER BY nome
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# 📅 Buscar atendimentos por paciente
def buscar_atendimentos_por_paciente(paciente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data, hora, tipo
        FROM atendimentos
        WHERE paciente_id = ?
        ORDER BY data, hora
    """, (paciente_id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# 📅 Buscar atendimentos por semana (offset = 0 é semana atual)
def buscar_atendimentos_por_offset(offset):
    conn = conectar()
    cursor = conn.cursor()

    hoje = date.today()
    inicio_semana = hoje + timedelta(weeks=offset, days=-hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    cursor.execute("""
        SELECT pacientes.nome, data, hora, tipo
        FROM atendimentos
        JOIN pacientes ON atendimentos.paciente_id = pacientes.id
        WHERE data BETWEEN ? AND ?
        ORDER BY data, hora
    """, (str(inicio_semana), str(fim_semana)))
    resultado = cursor.fetchall()
    conn.close()
    return resultado, str(inicio_semana), str(fim_semana)

# 🗓️ Inserir atendimento
def inserir_atendimento(paciente_id, data, hora, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO atendimentos (paciente_id, data, hora, tipo)
        VALUES (?, ?, ?, ?)
    """, (paciente_id, data, hora, tipo))
    conn.commit()
    conn.close()

# 📜 Histórico completo
def listar_historico():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pacientes.nome, atendimentos.data, atendimentos.hora, atendimentos.tipo
        FROM atendimentos
        JOIN pacientes ON atendimentos.paciente_id = pacientes.id
        ORDER BY atendimentos.data DESC, atendimentos.hora DESC
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# 📈 Evolução por paciente
def evolucao_por_paciente(paciente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data, tipo
        FROM atendimentos
        WHERE paciente_id = ?
        ORDER BY data
    """, (paciente_id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# ❌ Excluir atendimento
def excluir_atendimento(paciente_id, data, hora):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM atendimentos
        WHERE paciente_id = ? AND data = ? AND hora = ?
    """, (paciente_id, data, hora))
    conn.commit()
    conn.close()

# ❌ Excluir paciente e seus atendimentos
def excluir_paciente(paciente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atendimentos WHERE paciente_id = ?", (paciente_id,))
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conn.commit()
    conn.close()

# 🧹 Limpar atendimentos órfãos
def limpar_atendimentos_orfaos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM atendimentos
        WHERE paciente_id NOT IN (SELECT id FROM pacientes)
    """)
    conn.commit()
    conn.close()

# ✏️ Editar paciente
def editar_paciente(paciente_id, nome, telefone, observacoes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pacientes SET nome = ?, telefone = ?, observacoes = ? WHERE id = ?
    """, (nome, telefone, observacoes, paciente_id))
    conn.commit()
    conn.close()

# ❌ Deletar paciente (sem excluir atendimentos)
def deletar_paciente(paciente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conn.commit()
    conn.close()