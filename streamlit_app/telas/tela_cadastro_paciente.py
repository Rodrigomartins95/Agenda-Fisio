def tela_cadastro_paciente():
    import streamlit as st
    from db import inserir_paciente
    if "usuario_logado" not in st.session_state:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        st.stop()
    st.set_page_config(page_title="➕ Cadastrar Paciente", layout="centered")
    st.title("➕ Cadastro de Paciente")
    from db import inserir_atendimento
    with st.form("form_paciente"):
        nome = st.text_input("Nome completo do paciente")
        telefone = st.text_input("Telefone (WhatsApp)")
        obs = st.text_area("Observações clínicas", height=150)
        fisioterapeuta = st.text_input("Fisioterapeuta responsável", value=st.session_state.get("fisioterapeuta", ""), disabled=True)
        dias_semana = st.multiselect("Dias da semana para atendimento", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"])
        hora_atendimento = st.time_input("Hora do atendimento padrão")
        tipo = st.selectbox("Tipo de atendimento", ["Consulta", "Retorno", "Sessão"])
        qtd_semanas = st.number_input("Quantas semanas?", min_value=1, max_value=12, value=1)
        enviado = st.form_submit_button("Salvar")
        if enviado:
            if not nome or not telefone:
                st.warning("⚠️ Nome e telefone são obrigatórios.")
            elif not dias_semana:
                st.warning("Selecione pelo menos um dia da semana.")
            else:
                if st.session_state.get("ultimo_paciente_cadastrado") == nome:
                    st.info(f"Paciente '{nome}' já foi cadastrado!")
                else:
                    inserir_paciente(nome, telefone, obs, fisioterapeuta)
                    st.session_state["ultimo_paciente_cadastrado"] = nome
                    st.success(f"✅ Paciente '{nome}' cadastrado com sucesso!")
                    # Agendar atendimentos automaticamente
                    import datetime
                    dias_map = {"Segunda": 0, "Terça": 1, "Quarta": 2, "Quinta": 3, "Sexta": 4, "Sábado": 5}
                    hoje = datetime.date.today()
                    for semana in range(int(qtd_semanas)):
                        for dia in dias_semana:
                            # Encontrar próxima data do dia da semana
                            delta = (dias_map[dia] - hoje.weekday() + 7) % 7 + semana*7
                            data_atendimento = hoje + datetime.timedelta(days=delta)
                            inserir_atendimento(nome, str(data_atendimento), str(hora_atendimento), tipo)