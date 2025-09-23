import streamlit as st
from db import inicializar_banco
from telas import tela_inicio  # Tela inicial
from telas import tela_login
from telas import tela_cadastro  # Cadastro de usuário
from telas import tela_agenda
from telas import tela_cadastro_paciente
from telas import tela_lista_pacientes


# 🔧 Inicializa banco
inicializar_banco()

# 🧭 Estado inicial
if "tela" not in st.session_state:
    st.session_state["tela"] = "inicio"

# 📌 Menu lateral (aparece só após login)
if "usuario_logado" in st.session_state:
    with st.sidebar:
        st.markdown("## Navegação")
        if st.button("🗓️ Agenda Semanal"):
            st.session_state["tela"] = "agenda"
            st.rerun()
        if st.button("📋 Lista de Pacientes"):
            st.session_state["tela"] = "lista"
            st.rerun()
        if st.button("➕ Cadastrar Paciente"):
            st.session_state["tela"] = "cadastro_paciente"
            st.rerun()
        if st.button("🚪 Sair"):
            st.session_state.clear()
            st.rerun()

# 🔄 Navegação entre telas
tela = st.session_state["tela"]

# Telas públicas
if tela == "inicio":
    tela_inicio()
elif tela == "login":
    tela_login()
elif tela == "cadastro":
    tela_cadastro()

# Telas protegidas (exigem login)
elif tela in ["agenda", "lista", "cadastro_paciente"]:
    if "usuario_logado" in st.session_state:
        if tela == "agenda":
            tela_agenda()
        elif tela == "lista":
            tela_lista_pacientes()
        elif tela == "cadastro_paciente":
            tela_cadastro_paciente()
    else:
        # Evita renderizar tela protegida sem login
        if st.button("🔐 Ir para Login"):
            st.session_state["tela"] = "login"
            st.rerun()
        elif st.button("⬅️ Voltar para Login"):
            st.session_state["tela"] = "login"
            st.rerun()