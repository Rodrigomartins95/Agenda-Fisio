def deletar_paciente(paciente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conn.commit()
    conn.close()

def editar_paciente(paciente_id, nome, telefone, observacoes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pacientes SET nome = ?, telefone = ?, observacoes = ? WHERE id = ?
    """, (nome, telefone, observacoes, paciente_id))
    conn.commit()
    conn.close()
import sqlite3
import bcrypt

# 🔧 Conexão com o banco
def conectar():
    return sqlite3.connect("agenda.db")

# 📝 Salvar novo usuário com senha segura
def salvar_usuario(email, senha):
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            senha BLOB
        )
    """)
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
def inserir_paciente(nome, telefone, observacoes, fisioterapeuta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pacientes (nome, telefone, observacoes, fisioterapeuta)
        VALUES (?, ?, ?, ?)
    """, (nome, telefone, observacoes, fisioterapeuta))
    conn.commit()
    conn.close()


# 📋 Listar pacientes
def listar_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, observacoes FROM pacientes ORDER BY nome")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# 🗓️ Inserir atendimento
def inserir_atendimento(nome, data, hora, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO atendimentos (nome, data, hora, tipo)
        VALUES (?, ?, ?, ?)
    """, (nome, data, hora, tipo))
    conn.commit()
    conn.close()

# 📅 Buscar atendimentos por semana (offset = 0 é semana atual)
def buscar_atendimentos_por_offset(offset):
    import sqlite3
    from datetime import date, timedelta

    conn = conectar()
    cursor = conn.cursor()

    # Calcular início e fim da semana com base no offset
    hoje = date.today()
    inicio_semana = hoje + timedelta(weeks=offset, days=-hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    cursor.execute("""
        SELECT nome, data, hora, tipo FROM atendimentos
        WHERE data BETWEEN ? AND ?
        ORDER BY data, hora
    """, (str(inicio_semana), str(fim_semana)))
    resultado = cursor.fetchall()

    conn.close()
    return resultado, str(inicio_semana), str(fim_semana)

# 📜 Histórico completo
def listar_historico():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, data, hora, tipo FROM atendimentos ORDER BY data DESC, hora DESC")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# 🧱 Inicializar banco com estrutura correta
def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de usuários com senha como BLOB
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            senha BLOB
        )
    """)
    # Adiciona coluna fisioterapeuta se não existir
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN fisioterapeuta TEXT")
    except sqlite3.OperationalError:
        pass  # coluna já existe


    # Tabela de atendimentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            data TEXT,
            hora TEXT,
            tipo TEXT
        )
    """)
    # fisioterapeuta responsavel
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            observacoes TEXT,
            fisioterapeuta TEXT
        )
    """)

    conn.commit()
    conn.close()

# ❌ Excluir atendimento
def excluir_atendimento(nome, data, hora):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM atendimentos
        WHERE nome = ? AND data = ? AND hora = ?
    """, (nome, data, hora))
    conn.commit()
    conn.close()
