import streamlit as st
from PIL import Image
from utils.auth import *
import time


st.set_page_config(page_title = "Dash Alumni", layout="wide", initial_sidebar_state="collapsed")

dados_gerais = st.Page("pages/alumni_dash_dados_gerais.py", title="Dados Gerais")
engajamento = st.Page("pages/alumni_dash_engajamento.py", title="Engajamento e Giveback")
mentoria = st.Page("pages/alumni_dash_mentoria.py", title="Mentoria")
download = st.Page("pages/alumni_dash_downloads_bases.py", title="Download de bases")
mentoria = st.Page("pages/alumni_dash_mentoria.py", title="Mentoria")


if check_microsoft_login():
    # Mostra o toast APENAS na primeira vez
    if "auth_success_shown" not in st.session_state:
        st.toast("Autenticação realizada com sucesso! Selecione uma página no menu lateral.", icon="✅")
        st.session_state.auth_success_shown = True  # Marca como já exibido
 
    # Botão de logout na sidebar (melhorado)
    with st.sidebar:
        if st.button("🚪 **Sair da conta**",
                    type="secondary",
                    help="Clique para desconectar-se completamente",
                    use_container_width=True):
            logout()
            st.rerun()  # Recarrega a aplicação


    pg = st.navigation([dados_gerais, engajamento,mentoria, download])

    pg.run()

else:
    st.stop()
