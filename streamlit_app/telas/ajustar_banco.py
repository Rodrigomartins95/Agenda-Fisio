import sqlite3

conn = sqlite3.connect("agenda.db")
cursor = conn.cursor()
cursor.execute("ALTER TABLE atendimentos ADD COLUMN paciente_id INTEGER")
conn.commit()
conn.close()

print("✅ Coluna paciente_id adicionada com sucesso.")