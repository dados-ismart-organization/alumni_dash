import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from utils.funcoes import *
import base64
from io import BytesIO

exibir_banner('painel/download_bases.png', altura_px=100)

base_consolidada= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\base_final_consolidada.xlsx', tipo='excel')
engajamento_mensal= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\eventos_consolidados_por_mes.xlsx', tipo='excel')
engajamento_detalhado= importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\eventos_consolidados_detalhado.xlsx', tipo='excel')
mentoria_consolidado = importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\mentoria_consolidado.xlsx', tipo='excel')
mentoria_registros = importar_base(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\mentoria_registros_sessoes.xlsx', tipo='excel')


#dando espaço no expander e no banner
st.write('')
st.write('')
st.write('')

with st.expander("Descrição bases"):
    st.write("**Base geral:** Lista com todos os alumni, incluindo informações de status, soma dos indicadores de engajamento e giveback, além de dados de empregabilidade (caso tenha respondido à última pesquisa).")
    st.write("**Engajamento mensal:** Engajamento do aluno é consolidada mas por mês, ou seja cada aluno se repetirá para cada mês.")
    st.write("**Engajamento detalhado:** Registros de engajamento e giveback detalhados. Cada linha é um aluno em um evento.")
    st.write("**Mentoria consolidado:** Resumo da mentoria: participantes e suas informações além de consolidado de participação")
    st.write("**Mentoria participação das sessões:** Registro de participações por sessão, em cada linha a informação se o aluno participou ou não")



opcao_base = st.radio(
    "Escolha qual base você quer baixar:",
    ("Base geral", "Engajamento mensal", "Engajamento detalhado", "Mentoria consolidado","Mentoria participação das sessões")
)


if opcao_base == "Base geral":
    base = base_consolidada
elif opcao_base == "Engajamento mensal":
    base = engajamento_mensal
elif opcao_base == "Engajamento detalhado":
    base = engajamento_detalhado
elif opcao_base == "Mentoria consolidado":
    base = mentoria_consolidado
else:
    base = mentoria_registros


st.markdown("#### Escolha as colunas que deseja manter na tabela. Caso contrário, todas serão mantidas por padrão.")
with st.popover("Filtrar colunas"):
    colunas_tabelas = st.multiselect(
        "Selecionar colunas",
        base.columns.tolist(),
        default=base.columns.tolist()
    )
    base = base[colunas_tabelas]

st.markdown("#### Aplique filtros selecionando uma ou mais colunas e os valores correspondentes")

with st.expander("Selecionar filtros"):
    colunas_para_filtrar = st.multiselect(
        "Escolha as colunas para aplicar filtros", base.columns
    )

    for coluna in colunas_para_filtrar:
        valores = st.multiselect(
            f"Filtrar valores da coluna '{coluna}'",
            options=base[coluna].dropna().unique().tolist(),
            key=f"filtro_{coluna}"
        )
        if valores:
            base = base[base[coluna].isin(valores)]



st.markdown("#### Visualizar e baixar base")

with st.expander("**Clique aqui para visualizar a base:**"):
    base

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Alumni')
    processed_data = output.getvalue()
    return processed_data


excel_data = to_excel(base)


st.download_button(
    label="📥 Baixar base",
    data=excel_data,
    file_name='Base dash alumni.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
