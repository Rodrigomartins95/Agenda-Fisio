import sqlite3
from datetime import datetime, timedelta

def conectar():
    return sqlite3.connect("agenda.db")

def criar_tabela_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            observacoes TEXT
        )
    """)
    conn.commit()
    conn.close()

def criar_tabela_atendimentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data TEXT,
            hora TEXT,
            tipo TEXT,
            anotacoes TEXT,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        )
    """)
    conn.commit()
    conn.close()

def buscar_atendimentos_por_paciente(paciente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data, hora, tipo, anotacoes
        FROM atendimentos
        WHERE paciente_id = ?
        ORDER BY data DESC, hora DESC
    """, (paciente_id,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_atendimentos_do_dia():
    hoje = datetime.now().strftime("%Y-%m-%d")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pacientes.nome, atendimentos.hora, atendimentos.tipo
        FROM atendimentos
        JOIN pacientes ON pacientes.id = atendimentos.paciente_id
        WHERE atendimentos.data = ?
        ORDER BY atendimentos.hora ASC
    """, (hoje,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_atendimentos_por_offset(offset=0):
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday()) + timedelta(weeks=offset)
    fim_semana = inicio_semana + timedelta(days=6)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pacientes.nome, atendimentos.data, atendimentos.hora, atendimentos.tipo
        FROM atendimentos
        JOIN pacientes ON pacientes.id = atendimentos.paciente_id
        WHERE atendimentos.data BETWEEN ? AND ?
        ORDER BY atendimentos.data ASC, atendimentos.hora ASC
    """, (inicio_semana.strftime("%Y-%m-%d"), fim_semana.strftime("%Y-%m-%d")))
    resultados = cursor.fetchall()
    conn.close()
    return resultados, inicio_semana.strftime("%d/%m"), fim_semana.strftime("%d/%m")

def atualizar_atendimento(atendimento_id, data, hora, tipo, anotacoes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE atendimentos
        SET data = ?, hora = ?, tipo = ?, anotacoes = ?
        WHERE id = ?
    """, (data, hora, tipo, anotacoes, atendimento_id))
    conn.commit()
    conn.close()

def buscar_nomes_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM pacientes ORDER BY nome ASC")
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def criar_tabela():
    criar_tabela_pacientes()
    criar_tabela_atendimentos()

def inserir_paciente(nome, telefone, observacoes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (nome, telefone, observacoes) VALUES (?, ?, ?)",
                   (nome, telefone, observacoes))
    conn.commit()
    conn.close()