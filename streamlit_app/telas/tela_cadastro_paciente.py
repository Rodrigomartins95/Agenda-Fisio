import streamlit as st
from db import inserir_paciente, inserir_atendimento
import datetime

def tela_cadastro_paciente():
    st.title("👤 Cadastro de Paciente")

    # Inicializa estado
    if "paciente_salvo" not in st.session_state:
        st.session_state.paciente_salvo = False

    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    observacoes = st.text_area("Observações")

    dias_semana = st.multiselect("Dias da semana para atendimento", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])
    semanas = st.slider("Número de semanas", 1, 12, 4)
    hora = st.time_input("Horário do atendimento", value=datetime.time(9, 0))

    tipo = st.selectbox("Tipo de atendimento", ["Sessão", "Consulta", "Retorno"])

    if st.button("Salvar paciente"):
        paciente_id = inserir_paciente(nome, telefone, email, observacoes)

        hoje = datetime.date.today()
        dias_map = {
            "Segunda": 0, "Terça": 1, "Quarta": 2,
            "Quinta": 3, "Sexta": 4
        }

        for semana in range(semanas):
            for dia in dias_semana:
                delta_dias = dias_map[dia] - hoje.weekday() + (semana * 7)
                data_atendimento = hoje + datetime.timedelta(days=delta_dias)
                if data_atendimento >= hoje:
                    inserir_atendimento(paciente_id, str(data_atendimento), str(hora), tipo)

        st.success("✅ Paciente cadastrado com atendimentos agendados!")
