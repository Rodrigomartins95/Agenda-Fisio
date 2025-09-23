import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()  # carrega o .env

# def enviar_email_confirmacao(email_destino, codigo):
#     mensagem = Mail(
#         from_email='noreply@agenda-fisio.com.br',
#         to_emails=email_destino,
#         subject='Confirmação de Cadastro',
#         html_content=f"""
#         <p>Olá!</p>
#         <p>Seu código de verificação é: <strong>{codigo}</strong></p>
#         <p>Digite esse código no sistema para concluir seu cadastro.</p>
#         """
#     )

#     try:
#         api_key = os.getenv("SENDGRID_API_KEY")
#         sg = SendGridAPIClient(api_key)
#         sg.send(mensagem)
#     except Exception as e:
#         print(f"Erro ao enviar e-mail: {e}")

def exigir_login():
    import streamlit as st
    if "usuario_logado" not in st.session_state:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        st.stop()