
from PIL import Image
import streamlit as st
import os

def tela_inicio():
    st.set_page_config(page_title="Bem-vindo", layout="centered")
    st.markdown("# 👩‍⚕️ Bem-vindo ao Agendador Fisio")
    img_path = os.path.join(os.path.dirname(__file__), "..", "assets", "capa_clinica.png")
    img_path = os.path.abspath(img_path)
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((400, 250))  # largura x altura (pixels)
        st.image(img)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            st.session_state["tela"] = "login"
            st.rerun()
    with col2:
        if st.button("📝 Cadastro"):
            st.session_state["tela"] = "cadastro"
            st.rerun()
