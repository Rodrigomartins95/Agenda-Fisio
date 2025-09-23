import sqlite3

conn = sqlite3.connect("agenda.db")
cursor = conn.cursor()

# 🧱 Tabela de pacientes com ID
cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    observacoes TEXT
)
""")

# 🧱 Tabela de atendimentos com vínculo ao paciente
cursor.execute("""
CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    tipo TEXT,
    FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
)
""")

conn.commit()
conn.close()

print("✅ Banco de dados com vínculo por ID criado com sucesso!")