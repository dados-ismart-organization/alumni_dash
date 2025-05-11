import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from funcoes import *
import base64


exibir_banner('painel/engajamento.png', altura_px=100)


base_consolidada= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\base_final_consolidada.xlsx', tipo='excel')
engajamento_mensal= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\eventos_consolidados_por_mes.xlsx', tipo='excel')
engajamento_detalhado= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\eventos_consolidados_detalhado.xlsx', tipo='excel')

st.subheader("Visão por status da meta", divider='blue')

#azul1, azul2, azul3, azul4, azul alumni, roxinho, rosa choque, rosa claro, amarelo, verde

#colors = ['#D4EFFC','#9DDCF9','#00BDF2', '#008ED4',  '#002561','#924A7C', '#EE2D67','#F2665E', '#EBEA70','#8EC6B2']

engajamento_detalhado = engajamento_detalhado[engajamento_detalhado['Status_real'] == 'FORMADO']

paleta = ['#002561']

with st.sidebar:
    st.divider()
    st.subheader('Selecione seus filtros:')
    with st.popover("Filtros"):
        filtro_area_atual = selecionar_filtro(base_consolidada,'Area_Atual','Selecione a área de formação')
        base_consolidada_filtrada = aplicar_filtro(base_consolidada, 'Area_Atual',filtro_area_atual)
        engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado, 'Area_Atual',filtro_area_atual)


opcao = st.radio(
    "Escolha o tipo de participação para análise:",
    ("Engajamento + Giveback", "Engajamento", "Giveback")
)

# Define a coluna a ser usada com base na escolha
if opcao == "Engajamento + Giveback":
    base_consolidada_status_coluna_filtrada = 'status_meta_total'
    base_mensal_coluna_filtrada = 'status_meta_total'
    base_consolidada_status_coluna_filtrada_10h = "10h+_participacao"
elif opcao == "Engajamento":
    base_consolidada_status_coluna_filtrada = 'status_meta_engajamento'
    base_mensal_coluna_filtrada = 'status_meta_engajamento'
    base_consolidada_status_coluna_filtrada_10h = "10h+_engajamento"
    engajamento_detalhado_filtrado = engajamento_detalhado_filtrado[engajamento_detalhado_filtrado['tipo_participacao_aluno'] == opcao]
elif opcao == "Giveback":
    base_consolidada_status_coluna_filtrada = 'status_meta_giveback'
    base_mensal_coluna_filtrada = 'status_meta_giveback'
    base_consolidada_status_coluna_filtrada_10h = "10h+_giveback"
    engajamento_detalhado_filtrado = engajamento_detalhado_filtrado[engajamento_detalhado_filtrado['tipo_participacao_aluno'] == opcao]

total_alumni = base_consolidada_filtrada['RA'].count()
total_10 = base_consolidada_filtrada[base_consolidada_filtrada[base_consolidada_status_coluna_filtrada_10h] == 1].shape[0]                         
total_10_pct = round((total_10/total_alumni)*100,1)
st.metric("Alumni 10h+ total", total_10, delta = f"{total_10_pct}% da base alumni")


engajamento_status_meta_mensal = plot_barra_empilhada_percentual(
    engajamento_mensal,
    coluna_grupo="mes",
    coluna_categoria=base_mensal_coluna_filtrada,
    titulo="STATUS META POR MÊS",
    cor_categoria={
        "Alto engajamento": "#8EC6B2",
        "Engajamento mediano": "#9DDCF9",
        "Baixo engajamento": "#EBEA70",
        "Sem engajamento": "#F2665E"
    },
    ordem_categorias=["Alto engajamento", "Engajamento mediano", "Baixo engajamento",'Sem engajamento'],
    altura=400,
    orientacao='horizontal',
    ordem_grupos_alfabetica_invertida=True
)


status_meta_por_genero = plot_barra_empilhada_percentual(
    base_consolidada,
    coluna_grupo='Gênero',
    coluna_categoria=base_consolidada_status_coluna_filtrada,
    titulo="STATUS META ATUAL POR GÊNERO",
    cor_categoria={
        "Alto engajamento": "#8EC6B2",
        "Engajamento mediano": "#9DDCF9",
        "Baixo engajamento": "#EBEA70",
        "Sem engajamento": "#F2665E"
    },
    ordem_categorias=["Alto engajamento", "Engajamento mediano", "Baixo engajamento",'Sem engajamento'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)

status_meta_por_raca = plot_barra_empilhada_percentual(
    base_consolidada,
    coluna_grupo='Cor_raça',
    coluna_categoria=base_consolidada_status_coluna_filtrada,
    titulo="STATUS META ATUAL POR RAÇA",
    cor_categoria={
        "Alto engajamento": "#8EC6B2",
        "Engajamento mediano": "#9DDCF9",
        "Baixo engajamento": "#EBEA70",
        "Sem engajamento": "#F2665E"
    },
    ordem_categorias=["Alto engajamento", "Engajamento mediano", "Baixo engajamento",'Sem engajamento'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)

status_meta_por_area_formacao = plot_barra_empilhada_percentual(
    base_consolidada,
    coluna_grupo='Area_Atual',
    coluna_categoria=base_consolidada_status_coluna_filtrada,
    titulo="STATUS META ATUAL POR ÁREA DE FORMAÇÃO",
    cor_categoria={
        "Alto engajamento": "#8EC6B2",
        "Engajamento mediano": "#9DDCF9",
        "Baixo engajamento": "#EBEA70",
        "Sem engajamento": "#F2665E"
    },
    ordem_categorias=["Alto engajamento", "Engajamento mediano", "Baixo engajamento",'Sem engajamento'],
    altura=400,
    orientacao='vertical',
    ordem_grupos_alfabetica_invertida=True
)


status_meta_por_tempo_formacao = plot_barra_empilhada_percentual(
    base_consolidada,
    coluna_grupo='Classificacao_tempo_de_formacao',
    coluna_categoria=base_consolidada_status_coluna_filtrada,
    titulo="STATUS META ATUAL POR TEMPO DE FORMAÇÃO",
    cor_categoria={
        "Alto engajamento": "#8EC6B2",
        "Engajamento mediano": "#9DDCF9",
        "Baixo engajamento": "#EBEA70",
        "Sem engajamento": "#F2665E"
    },
    ordem_categorias=["Alto engajamento", "Engajamento mediano", "Baixo engajamento",'Sem engajamento'],
    altura=400,
    orientacao='vertical',
    ordem_grupos = ["Recém formado", "De 1 a 3 anos", "De 4 a 6 anos", "De 7 a 9 anos", "A partir de 10 anos"]
)

st.plotly_chart(engajamento_status_meta_mensal, use_container_width=True)


with st.expander("Mais gráficos por status da meta"):
    col1,col2 = st.columns(2)

    with col1:
        st.plotly_chart(status_meta_por_genero, use_container_width=True)
        st.divider()
        st.plotly_chart(status_meta_por_area_formacao, use_container_width=True)
        st.divider()
    with col2:
        st.plotly_chart(status_meta_por_raca, use_container_width=True)
        st.divider()
        st.plotly_chart(status_meta_por_tempo_formacao, use_container_width=True)
        st.divider()

st.divider()


st.subheader("Visão geral", divider='blue')

tab1, tab2= st.tabs(["Quebra inscrições", "Participantes ou totais"])

with tab1:

    st.markdown("#### Quebra inscrições")

    engajamento_detalhado_filtrado['participou?'] = engajamento_detalhado_filtrado['participou?'].replace({1: 'Sim', 0: 'Não'})


    col1,col2,col3,col4 = st.columns(4)
    with col1:
        with st.popover("Filtro mês"):
            filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes_y','Selecione os meses que gostaria de visualizar')
            engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'mes_y',filtro_mes_grafico_inscricoes)

    participacao_por_eventos = plot_barra_empilhada_percentual(
        engajamento_detalhado_filtrado,
        coluna_grupo='nome_evento',
        coluna_categoria='participou?',
        titulo="PARTICIPAÇÃO DOS EVENTOS DE ACORDO COM AS INSCRIÇÕES",
        altura=400,
        cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
        ordem_categorias=["Sim", "Não"],
        orientacao='vertical',
    )

    st.plotly_chart(participacao_por_eventos, use_container_width=True)

    st.caption(":red[Obs: eventos como mentoria cada sessão é contada como um único evento]")

    with st.expander("Mais gráficos por quebra de inscrições"):
    
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            with st.popover("Filtro mês"):
                filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes_y','Selecione os meses que gostaria de visualizar',key='outros_graficos')
                filtro_eventos_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'nome_evento','Selecione os meses que gostaria de visualizar')
                engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'mes_y',filtro_mes_grafico_inscricoes)
                engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'nome_evento',filtro_eventos_grafico_inscricoes)

        participacao_por_genero = plot_barra_empilhada_percentual(
            engajamento_detalhado_filtrado,
            coluna_grupo='Gênero',
            coluna_categoria='participou?',
            titulo="PARTICIPAÇÃO POR GÊNERO",
            altura=400,
            cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
            ordem_categorias=["Sim", "Não"],
            orientacao='vertical',
            ordem_grupos_alfabetica_invertida=True
        )

        participacao_por_raca = plot_barra_empilhada_percentual(
            engajamento_detalhado_filtrado,
            coluna_grupo='Cor_raça',
            coluna_categoria='participou?',
            titulo="PARTICIPAÇÃO POR RAÇA",
            altura=400,
            cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
            ordem_categorias=["Sim", "Não"],
            orientacao='vertical',
            ordem_grupos_alfabetica_invertida=True
        )

        participacao_por_area_formacao= plot_barra_empilhada_percentual(
            engajamento_detalhado_filtrado,
            coluna_grupo='Area_Atual',
            coluna_categoria='participou?',
            titulo="PARTICIPAÇÃO POR RAÇA",
            altura=400,
            cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
            ordem_categorias=["Sim", "Não"],
            orientacao='vertical',
            ordem_grupos_alfabetica_invertida=True
        )




        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(participacao_por_genero, use_container_width=True)
            st.divider()
            st.plotly_chart(participacao_por_area_formacao, use_container_width=True)
        with col2:
            st.plotly_chart(participacao_por_raca, use_container_width=True)
            st.divider()


with tab2:
    st.markdown("#### Parcipantes ou horas totais")   

    horas_totais_ou_participacao = st.radio(
    "Escolha o tipo de visualização:",
    ("Participantes totais", "Horas somadas")
)

    if horas_totais_ou_participacao == "Participantes totais":
        tipo_agregacao = 'contagem'
        coluna_valor = None
        nome_grafico= "PARTICIPANTES TOTAIS"
    else: 
        tipo_agregacao = 'soma'
        coluna_valor = 'horas_participadas'
        nome_grafico= "HORAS TOTAIS"



    col1,col2,col3,col4 = st.columns(4)
    with col1:
        with st.popover("Filtro mês"):
            filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes_y','Selecione os meses que gostaria de visualizar', key='horas_totais')
            engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'mes_y',filtro_mes_grafico_inscricoes)


    horas_totais_participacao_por_eventos =  grafico_barras(
        engajamento_detalhado_filtrado,
        "nome_evento",
        f"{nome_grafico} POR EVENTO",
        cores=['#002561'],
        template='plotly_white',
        bg_color='rgba(0,0,0,0)',
        ordem_categorias='maior_menor',  
        tipo_agregacao=tipo_agregacao,  
        coluna_valor=coluna_valor  
    )

    st.plotly_chart(horas_totais_participacao_por_eventos, use_container_width=True)

    with st.expander("Mais gráficos por horas_totais"):
    
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            with st.popover("Filtro mês"):
                filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes_y','Selecione os meses que gostaria de visualizar',key='horas_totais_outros_graficos')
                filtro_eventos_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'nome_evento','Selecione os meses que gostaria de visualizar', key ='horas_totais_outros_graficos_nome_evento')
                engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'mes_y',filtro_mes_grafico_inscricoes)
                engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'nome_evento',filtro_eventos_grafico_inscricoes)
        
        col1, col2 = st.columns(2)
        with col1: 
            horas_totais_por_genero =  grafico_barras(
                engajamento_detalhado_filtrado,
                "Gênero",
                f"{nome_grafico} POR GÊNERO",
                cores=['#002561'],
                template='plotly_white',
                bg_color='rgba(0,0,0,0)',
                ordem_categorias='maior_menor',  
                tipo_agregacao=tipo_agregacao,  
                coluna_valor=coluna_valor  
            )

            horas_totais_por_raca =  grafico_barras(
                engajamento_detalhado_filtrado,
                "Cor_raça",
                f"{nome_grafico} POR GÊNERO",
                cores=['#002561'],
                template='plotly_white',
                bg_color='rgba(0,0,0,0)',
                ordem_categorias='maior_menor',  
                tipo_agregacao=tipo_agregacao,  
                coluna_valor=coluna_valor  
            )

            horas_totais_por_area_atual =  grafico_barras(
                engajamento_detalhado_filtrado,
                "Area_Atual",
               f"{nome_grafico} POR ÁREA DE FORMAÇÃO",
                cores=['#002561'],
                template='plotly_white',
                bg_color='rgba(0,0,0,0)',
                ordem_categorias='maior_menor',  
                tipo_agregacao=tipo_agregacao,  
                coluna_valor=coluna_valor  
            )

        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(horas_totais_por_genero, use_container_width=True)
            st.divider()
            st.plotly_chart(horas_totais_por_area_atual, use_container_width=True)
        with col2:
            st.plotly_chart(horas_totais_por_raca, use_container_width=True)
            st.divider()
