import sqlite3

conn = sqlite3.connect("agenda.db")
cursor = conn.cursor()

# Tabela de pacientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    observacoes TEXT
)
""")

# Tabela de atendimentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    tipo TEXT
)
""")

conn.commit()
conn.close()

print("✅ Banco de dados inicializado com sucesso!")