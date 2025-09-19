import streamlit as st
from db import inserir_paciente

st.set_page_config(page_title="Cadastro de Pacientes", layout="centered")
st.title("👩‍⚕️ Cadastro de Pacientes")

# Campos do formulário
with st.form("form_cadastro"):
    nome = st.text_input("Nome do paciente")
    telefone = st.text_input("Telefone")
    observacoes = st.text_area("Observações")

    enviado = st.form_submit_button("Salvar")

    if enviado:
        if nome.strip():
            inserir_paciente(nome, telefone, observacoes)
            st.success("✅ Paciente salvo com sucesso!")
        else:
            st.error("⚠️ O campo nome é obrigatório.")