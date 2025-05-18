import streamlit as st
import time

 
def check_microsoft_login():
    """Autenticação via login da Microsoft e verificação do domínio."""
    if not st.user.is_logged_in:
        st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold;'>🔐 Bem-vindo(a) ao Dashboard Alumni</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 18px;'>Para acessar as informações, faça login com sua conta institucional.</div>", unsafe_allow_html=True)
        st.write("")
       
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.write("")
            st.button("🔓 Acessar com minha conta Microsoft",
                      on_click=st.login,
                      help="Clique para entrar com seu e-mail do Ismart",
                      use_container_width=True)
            st.write("")
        st.stop()
 
    usuario = st.user
    email_usuario = usuario.email
 
    if not email_usuario.endswith("@ismart.org.br"):
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold;'>⛔ Acesso não autorizado</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 16px;'>Apenas usuários com e-mail institucional (@ismart.org.br) podem acessar este dashboard.</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 14px;'>Caso precise de ajuda, entre em contato com o <b>time de dados</b>!</div>", unsafe_allow_html=True)
            st.write("")
            st.button("↩️ Tentar novamente", on_click=st.logout, use_container_width=True)
        st.stop()
 
    return True
 
def logout():
    """Realiza logout da conta Microsoft e limpa a sessão."""
    if st.user.is_logged_in:
        st.logout()
   
    # Limpa variáveis da sessão
    keys_to_remove = ["auth_success_shown", "autenticado"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
   
    st.toast("🔒 Você foi desconectado com sucesso!", icon="🔒")
    time.sleep(0.5)