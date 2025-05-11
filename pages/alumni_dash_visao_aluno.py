import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from funcoes import *
import base64



base_consolidada= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\base_final_consolidada.xlsx', tipo='excel')
engajamento_mensal= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\eventos_consolidados_por_mes.xlsx', tipo='excel')


st.subheader("Visão geral do alumni", divider='blue')

#azul1, azul2, azul3, azul4, azul alumni, roxinho, rosa choque, rosa claro, amarelo, verde

#colors = ['#D4EFFC','#9DDCF9','#00BDF2', '#008ED4',  '#002561','#924A7C', '#EE2D67','#F2665E', '#EBEA70','#8EC6B2']

col1, col2, col3, col4 = st.columns(4)

with col1:

    nome_alumni = st.selectbox(
        "Nome alumni",
        base_consolidada['NOME_SEM_ACENTO_MAIUSCULO '].unique(),
    )

base_consolidada_alumni = base_consolidada[base_consolidada['NOME_SEM_ACENTO_MAIUSCULO '] == nome_alumni]
engajamento_mensal =  engajamento_mensal[engajamento_mensal['NOME_SEM_ACENTO_MAIUSCULO '] == nome_alumni]

opcao_tipo = st.radio(
    "Escolha o tipo de participação para análise:",
    ("Engajamento + Giveback", "Engajamento", "Giveback"), key='segundo_radio'
)

# Define a coluna a ser usada com base na escolha
if opcao_tipo == "Engajamento + Giveback":
    base_consolidada_status_coluna_filtrada = 'status_meta_total'
    base_mensal_coluna_filtrada = 'status_meta_total'
elif opcao_tipo == "Engajamento":
    base_consolidada_status_coluna_filtrada = 'status_meta_engajamento'
    base_mensal_coluna_filtrada = 'status_meta_engajamento'
elif opcao_tipo == "Giveback":
    base_consolidada_status_coluna_filtrada = 'status_meta_giveback'
    base_mensal_coluna_filtrada = 'status_meta_giveback'





alumni_engajamento_por_mes = grafico_barras_teste(
    engajamento_mensal,
    coluna_x='mes',
    nome_grafico='Horas dedicadas por mês',
    tipo_agregacao='soma',
    coluna_valor='horas_totais_somados_acumulados',
    cores=['#002561'],
)

st.plotly_chart(alumni_engajamento_por_mes, use_container_width=True)
st.divider()