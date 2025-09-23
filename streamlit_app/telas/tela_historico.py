def tela_historico():
    import streamlit as st
    from db import listar_historico

    if "usuario_logado" not in st.session_state:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        st.stop()

    st.set_page_config(page_title="📜 Histórico de Atendimentos", layout="wide")
    st.title("📜 Histórico de Atendimentos")

    historico = listar_historico()

    if not historico:
        st.info("Nenhum atendimento registrado ainda.")
        return

    # Filtros opcionais
    st.markdown("### 🔍 Filtros")
    nome_filtro = st.text_input("Filtrar por nome do paciente")
    tipo_filtro = st.selectbox("Filtrar por tipo", ["Todos", "Consulta", "Retorno", "Sessão"])

    # Aplicar filtros
    atendimentos_filtrados = []
    for nome, data, hora, tipo in historico:
        if nome_filtro and nome_filtro.lower() not in nome.lower():
            continue
        if tipo_filtro != "Todos" and tipo != tipo_filtro:
            continue
        atendimentos_filtrados.append((nome, data, hora, tipo))

    # Exibir tabela
    st.markdown("### 📋 Lista de atendimentos")
    st.dataframe(
        atendimentos_filtrados,
        use_container_width=True,
        column_config={
            0: "Paciente",
            1: "Data",
            2: "Hora",
            3: "Tipo"
        }
    )