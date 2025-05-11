import streamlit as st


st.set_page_config(page_title = "Dash Alumni", layout="wide", initial_sidebar_state="collapsed")

dados_gerais = st.Page("pages/alumni_dash_dados_gerais.py", title="Dados Gerais")
engajamento = st.Page("pages/alumni_dash_engajamento.py", title="Engajamento e Giveback")
mentoria = st.Page("pages/alumni_dash_mentoria.py", title="Mentoria")
download = st.Page("pages/alumni_dash_downloads_bases.py", title="Download de bases")
mentoria = st.Page("pages/alumni_dash_mentoria.py", title="Mentoria")

pg = st.navigation([dados_gerais, engajamento,mentoria, download])

pg.run()
