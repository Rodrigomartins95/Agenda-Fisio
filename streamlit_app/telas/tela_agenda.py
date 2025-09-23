from streamlit_calendar import calendar
import streamlit as st
import datetime
from db import (
    buscar_atendimentos_por_offset,
    excluir_atendimento,
    limpar_atendimentos,
    editar_atendimento,
    buscar_paciente_id_por_nome
)

def tela_agenda():
    if "usuario_logado" not in st.session_state:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        st.stop()

    st.set_page_config(page_title="Agenda Semanal", layout="wide")
    st.title("📅 Agenda da Semana")

    offset = st.slider("Semana", min_value=0, max_value=12, value=0, help="Escolha a semana para visualizar")
    atendimentos, inicio, fim = buscar_atendimentos_por_offset(offset)

    cores_por_tipo = {
        "Consulta": "#90caf9",
        "Retorno": "#a5d6a7",
        "Sessão": "#f48fb1"
    }

    eventos = []
    if atendimentos:
        for atendimento in atendimentos:
            try:
                nome, data, hora, tipo = atendimento
                hora_formatada = hora if len(hora.split(":")) == 3 else f"{hora}:00"
                dt_str = f"{data}T{hora_formatada}"
                eventos.append({
                    "title": f"{tipo}: {nome}",
                    "start": dt_str,
                    "end": dt_str,
                    "color": cores_por_tipo.get(tipo, "#e0e0e0"),
                    "extendedProps": {
                        "paciente": nome,
                        "tipo": tipo,
                        "data": data,
                        "hora": hora_formatada,
                    }
                })
            except Exception as e:
                st.error(f"Erro ao montar evento: {e}")

    calendar_options = {
        "initialView": "timeGridWeek",
        "locale": "pt-br",
        "editable": False,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "slotMinTime": "07:00:00",
        "slotMaxTime": "23:00:00"
    }

    clicked_event = calendar(events=eventos, options=calendar_options)

    if clicked_event:
        props = clicked_event.get("extendedProps", {})
        paciente = props.get("paciente")
        tipo = props.get("tipo")
        data = props.get("data")
        hora = props.get("hora")

        st.markdown("### 📋 Detalhes do atendimento")
        with st.container():
            st.write(f"**Paciente:** {paciente}")
            st.write(f"**Tipo:** {tipo}")
            st.write(f"**Data:** {datetime.date.fromisoformat(data).strftime('%d-%m-%Y')}")
            st.write(f"**Hora:** {hora}")

            with st.form("form_editar_atendimento"):
                try:
                    data_formatada = data.split("T")[0] if "T" in data else data
                    nova_data = st.date_input("Nova data", value=datetime.date.fromisoformat(data_formatada))

                    hora_formatada = hora.split("T")[-1] if "T" in hora else hora
                    if len(hora_formatada.split(":")) == 2:
                        hora_formatada += ":00"
                    nova_hora = st.time_input("Nova hora", value=datetime.time.fromisoformat(hora_formatada))

                    novo_tipo = st.selectbox(
                        "Novo tipo",
                        ["Consulta", "Retorno", "Sessão"],
                        index=["Consulta", "Retorno", "Sessão"].index(tipo)
                    )
                except Exception as e:
                    st.error(f"❌ Erro ao interpretar data ou hora: {e}")
                    st.stop()

                submitted = st.form_submit_button("💾 Salvar alterações")
                if submitted:
                    paciente_id = buscar_paciente_id_por_nome(paciente)
                    if paciente_id is None:
                        st.error("❌ Paciente não encontrado no banco.")
                    else:
                        editar_atendimento(
                            paciente_id=paciente_id,
                            data_antiga=data,
                            hora_antiga=hora,
                            nova_data=nova_data.strftime("%Y-%m-%d"),  # salva no formato ISO
                            nova_hora=nova_hora.strftime("%H:%M:%S"),
                            novo_tipo=novo_tipo
                        )
                        st.success("✅ Atendimento atualizado com sucesso!")
                        st.rerun()

            if st.button("🗑️ Excluir atendimento"):
                confirm = st.checkbox("Confirmar exclusão")
                if confirm:
                    excluir_atendimento(paciente, data, hora)
                    st.success("✅ Atendimento excluído com sucesso!")
                    st.rerun()

    st.markdown("### 🧹 Limpeza de atendimentos")
    if st.button("Limpar atendimentos sem paciente"):
        limpar_atendimentos()
        st.success("✅ Atendimentos removidos com sucesso!")
        st.rerun()