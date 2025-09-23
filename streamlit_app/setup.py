# streamlit_app/setup.py
import os
from db import inicializar_banco

def verificar_banco():
    caminho_db = os.path.join(os.path.dirname(__file__), "agenda.db")
    if not os.path.exists(caminho_db):
        print("🔧 Banco não encontrado. Inicializando...")
        inicializar_banco()
    else:
        print("✅ Banco já existe. Tudo certo!")

verificar_banco()