import pandas as pd
import altair as alt
import streamlit as st
from db import (
    listar_pacientes,
    buscar_atendimentos_por_paciente,
    excluir_paciente,
    evolucao_por_paciente  # ✅ Importação adicionada
)

def tela_paciente():
    if "usuario_logado" not in st.session_state:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        st.stop()

    st.set_page_config(page_title="👤 Perfil do Paciente", layout="wide")
    st.title("👤 Perfil do Paciente")

    pacientes = listar_pacientes()
    if not pacientes:
        st.info("Nenhum paciente cadastrado ainda.")
        return

    nomes = [p[1] for p in pacientes]  # p[1] = nome
    nome_selecionado = st.selectbox("Selecione um paciente", nomes)

    paciente = next(p for p in pacientes if p[1] == nome_selecionado)
    paciente_id = paciente[0]

    st.markdown("### 📇 Dados do paciente")
    st.write(f"**Nome:** {paciente[1]}")
    st.write(f"**Telefone:** {paciente[2]}")
    st.write(f"**Email:** {paciente[3]}")
    st.write(f"**Observações:** {paciente[4]}")

    atendimentos = buscar_atendimentos_por_paciente(paciente_id)
    st.markdown("### 📋 Atendimentos agendados")

    if atendimentos:
        df_atendimentos = pd.DataFrame(atendimentos, columns=["Data", "Hora", "Tipo"])
        st.dataframe(df_atendimentos, use_container_width=True)
    else:
        st.info("Este paciente ainda não possui atendimentos registrados.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Editar paciente"):
            st.warning("Função de edição ainda não implementada.")
    with col2:
        if st.button("🗑️ Excluir paciente"):
            confirm = st.checkbox("Confirmar exclusão")
            if confirm:
                excluir_paciente(paciente_id)
                st.success("✅ Paciente excluído com sucesso!")
                st.rerun()

    evolucao = evolucao_por_paciente(paciente_id)
    if evolucao:
        df_evolucao = pd.DataFrame(evolucao, columns=["Data", "Tipo"])
        df_evolucao["Data"] = pd.to_datetime(df_evolucao["Data"])

        st.markdown("### 📈 Evolução dos atendimentos")

        grafico = alt.Chart(df_evolucao).mark_bar().encode(
            x=alt.X("yearmonth(Data):O", title="Mês"),
            y=alt.Y("count():Q", title="Número de atendimentos"),
            color=alt.Color("Tipo:N", title="Tipo de atendimento")
        ).properties(width=700, height=400)

        st.altair_chart(grafico, use_container_width=True)
    else:
        st.info("Este paciente ainda não possui evolução registrada.")