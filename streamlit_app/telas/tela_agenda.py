def tela_agenda():
    import streamlit as st
    from db import buscar_atendimentos_por_offset
    if "usuario_logado" not in st.session_state:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        st.stop()
    st.set_page_config(page_title="Agenda Semanal", layout="wide")
    st.title("📅 Agenda da Semana")
    from db import listar_pacientes, inserir_atendimento
    atendimentos, inicio, fim = buscar_atendimentos_por_offset(0)
    import datetime
    # Corrigir caso inicio/fim sejam None
    if not inicio or not fim:
        hoje = datetime.date.today()
        inicio = (hoje - datetime.timedelta(days=hoje.weekday())).strftime("%d/%m/%Y")
        fim = (hoje + datetime.timedelta(days=5-hoje.weekday())).strftime("%d/%m/%Y")
    st.markdown("### Agendar novo atendimento")
    pacientes = listar_pacientes()
    nomes_pacientes = [p[1] for p in pacientes] if pacientes else []
    with st.form("form_agendar"):
        paciente = st.selectbox("Paciente", nomes_pacientes)
        data = st.date_input("Data do atendimento")
        hora = st.time_input("Hora do atendimento")
        tipo = st.selectbox("Tipo de atendimento", ["Consulta", "Retorno", "Sessão"])
        enviar = st.form_submit_button("Agendar")
        if enviar:
            if not paciente:
                st.warning("Selecione um paciente.")
            else:
                inserir_atendimento(paciente, str(data), str(hora), tipo)
                st.success(f"Atendimento para '{paciente}' agendado com sucesso!")
                st.rerun()

    import datetime
    st.markdown(f"**Semana de {inicio} a {fim}**")
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    agenda = {dia: {} for dia in dias_semana}  # {dia: {hora: [atendimentos]}}
    horarios_padrao = [f"{h:02d}:00" for h in range(7, 21)]  # 07:00 até 20:00
    if atendimentos:
        for nome, data, hora, tipo in atendimentos:
            try:
                dt = datetime.datetime.strptime(data, "%Y-%m-%d")
                dia_idx = dt.weekday()
                if dia_idx < 6:
                    dia = dias_semana[dia_idx]
                    if hora not in agenda[dia]:
                        agenda[dia][hora] = []
                    agenda[dia][hora].append({"nome": nome, "tipo": tipo})
            except Exception:
                continue
        st.markdown("<style>div[data-testid='column']{min-width:180px !important;} .calendar-cell{border:1px solid #222;padding:4px;height:40px;vertical-align:top;}</style>", unsafe_allow_html=True)
        st.markdown("<b>Calendário semanal</b>")
        # Cabeçalho dos dias
        header_cols = st.columns(len(dias_semana)+1)
        with header_cols[0]:
            st.markdown("<b>Horário</b>", unsafe_allow_html=True)
        for i, dia in enumerate(dias_semana):
            with header_cols[i+1]:
                st.markdown(f"<b>{dia}</b>", unsafe_allow_html=True)
        # Grid de horários
        for hora in horarios_padrao:
            row = st.columns(len(dias_semana)+1)
            with row[0]:
                st.markdown(f"<span style='font-size:13px'>{hora}</span>", unsafe_allow_html=True)
            for i, dia in enumerate(dias_semana):
                with row[i+1]:
                    cell = agenda[dia].get(hora, [])
                    if cell:
                        for item in cell:
                            st.markdown(f"<div class='calendar-cell' style='background:#e3f2fd;border-radius:6px;margin-bottom:2px'>"
                                        f"<b>{item['nome']}</b><br><span style='font-size:12px'>{item['tipo']}</span></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='calendar-cell'></div>", unsafe_allow_html=True)
    else:
        st.info("Nenhum atendimento agendado para esta semana.")