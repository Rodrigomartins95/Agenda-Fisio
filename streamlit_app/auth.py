import streamlit as st
import re, secrets, smtplib
from email.message import EmailMessage
from db import salvar_usuario, autenticar_usuario
from utils import enviar_email_confirmacao
from dotenv import load_dotenv
load_dotenv()



def tela_login():
    st.title("🔐 Login")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar_usuario(email, senha):
            st.session_state["logado"] = True
            st.success("✅ Login realizado!")
        else:
            st.error("❌ E-mail ou senha incorretos.")

    st.markdown("---")
    if st.button("📝 Cadastre-se"):
        st.session_state["tela"] = "cadastro"
        st.rerun()

def tela_cadastro():
    st.title("📝 Cadastro")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("E-mail inválido.")
        else:
            codigo = secrets.token_hex(3)
            st.session_state["codigo_verificacao"] = codigo
            st.session_state["email_temp"] = email
            st.session_state["senha_temp"] = senha
            enviar_email_confirmacao(email, codigo)
            st.success("Código enviado para seu e-mail.")
            st.session_state["tela"] = "verificar"
            st.rerun()

