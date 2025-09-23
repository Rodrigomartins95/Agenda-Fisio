def tela_cadastro():
    import streamlit as st
    import sqlite3
    import bcrypt
    from db import inicializar_banco

    # Inicializa banco
    inicializar_banco()

    # Configuração da página
    st.set_page_config(page_title="📝 Cadastro", layout="centered")
    st.title("Cadastro de Fisioterapeuta")
    prefixo = st.selectbox("Prefixo", ["Dr", "Dra"])
    email = st.text_input("Email", key="cadastro_email")
    senha = st.text_input("Senha", type="password", key="cadastro_senha")
    confirmar = st.text_input("Confirmar Senha", type="password", key="cadastro_confirmar")
    nome_fisio = st.text_input("Nome completo do fisioterapeuta")

    def salvar_usuario(email, senha, fisioterapeuta):
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        conn = sqlite3.connect("agenda.db")
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    senha BLOB,
                    fisioterapeuta TEXT
                )
            """)
            cursor.execute("INSERT INTO usuarios (email, senha, fisioterapeuta) VALUES (?, ?, ?)", (email, senha_hash, fisioterapeuta))
            conn.commit()
        finally:
            conn.close()

    col1, col2 = st.columns([2,1])
    with col1:
        cadastrar = st.button("Cadastrar")
        if cadastrar:
            if not email or not senha or not confirmar or not nome_fisio:
                st.warning("⚠️ Preencha todos os campos.")
            elif senha != confirmar:
                st.error("❌ As senhas não coincidem.")
            else:
                fisioterapeuta = f"{prefixo} {nome_fisio.strip()}"
                try:
                    salvar_usuario(email, senha, fisioterapeuta)
                    st.session_state["usuario_logado"] = email
                    st.session_state["fisioterapeuta"] = fisioterapeuta
                    st.success("✅ Cadastro realizado com sucesso!")
                    st.session_state["tela"] = "login"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("❌ Este email já está cadastrado.")
                except Exception as exc:
                    st.error(f"Erro ao cadastrar: {exc}")
    # Link para login
    st.markdown("---")
    st.markdown("Já tem cadastro?")

    if st.button("🔐 Ir para Login"):
        st.session_state["tela"] = "login"
        st.rerun()