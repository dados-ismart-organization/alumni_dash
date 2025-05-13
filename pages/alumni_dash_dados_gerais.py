import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from funcoes import *
import base64

exibir_banner('painel/dados_gerais.png', altura_px=100)


base_consolidada= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\base_final_consolidada.xlsx', tipo='excel')

st.subheader("Dados Gerais", divider='blue')

#azul1, azul2, azul3, azul4, azul alumni, roxinho, rosa choque, rosa claro, amarelo, verde

#colors = ['#D4EFFC','#9DDCF9','#00BDF2', '#008ED4',  '#002561','#924A7C', '#EE2D67','#F2665E', '#EBEA70','#8EC6B2']

with st.sidebar:
    st.divider()
    st.subheader('Selecione seus filtros:')
    with st.popover("Filtros"):
        filtro_area_atual = selecionar_filtro(base_consolidada,'Area_Atual','Selecione a área de formação')
        base_consolidada_filtrada = aplicar_filtro(base_consolidada, 'Area_Atual',filtro_area_atual)


## Tratamentos#
# contando quantos alumni tem na base
total_alumni = base_consolidada_filtrada['RA'].count()
#transformando tempo de formação em STR para corrigir bug do gráfico


st.metric("Alumni ativos", total_alumni)

alumni_genero = grafico_barras(
    df=base_consolidada_filtrada,
    coluna_x='Gênero',
    nome_grafico='ALUMNI POR GÊNERO',
    cores=['#002561'],
    ordem_categorias="alfabetica"
)

alumni_raca = grafico_barras(
    df=base_consolidada_filtrada,
    coluna_x='Cor_raça',
    nome_grafico='ALUMNI POR RAÇA',
    cores=['#002561'],
    ordem_categorias="alfabetica"
)

alumni_area_formacao = grafico_barras(
    df=base_consolidada_filtrada,
    coluna_x='Area_Atual',
    nome_grafico='ALUMNI POR ÁREA DE FORMAÇÃO',
    cores=['#002561'],
    ordem_categorias=None
)


col1, col2, col3 = st.columns([2, 0.4, 2])

with col1:
    st.plotly_chart(alumni_genero, use_container_width=True)
    st.divider()
    #st.write para pular espaço e alinhar os gráficos da "segunda linha"
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.plotly_chart(alumni_area_formacao, use_container_width=True)

#with col2:
    #st.markdown("""<div style="height: 1050px; border-left: 2px solid grey; margin: auto;"></div>""", unsafe_allow_html=True)

with col3: 
    st.plotly_chart(alumni_raca, use_container_width=True)
    st.divider()

    opcao_grafico_tempo = st.radio(
    "Escolha o tipo de visualização:",
    ("Ano_Termino_Curso_Atual", "Classificacao_tempo_de_formacao"), horizontal=True
)
    
    #poderia colocar a variacal opcao_grafico_tempo direto na coluna_x mas como precisava por o ordem_categorias no tempo de formação fiz com IF
    if opcao_grafico_tempo == "Ano_Termino_Curso_Atual":  
        alumni_tempo_formado = grafico_barras(
            df=base_consolidada_filtrada,
            coluna_x= "Ano_Termino_Curso_Atual",
            nome_grafico=f'ALUMNI POR ANO DE FORMAÇÃO',
            cores=['#002561'],
            ordem_categorias=None
        )
    else:
        alumni_tempo_formado = grafico_barras(
            df=base_consolidada_filtrada,
            coluna_x= "Classificacao_tempo_de_formacao",
            nome_grafico=f'ALUMNI POR TEMPO DE FORMAÇÃO',
            cores=['#002561'],
            ordem_categorias=["Recém formado", "De 1 a 3 anos", "De 4 a 6 anos", "De 7 a 9 anos", "A partir de 10 anos"]
        )

    st.plotly_chart(alumni_tempo_formado, use_container_width=True)

with st.expander("Gráfico curso e Universidade"):
    top_cursos = (
        base_consolidada_filtrada['Curso_Detalhado_Atual']
        .value_counts()
        .head(10)
        .index
    )

    df_top_cursos = base_consolidada_filtrada[
        base_consolidada_filtrada['Curso_Detalhado_Atual'].isin(top_cursos)
    ]

    alumni_curso_formacao = grafico_barras(
        df=df_top_cursos,
        coluna_x='Curso_Agregado_Atual',
        nome_grafico='TOP 10 CURSOS - ALUMNI',
        cores=['#002561'],
        ordem_categorias="maior_menor"
    )
    st.plotly_chart(alumni_curso_formacao, use_container_width=True)

    top_unis = (
        base_consolidada_filtrada['Universidade_Detalhado_Atual']
        .value_counts()
        .head(10)
        .index
    )

    df_top_unis = base_consolidada_filtrada[
        base_consolidada_filtrada['Universidade_Detalhado_Atual'].isin(top_unis)
    ]

    alumni_universidade_formacao = grafico_barras(
        df=df_top_unis,
        coluna_x='Universidade_Detalhado_Atual',
        nome_grafico='TOP 10 UNIVERSIDADES - ALUMNI',
        cores=['#002561'],
        ordem_categorias="maior_menor"
    )
    st.plotly_chart(alumni_universidade_formacao, use_container_width=True)
st.subheader("Dados Empregabilidade", divider='blue')

#total respondentes pesquisa
base_respondentes_pesquisa_filtrado =  base_consolidada_filtrada[base_consolidada_filtrada['Respondeu última pesquisa?'] == "Sim"]
total_respondentes = base_respondentes_pesquisa_filtrado['Respondeu última pesquisa?'].count()




st.metric(
    label="Respondentes pesquisa alumni",
    value=f"{total_respondentes} alunos",
)


destaques_tipo_carreira = plot_barra_empilhada_percentual(
    base_respondentes_pesquisa_filtrado,
    coluna_grupo="Carreira - nova referência",
    coluna_categoria="Destaque? 10%+ parametrizado",
    titulo="DESTAQUES POR TIPO DE CARREIRA",
    cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
    ordem_categorias=["Sim", "Não"],
    ordem_grupos=["Exterior", "C", "B", "A"] 
)

destaques_tempo_formado = plot_barra_empilhada_percentual(
    base_respondentes_pesquisa_filtrado,
    coluna_grupo="Classificacao_tempo_de_formacao",
    coluna_categoria="Destaque? 10%+ parametrizado",
    titulo="DESTAQUES POR TEMPO DE FORMAÇÃO",
    cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
    ordem_categorias=["Sim", "Não"],
    ordem_grupos=["A partir de 10 anos", "De 7 a 9 anos", "De 4 a 6 anos", "De 1 a 3 anos", "Recém formado"] 
)


destaques_carreira = plot_barra_empilhada_percentual(
    base_respondentes_pesquisa_filtrado,
    coluna_grupo="Classificação_Corrigido",
    coluna_categoria="Destaque? 10%+ parametrizado",
    titulo="DESTAQUES POR CARREIRA",
    cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
    ordem_categorias=["Sim", "Não"],
    ordem_grupos_alfabetica_invertida=False,  
    altura = 500,
    orientacao = 'vertical'
)


col1, col2 = st.columns (2)

with col1:
    st.plotly_chart(destaques_tipo_carreira, use_container_width=True)
    

with col2:
    st.plotly_chart(destaques_tempo_formado, use_container_width=True)


st.plotly_chart(destaques_carreira, use_container_width=True)


with st.expander('Mais visualização por status empregabilidade'):
    destaques_genero = plot_barra_empilhada_percentual(
        base_respondentes_pesquisa_filtrado,
        coluna_grupo="Gênero",
        coluna_categoria="Destaque? 10%+ parametrizado",
        titulo="DESTAQUES POR GÊNERO",
        cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
        ordem_categorias=["Sim", "Não"],
        ordem_grupos_alfabetica_invertida=False,
        orientacao='vertical'  
    )
    destaques_por_raca = plot_barra_empilhada_percentual(
        base_respondentes_pesquisa_filtrado,
        coluna_grupo="Cor_raça",
        coluna_categoria="Destaque? 10%+ parametrizado",
        titulo="DESTAQUES POR RAÇA",
        cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
        ordem_categorias=["Sim", "Não"],
        ordem_grupos_alfabetica_invertida=False,
        orientacao='vertical'  
    )
    destaques_por_area_formacao = plot_barra_empilhada_percentual(
        base_respondentes_pesquisa_filtrado,
        coluna_grupo='Area_Atual',
        coluna_categoria="Destaque? 10%+ parametrizado",
        titulo="DESTAQUES POR ÁREA ATUAL",
        cor_categoria={"Sim": "#002561", "Não": "#C4ECFF"},
        ordem_categorias=["Sim", "Não"],
        ordem_grupos_alfabetica_invertida=False,
        orientacao='vertical'  
    )
    col1, col2 = st.columns (2)

    with col1:
        st.plotly_chart(destaques_genero, use_container_width=True)
        st.divider()
    with col2:
        st.plotly_chart(destaques_por_raca, use_container_width=True)
        st.divider()
    st.plotly_chart(destaques_por_area_formacao, use_container_width=True)



tipos_carreiras = base_respondentes_pesquisa_filtrado['Carreira - nova referência'].unique()
tipos_carreira = st.selectbox('Selecione carreira:', tipos_carreiras)
base_respondentes_pesquisa_filtrado_carreira = base_respondentes_pesquisa_filtrado[base_respondentes_pesquisa_filtrado['Carreira - nova referência'] == tipos_carreira]

plotagem_graduados = plot_scatter_generico_plotly(
    df= base_respondentes_pesquisa_filtrado_carreira,
    coluna_x='Tempo de formado',
    coluna_y='Remuneração 10%+',
    coluna_linha_referencia='Remuneração Esperada',
    coluna_categoria='Reclassificação final',
    coluna_nome_pessoa='NOME_SEM_ACENTO_MAIUSCULO ',
    label_linha_referencia='Remuneração Esperada',
    titulo='REMUNERAÇÃO POR TEMPO DE FORMAÇÃO',
    label_x='Tempo de Formação',
    label_y='Salário'
)
st.plotly_chart(plotagem_graduados, use_container_width=True)
