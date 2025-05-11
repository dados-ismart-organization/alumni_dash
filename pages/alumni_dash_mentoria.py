import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from funcoes import *
import base64

#chamando função que lê o banner
exibir_banner('painel/mentoria.png', altura_px=100)



#azul1, azul2, azul3, azul4, azul alumni, roxinho, rosa choque, rosa claro, amarelo, verde

#colors = ['#D4EFFC','#9DDCF9','#00BDF2', '#008ED4',  '#002561','#924A7C', '#EE2D67','#F2665E', '#EBEA70','#8EC6B2']

#importando bases
mentoria_consolidado= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\mentoria_consolidado.xlsx', tipo='excel')
mentoria_sessoes_consolidadas= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\mentoria_registros_sessoes.xlsx', tipo='excel')


with st.sidebar:
    st.divider()
    st.subheader('Selecione seus filtros:')
    with st.popover("Filtros"):
        selecao_area = selecionar_filtro(mentoria_sessoes_consolidadas,'Area_Atual','Selecione a área de formação', key='area_atual')
        mentoria_sessoes_consolidadas = aplicar_filtro(mentoria_sessoes_consolidadas, 'Area_Atual', selecao_area)
        mentoria_consolidado = aplicar_filtro(mentoria_consolidado, 'Area_Atual', selecao_area)


#filtro de escolha de qual mentoria gostaria de ser visualizada
opcao_mentoria = st.radio(
    "Escolha qual mentoria gostaria de visualizar:",
    (mentoria_consolidado['nome_evento'].unique())
)


#filtrando base com mentoria que gostaria de ver
mentoria_consolidado_filtrado = mentoria_consolidado[mentoria_consolidado['nome_evento'] == opcao_mentoria]
#mentoria_sessoes_consolidadas_filtrado = mentoria_sessoes_consolidadas[mentoria_sessoes_consolidadas['nome_evento'] == opcao_mentoria]



inscritos_totais = mentoria_consolidado_filtrado['RA'].count()
ativos_atualmente = mentoria_consolidado_filtrado[mentoria_consolidado_filtrado['status_mentoria'] != 'Desistente'].shape[0]                         
ativos_atualmente_pct = round((ativos_atualmente/inscritos_totais)*100,1)
st.metric("Ativos atualmente", ativos_atualmente, delta = f"{ativos_atualmente_pct}% dos incritos")


#criando df com os desistentes
mentoria_consolidado_filtrado_desistente = mentoria_consolidado_filtrado[mentoria_consolidado_filtrado['status_mentoria'] == "Desistente"]


alumni_mentoria_status = grafico_barras(
    df=mentoria_consolidado_filtrado,
    coluna_x='status_mentoria',
    nome_grafico='STATUS MENTORIA',
    cores=['#00BDF2'],
    ordem_categorias=None
)

alumni_mentoria_status_desistente = grafico_barras(
    df=mentoria_consolidado_filtrado_desistente,
    coluna_x='motivo_desistencias_agrupado',
    nome_grafico='MOTIVOS DESISTÊNCIAS',
    cores=['#00BDF2'],
    ordem_categorias=None
)


col1, col2 =  st.columns(2)
with col1:
    st.plotly_chart(alumni_mentoria_status, use_container_width=True)
with col2:
    st.plotly_chart(alumni_mentoria_status_desistente, use_container_width=True)


st.divider()

status_mentoria_por_genero = plot_barra_empilhada_percentual(
    mentoria_consolidado_filtrado,
    coluna_grupo='Gênero',
    coluna_categoria='status_mentoria',
    titulo="STATUS MENTORIA POR GÊNERO",
    cor_categoria={
        "Participacao total": "#8EC6B2",
        "Participacao parcial": "#9DDCF9",
        "Desengajado": "#EBEA70",
        "Desistente": "#F2665E"
    },
    ordem_categorias=["Participacao total", "Participacao parcial", "Desengajado",'Desistente'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)


status_mentoria_por_genero = plot_barra_empilhada_percentual(
    mentoria_consolidado_filtrado,
    coluna_grupo='Gênero',
    coluna_categoria='status_mentoria',
    titulo="STATUS MENTORIA POR GÊNERO",
    cor_categoria={
        "Participacao total": "#8EC6B2",
        "Participacao parcial": "#9DDCF9",
        "Desengajado": "#EBEA70",
        "Desistente": "#F2665E"
    },
    ordem_categorias=["Participacao total", "Participacao parcial", "Desengajado",'Desistente'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)

status_mentoria_por_raca = plot_barra_empilhada_percentual(
    mentoria_consolidado_filtrado,
    coluna_grupo='Cor_raça',
    coluna_categoria='status_mentoria',
    titulo="STATUS MENTORIA POR RAÇA",
    cor_categoria={
        "Participacao total": "#8EC6B2",
        "Participacao parcial": "#9DDCF9",
        "Desengajado": "#EBEA70",
        "Desistente": "#F2665E"
    },
    ordem_categorias=["Participacao total", "Participacao parcial", "Desengajado",'Desistente'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)

status_mentoria_por_area_formacao = plot_barra_empilhada_percentual(
    mentoria_consolidado_filtrado,
    coluna_grupo='Area_Atual',
    coluna_categoria='status_mentoria',
    titulo="STATUS MENTORIA ÁREA DE FORMAÇÃO",
    cor_categoria={
        "Participacao total": "#8EC6B2",
        "Participacao parcial": "#9DDCF9",
        "Desengajado": "#EBEA70",
        "Desistente": "#F2665E"
    },
    ordem_categorias=["Participacao total", "Participacao parcial", "Desengajado",'Desistente'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)

status_mentoria_por_perfil = plot_barra_empilhada_percentual(
    mentoria_consolidado_filtrado,
    coluna_grupo='Perfil_real',
    coluna_categoria='status_mentoria',
    titulo="STATUS MENTORIA POR TEMPO DE FORMAÇÃO",
    cor_categoria={
        "Participacao total": "#8EC6B2",
        "Participacao parcial": "#9DDCF9",
        "Desengajado": "#EBEA70",
        "Desistente": "#F2665E"
    },
    ordem_categorias=["Participacao total", "Participacao parcial", "Desengajado",'Desistente'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)


with st.expander("Mais gráficos por status da mentoria"):
    col1,col2 = st.columns(2)

    with col1:
        st.plotly_chart(status_mentoria_por_genero, use_container_width=True)
        st.divider()
        st.plotly_chart(status_mentoria_por_area_formacao, use_container_width=True)
        st.divider()

    with col2:
        st.plotly_chart(status_mentoria_por_raca, use_container_width=True)
        st.divider()
        st.plotly_chart(status_mentoria_por_perfil, use_container_width=True)
        st.divider()