def tela_login():
    import streamlit as st
    import sqlite3
    import bcrypt
    from db import inicializar_banco

    # Inicializa o banco
    inicializar_banco()

    # Título da página
    st.title("🔐 Login")

    # Campos de entrada
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")

    # Função para autenticar usuário e recuperar fisioterapeuta
    def autenticar_usuario(email, senha_digitada):
        conn = sqlite3.connect("agenda.db")
        cursor = conn.cursor()
        cursor.execute("SELECT senha, fisioterapeuta FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            senha_hash, fisioterapeuta = resultado
            if bcrypt.checkpw(senha_digitada.encode(), senha_hash):
                st.session_state["usuario_logado"] = email
                st.session_state["fisioterapeuta"] = fisioterapeuta
                return True
        return False

    col1, col2 = st.columns([2,1])
    with col1:
        if st.button("Entrar"):
            if autenticar_usuario(email, senha):
                st.success("✅ Login realizado com sucesso!")
                st.session_state["tela"] = "agenda"
                st.rerun()
            else:
                st.error("❌ Email ou senha inválidos.")
    with col2:
        if st.button("⬅️ Voltar"):
            st.session_state["tela"] = "inicio"
            st.rerun()
