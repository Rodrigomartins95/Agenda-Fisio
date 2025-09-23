import streamlit as st

# 🔧 Banco e setup
from db import inicializar_banco
from setup import verificar_banco

# 🧭 Telas
from telas import (
    tela_inicio,
    tela_login,
    tela_cadastro,
    tela_agenda,
    tela_cadastro_paciente,
    tela_lista_pacientes,
    tela_historico,
    tela_paciente
)

# ✅ Inicialização
verificar_banco()
inicializar_banco()

# 🔁 Estado inicial
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
        if st.button("📁 Histórico"):
            st.session_state["tela"] = "lista_historico"
            st.rerun()
        if st.button("👤 Paciente"):
            st.session_state["tela"] = "tela_paciente"
            st.rerun()
        if st.button("🚪 Sair"):
            # 🔒 Removido uso de auth_utils
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

# Telas protegidas
elif tela == "agenda":
    if "usuario_logado" in st.session_state:
        tela_agenda()
    else:
        st.warning("🔐 Você precisa estar logado para acessar a agenda.")
        if st.button("Ir para Login"):
            st.session_state["tela"] = "login"
            st.rerun()

elif tela == "lista":
    if "usuario_logado" in st.session_state:
        tela_lista_pacientes()
    else:
        st.warning("🔐 Você precisa estar logado para acessar a lista.")
        if st.button("Ir para Login"):
            st.session_state["tela"] = "login"
            st.rerun()

elif tela == "cadastro_paciente":
    if "usuario_logado" in st.session_state:
        tela_cadastro_paciente()
    else:
        st.warning("🔐 Você precisa estar logado para cadastrar pacientes.")
        if st.button("Ir para Login"):
            st.session_state["tela"] = "login"
            st.rerun()

elif tela == "lista_historico":
    if "usuario_logado" in st.session_state:
        tela_historico()
    else:
        st.warning("🔐 Você precisa estar logado para ver o histórico.")
        if st.button("Ir para Login"):
            st.session_state["tela"] = "login"
            st.rerun()

elif tela == "tela_paciente":
    if "usuario_logado" in st.session_state:
        tela_paciente()
    else:
        st.warning("🔐 Você precisa estar logado para acessar o paciente.")
        if st.button("Ir para Login"):
            st.session_state["tela"] = "login"
            st.rerun()

# 🔚 Fallback
else:
    st.error("❌ Tela não reconhecida.")
    st.session_state["tela"] = "inicio"
    st.rerun()