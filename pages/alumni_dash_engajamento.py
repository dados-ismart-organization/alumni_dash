import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from utils.funcoes import *
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
    #colocando esses espaços vazios só para o popover caber certinho na tela   
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.divider()
    st.subheader('Filtros gerais:')

    with st.popover("Filtros"):


        #criando multiselect dos filtros
        filtro_area_atual = selecionar_filtro(base_consolidada,'Area_Atual','Selecione a área de formação')
        filtro_tempo_formacao = selecionar_filtro(base_consolidada,'Classificacao_tempo_de_formacao','Selecione o tempo de formação')
        filtro_genero = selecionar_filtro(base_consolidada,'Gênero','Selecione o filtro de gênero')
        filtro_raca = selecionar_filtro(base_consolidada,'Cor_raça','Selecione o filtro de raça')

        #aplicando filtro as bases e gerando as bases filtradas
        ## filtro de área
    
        base_consolidada_filtrada = aplicar_filtro(base_consolidada, 'Area_Atual',filtro_area_atual)
        engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado, 'Area_Atual',filtro_area_atual)
        engajamento_mensal_filtrado = aplicar_filtro(engajamento_mensal, 'Area_Atual',filtro_area_atual)

        ## filtro de tempo de formação

        base_consolidada_filtrada = aplicar_filtro(base_consolidada, 'Classificacao_tempo_de_formacao',filtro_tempo_formacao)
        engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado, 'Classificacao_tempo_de_formacao',filtro_tempo_formacao)
        engajamento_mensal_filtrado = aplicar_filtro(engajamento_mensal, 'Classificacao_tempo_de_formacao',filtro_tempo_formacao)
        
        ## filtro de genero
    
        base_consolidada_filtrada = aplicar_filtro(base_consolidada_filtrada, 'Gênero',filtro_genero)
        engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'Gênero',filtro_genero)
        engajamento_mensal_filtrado = aplicar_filtro(engajamento_mensal_filtrado, 'Gênero',filtro_genero)
        
        ## filtro de raça
    
        base_consolidada_filtrada = aplicar_filtro(base_consolidada_filtrada, 'Cor_raça',filtro_raca)
        engajamento_detalhado_filtrado = aplicar_filtro(engajamento_detalhado_filtrado, 'Cor_raça',filtro_raca)
        engajamento_mensal_filtrado = aplicar_filtro(engajamento_mensal_filtrado, 'Cor_raça',filtro_raca)


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
    engajamento_mensal_filtrado,
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
    base_consolidada_filtrada,
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
    base_consolidada_filtrada,
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
    base_consolidada_filtrada,
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
    base_consolidada_filtrada,
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


status_meta_por_programa_entrada = plot_barra_empilhada_percentual(
    base_consolidada_filtrada,
    coluna_grupo='Programa_Entrada',
    coluna_categoria=base_consolidada_status_coluna_filtrada,
    titulo="STATUS META ATUAL POR PRGRAMA DE ENTRADA",
    cor_categoria={
        "Alto engajamento": "#8EC6B2",
        "Engajamento mediano": "#9DDCF9",
        "Baixo engajamento": "#EBEA70",
        "Sem engajamento": "#F2665E"
    },
    ordem_categorias=["Alto engajamento", "Engajamento mediano", "Baixo engajamento",'Sem engajamento'],
    altura=400,
    orientacao='vertical',
)

status_meta_por_praca_eb = plot_barra_empilhada_percentual(
    base_consolidada_filtrada,
    coluna_grupo='Praça_Agrupado',
    coluna_categoria=base_consolidada_status_coluna_filtrada,
    titulo="STATUS META ATUAL POR PRAÇA DE ENTRADA",
    cor_categoria={
        "Alto engajamento": "#8EC6B2",
        "Engajamento mediano": "#9DDCF9",
        "Baixo engajamento": "#EBEA70",
        "Sem engajamento": "#F2665E"
    },
    ordem_categorias=["Alto engajamento", "Engajamento mediano", "Baixo engajamento",'Sem engajamento'],
    altura=400,
    orientacao='vertical',
)

st.plotly_chart(engajamento_status_meta_mensal, use_container_width=True)

with st.expander("Mais gráficos por status da meta"):
    
    #st.columns feito dessa forma para dar um espaço (0.5) e uma coluna e outra
    col1,col2,col3 = st.columns([2,0.5,2])

    with col1:
        st.plotly_chart(status_meta_por_genero, use_container_width=True)
        st.divider()
        st.plotly_chart(status_meta_por_area_formacao, use_container_width=True)
        st.divider()
        st.plotly_chart(status_meta_por_programa_entrada, use_container_width=True)

    with col3:
        st.plotly_chart(status_meta_por_raca, use_container_width=True)
        st.divider()
        st.plotly_chart(status_meta_por_tempo_formacao, use_container_width=True)
        st.divider()
        st.plotly_chart(status_meta_por_praca_eb, use_container_width=True)

st.divider()


st.subheader("Visão geral", divider='blue')

tab1, tab2= st.tabs(["Quebra inscrições", "Participantes ou totais"])

with tab1:

    st.markdown("#### Quebra inscrições")

    engajamento_detalhado_filtrado['participou?'] = engajamento_detalhado_filtrado['participou?'].replace({1: 'Sim', 0: 'Não'})


    col1,col2,col3,col4 = st.columns(4)
    with col1:
        with st.popover("Filtro mês"):
            filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes','Selecione os meses que gostaria de visualizar', key='filtro_mes_quebra_inscricoes')
            engajamento_detalhado_filtrado_quebra = aplicar_filtro(engajamento_detalhado_filtrado, 'mes',filtro_mes_grafico_inscricoes)

    participacao_por_eventos = plot_barra_empilhada_percentual(
        engajamento_detalhado_filtrado_quebra,
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
                #criando multislect de mes e nome do evento para gráficos dessa parte
                filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes','Selecione os meses que gostaria de visualizar',key='outros_graficos')
                filtro_eventos_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'nome_evento','Selecione os meses que gostaria de visualizar')
                
                #aploicando filtro de mes e nome do evento
                engajamento_detalhado_filtrado_quebra_outros = aplicar_filtro(engajamento_detalhado_filtrado, 'mes',filtro_mes_grafico_inscricoes)
                engajamento_detalhado_filtrado_quebra_outros = aplicar_filtro(engajamento_detalhado_filtrado_quebra_outros, 'nome_evento',filtro_eventos_grafico_inscricoes)

        participacao_por_genero = plot_barra_empilhada_percentual(
            engajamento_detalhado_filtrado_quebra_outros,
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
            engajamento_detalhado_filtrado_quebra_outros,
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
            engajamento_detalhado_filtrado_quebra_outros,
            coluna_grupo='Area_Atual',
            coluna_categoria='participou?',
            titulo="PARTICIPAÇÃO POR ÁREA DE FORMAÇÃO",
            altura=400,
            cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
            ordem_categorias=["Sim", "Não"],
            orientacao='vertical',
            ordem_grupos_alfabetica_invertida=True
        )

        participacao_por_tempo_formacao= plot_barra_empilhada_percentual(
            engajamento_detalhado_filtrado_quebra_outros,
            coluna_grupo='Classificacao_tempo_de_formacao',
            coluna_categoria='participou?',
            titulo="PARTICIPAÇÃO POR TEMPO DE FORMAÇÃO",
            altura=400,
            cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
            ordem_categorias=["Sim", "Não"],
            orientacao='vertical',
            ordem_grupos = ["Recém formado", "De 1 a 3 anos", "De 4 a 6 anos", "De 7 a 9 anos", "A partir de 10 anos"]
            )


        participacao_por_programa_entrada = plot_barra_empilhada_percentual(
            engajamento_detalhado_filtrado_quebra_outros,
            coluna_grupo='Programa_Entrada',
            coluna_categoria='participou?',
            titulo="PARTICIPAÇÃO POR ÁREA DE FORMAÇÃO",
            altura=400,
            cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
            ordem_categorias=["Sim", "Não"],
            orientacao='vertical',

        )

        participacao_por_praca_eb = plot_barra_empilhada_percentual(
            engajamento_detalhado_filtrado_quebra_outros,
            coluna_grupo='Praça_Agrupado',
            coluna_categoria='participou?',
            titulo="PARTICIPAÇÃO POR PRAÇA DE ENTRADA",
            altura=400,
            cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
            ordem_categorias=["Sim", "Não"],
            orientacao='vertical',
        )


         #st.columns feito dessa forma para dar um espaço (0.5) e uma coluna e outra
        col1,col2, col3 = st.columns([2, 0.5,2])
        with col1:
            st.plotly_chart(participacao_por_genero, use_container_width=True)
            st.divider()
            st.plotly_chart(participacao_por_area_formacao, use_container_width=True)
            st.divider()
            st.plotly_chart(participacao_por_programa_entrada, use_container_width=True)

        with col3:
            st.plotly_chart(participacao_por_raca, use_container_width=True)
            st.divider()
            st.plotly_chart(participacao_por_tempo_formacao, use_container_width=True)
            st.divider()
            st.plotly_chart(participacao_por_praca_eb, use_container_width=True)


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
            filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes','Selecione os meses que gostaria de visualizar', key='horas_totais')
            engajamento_detalhado_filtrado_hrs = aplicar_filtro(engajamento_detalhado_filtrado, 'mes',filtro_mes_grafico_inscricoes)


    horas_totais_participacao_por_eventos =  grafico_barras(
        engajamento_detalhado_filtrado_hrs,
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
                filtro_mes_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'mes','Selecione os meses que gostaria de visualizar',key='horas_totais_outros_graficos')
                filtro_eventos_grafico_inscricoes = selecionar_filtro(engajamento_detalhado_filtrado,'nome_evento','Selecione os meses que gostaria de visualizar', key ='horas_totais_outros_graficos_nome_evento')
                engajamento_detalhado_filtrado_hrs_outros = aplicar_filtro(engajamento_detalhado_filtrado, 'mes',filtro_mes_grafico_inscricoes)
                engajamento_detalhado_filtrado_hrs_outros = aplicar_filtro(engajamento_detalhado_filtrado_hrs_outros, 'nome_evento',filtro_eventos_grafico_inscricoes)

        horas_totais_por_genero =  grafico_barras(
            engajamento_detalhado_filtrado_hrs_outros,
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
            engajamento_detalhado_filtrado_hrs_outros,
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
            engajamento_detalhado_filtrado_hrs_outros,
            "Area_Atual",
            f"{nome_grafico} POR ÁREA DE FORMAÇÃO",
            cores=['#002561'],
            template='plotly_white',
            bg_color='rgba(0,0,0,0)',
            ordem_categorias='maior_menor',  
            tipo_agregacao=tipo_agregacao,  
            coluna_valor=coluna_valor  
        )

        horas_totais_por_tempo_formacao =  grafico_barras(
            engajamento_detalhado_filtrado_hrs_outros,
            "Classificacao_tempo_de_formacao",
            f"{nome_grafico} POR TEMPO DE FORMAÇÃO",
            cores=['#002561'],
            template='plotly_white',
            bg_color='rgba(0,0,0,0)',
            tipo_agregacao=tipo_agregacao,  
            coluna_valor=coluna_valor,
            ordem_categorias=["Recém formado", "De 1 a 3 anos", "De 4 a 6 anos", "De 7 a 9 anos", "A partir de 10 anos"]
        )

        horas_totais_por_programa_entrada =  grafico_barras(
            engajamento_detalhado_filtrado_hrs_outros,
            "Programa_Entrada",
            f"{nome_grafico} POR ÁREA DE FORMAÇÃO",
            cores=['#002561'],
            template='plotly_white',
            bg_color='rgba(0,0,0,0)',
            ordem_categorias='maior_menor',  
            tipo_agregacao=tipo_agregacao,  
            coluna_valor=coluna_valor  
        )

        horas_totais_por_praca_eb =  grafico_barras(
            engajamento_detalhado_filtrado_hrs_outros,
            "Praça_Agrupado",
            f"{nome_grafico} POR ÁREA DE FORMAÇÃO",
            cores=['#002561'],
            template='plotly_white',
            bg_color='rgba(0,0,0,0)',
            ordem_categorias='maior_menor',  
            tipo_agregacao=tipo_agregacao,  
            coluna_valor=coluna_valor  
        )

         #st.columns feito dessa forma para dar um espaço (0.5) e uma coluna e outra
        col1,col2, col3 = st.columns([2, 0.5,2])
        with col1:
            st.plotly_chart(horas_totais_por_genero, use_container_width=True)
            st.divider()
            st.plotly_chart(horas_totais_por_area_atual, use_container_width=True)
            st.divider()
            st.plotly_chart(horas_totais_por_programa_entrada, use_container_width=True)
        with col3:
            st.plotly_chart(horas_totais_por_raca, use_container_width=True)
            st.divider()
            st.plotly_chart(horas_totais_por_tempo_formacao, use_container_width=True)
            st.divider()
            st.plotly_chart(horas_totais_por_praca_eb, use_container_width=True)