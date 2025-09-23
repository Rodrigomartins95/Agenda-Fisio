import streamlit as st
import sqlite3
import bcrypt
from db import inicializar_banco
from ..auth_utils import (
    gerar_token,
    validar_token,
    salvar_token_local,
    carregar_token_local,
    limpar_token_local
)

def tela_login():
    # Inicializa o banco de dados
    inicializar_banco()

    # 🔁 Verifica se já existe token salvo e válido
    token = carregar_token_local()
    if token:
        email, fisio = validar_token(token)
        if email and fisio:
            st.session_state["usuario_logado"] = email
            st.session_state["fisioterapeuta"] = fisio
            st.session_state["token"] = token
            st.session_state["tela"] = "agenda"
            st.success(f"🔓 Sessão restaurada para {email}")
            return

    # Título da página
    st.title("🔐 Login")

    # Campos de entrada
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")

    # Função para autenticar usuário e gerar token
    def autenticar_usuario(email, senha_digitada):
        conn = sqlite3.connect("agenda.db")
        cursor = conn.cursor()
        cursor.execute("SELECT senha, fisioterapeuta FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            senha_hash, fisioterapeuta = resultado
            if bcrypt.checkpw(senha_digitada.encode(), senha_hash):
                token = gerar_token(email, fisioterapeuta)
                salvar_token_local(token)
                st.session_state["usuario_logado"] = email
                st.session_state["fisioterapeuta"] = fisioterapeuta
                st.session_state["token"] = token
                return True
        return False

    # Botões de ação
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Entrar"):
            if autenticar_usuario(email, senha):
                st.success("✅ Login realizado com sucesso!")
                st.session_state["tela"] = "agenda"
                st.rerun()
            else:
                st.error("❌ Email ou senha inválidos.")
    with col2:
        if st.button("⬅️ Voltar"):
            st.session_state["tela"] = "inicio"
            st.rerun()

    # 🚪 Botão de logout (opcional, se já estiver logado)
    if "usuario_logado" in st.session_state:
        if st.button("Sair"):
            limpar_token_local()
            st.session_state.clear()
            st.rerun()