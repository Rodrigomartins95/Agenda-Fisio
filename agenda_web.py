import streamlit as st
from db import buscar_atendimentos_por_offset
from datetime import datetime

# Função para formatar os dias
dias_formatados = {
    "Monday": "Segunda",
    "Tuesday": "Terça",
    "Wednesday": "Quarta",
    "Thursday": "Quinta",
    "Friday": "Sexta",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Cores por tipo de atendimento
tipo_cores = {
    "Fisioterapia": "#AED581",
    "Avaliação": "#64B5F6",
    "Retorno": "#FFD54F",
    "Pilates": "#FF8A65",
    "Outro": "#E0E0E0"
}

st.set_page_config(page_title="Agenda Semanal", layout="wide")
st.title("📅 Agenda Semanal")

# Navegação entre semanas
offset = st.slider("Semana", min_value=-4, max_value=4, value=0, step=1, format="Semana %d")
atendimentos, inicio, fim = buscar_atendimentos_por_offset(offset)

st.markdown(f"**Semana de {inicio} a {fim}**")

# Agrupar atendimentos por dia
agenda_por_dia = {}
for nome, data, hora, tipo in atendimentos:
    dia_semana = dias_formatados[datetime.strptime(data, "%Y-%m-%d").strftime("%A")]
    chave = f"{dia_semana} - {data}"
    if chave not in agenda_por_dia:
        agenda_por_dia[chave] = []
    agenda_por_dia[chave].append((hora, nome, tipo))

# Exibir agenda
for dia, lista in agenda_por_dia.items():
    st.subheader(dia)
    for hora, nome, tipo in lista:
        cor = tipo_cores.get(tipo, tipo_cores["Outro"])
        st.markdown(
            f"<div style='background-color:{cor};padding:8px;border-radius:5px;margin-bottom:5px;'>"
            f"<strong>{hora}</strong> - {nome} ({tipo})"
            f"</div>",
            unsafe_allow_html=True
        )