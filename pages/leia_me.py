import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from utils.funcoes import *
import base64



st.subheader("Bem-vindo(a) ao dash do alumni Ismart", divider='blue')

st.markdown("**Utilize a barra lateral para navegar entre as páginas:**")


st.subheader("Resumo das páginas")

st.markdown("**Dados Gerais:** contém dados principais como área de formação, praça, tempo de formação. Além de conter uma visualização focada na Pesquisa Alumni de 2024.")
st.markdown("**Engajamento e Giveback:** dados consolidados de horas de engajamento em 2025, destacando alunos que atingiram a meta de 10h+ de giveback e engajamento.")
st.markdown("**Mentoria:** página focada no acompanhanento das mentorias, sendo PGP ou Ismart. Lembrando que as horas de mentoria também contabilizam dentro de engajamento e giveback")
st.markdown("**Download de bases:** por essa página é possível fazer download de todas as bases que irão conter dados de todas as outras páginas citadas")



st.subheader("Atualizações")

st.markdown("**Estrutural:** última atualização na estrutura das páginas foram feitas no dia 19/05/2025, data da criação do mesmo.")
st.markdown("**Atualização dos dados:** sem definição da periodicidade")

st.subheader("Contato para dúvidas, sugestões e reports de erros:")

st.markdown("marcos.cerqueira@ismart.org.br")
st.markdown("alex.oliveira@ismart.org.br")
st.markdown("livia.sousa@ismart.org.br")
st.markdown("william.santos@ismart.org.br")
st.markdown("felipe.amaral@ismart.org.br")
