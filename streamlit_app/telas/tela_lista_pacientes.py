def tela_lista_pacientes():
    import streamlit as st
    from db import listar_pacientes
    if "usuario_logado" not in st.session_state:
        st.warning("⚠️ Você precisa estar logado para acessar esta página.")
        st.stop()
    st.set_page_config(page_title="Pacientes", layout="wide")
    st.title("Pacientes Cadastrados")
    pacientes = listar_pacientes()
    from db import deletar_paciente, editar_paciente
    if pacientes:
        for id, nome, telefone, obs in pacientes:
            st.subheader(f"{nome}")
            st.write(f"📞 Telefone: {telefone}")
            if obs:
                st.write(f"📝 Observações: {obs}")
            col1, col2, col3 = st.columns([1,1,2])
            with col1:
                if st.button(f"🗑️ Deletar", key=f"del_{id}"):
                    deletar_paciente(id)
                    st.success(f"Paciente '{nome}' deletado!")
                    st.rerun()
            with col2:
                if st.button(f"✏️ Editar", key=f"edit_{id}"):
                    st.session_state["edit_paciente_id"] = id
                    st.session_state["edit_paciente_nome"] = nome
                    st.session_state["edit_paciente_telefone"] = telefone
                    st.session_state["edit_paciente_obs"] = obs
                    st.session_state["edit_mode"] = True
                    st.rerun()
            st.divider()
        # Formulário de edição
        if st.session_state.get("edit_mode", False):
            st.markdown("## Editar Paciente")
            with st.form("form_editar_paciente"):
                novo_nome = st.text_input("Nome", value=st.session_state["edit_paciente_nome"])
                novo_telefone = st.text_input("Telefone", value=st.session_state["edit_paciente_telefone"])
                novo_obs = st.text_area("Observações", value=st.session_state["edit_paciente_obs"])
                enviado = st.form_submit_button("Salvar alterações")
                if enviado:
                    editar_paciente(
                        st.session_state["edit_paciente_id"],
                        novo_nome,
                        novo_telefone,
                        novo_obs
                    )
                    st.success("Paciente editado com sucesso!")
                    st.session_state["edit_mode"] = False
                    st.rerun()
    else:
        st.info("Nenhum paciente cadastrado ainda.")