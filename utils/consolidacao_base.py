# %%
import pandas as pd
from datetime import datetime
import numpy as np


# %%
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# %%
#exportando bases
eventos = pd.read_excel(r'I:\PROJETOS\ALUMNI\07. Acompanhamento de metas\Registros engajamento e giveback.xlsx', sheet_name='evento')
participacao = pd.read_excel(r'I:\PROJETOS\ALUMNI\07. Acompanhamento de metas\Registros engajamento e giveback.xlsx', sheet_name='participacao')
pesquisa_alumni = pd.read_excel(r'I:\PROJETOS\ALUMNI\07. Acompanhamento de metas\pesquisa_alumni_tratada_2023-2024.xlsx')
status = pd.read_excel(r'I:\PROJETOS\ENSINO_SUPERIOR\3. Base de Dados\2025\Status_Universitários\Status 2025_PARA_CONSULTA.xlsx')
tabelas_interesses_status =  pd.read_excel(r'I:\PROJETOS\ALUMNI\07. Acompanhamento de metas\colunas_relevantes_status.xlsx')
mentoria_base_geral = pd.read_excel(r'I:\PROJETOS\ALUMNI\07. Acompanhamento de metas\Registros_Mentoria.xlsx', sheet_name='Base_Mentoria')
mentoria_desistências = pd.read_excel(r'I:\PROJETOS\ALUMNI\07. Acompanhamento de metas\Registros_Mentoria.xlsx', sheet_name='Desistências')
mentoria_registros_sessoes = pd.read_excel(r'I:\PROJETOS\ALUMNI\07. Acompanhamento de metas\Registros_Mentoria.xlsx', sheet_name='Registros_sessões')

# %%
#transformando colunas de interesses em lista e filtrando status com ela
tabelas_interesses = tabelas_interesses_status['tabelas_de_interesses'].unique().tolist()
status_filtrada = status[tabelas_interesses]

# %%
#renomeando coluna ID

status_filtrada = status_filtrada.rename(columns={'ID': 'RA'})

# %%
#filtrando status para pegar apenas alumni e pesquisa de graduados para pegar apenas 2024
status_filtrada_alumni = status_filtrada[status_filtrada['Status_real'] == 'FORMADO']
pesquisa_alumni_2024 = pesquisa_alumni[pesquisa_alumni['Ano'] == 2024]

# %%
#adicionando coluna mes MM/AAAA na tabela de eventos
eventos['mes'] = eventos['data_termino'].dt.strftime('%m/%Y')


# %%
# unificando participação dos eventos com a descrição dos meses
eventos_consolidacao = pd.merge(participacao, eventos, on='id_evento',how="left")
# unificando status com dados da pesquisa alumni
base_final_consolidada = pd.merge(status_filtrada_alumni, pesquisa_alumni_2024, on='RA', how ='left')

# %%
# criando coluna de tempo de formação
ano_atual = datetime.now().year
base_final_consolidada['Tempo de formado'] = ano_atual - base_final_consolidada['Ano_Termino_Curso_Atual']
status_filtrada['Tempo de formado'] = ano_atual - status_filtrada['Ano_Termino_Curso_Atual']
base_final_consolidada['Tempo de formado - Ref PA'] = (ano_atual-1) - base_final_consolidada['Ano_Termino_Curso_Atual']

# %%
#adicionando coluna que fala se o aluno respondeu ou não a última pesquisa
base_final_consolidada["Respondeu última pesquisa?"] = base_final_consolidada["Nome Completo"].notna().map({True: "Sim", False: "Não"})


# %%
#criando cluster de tempo de formação
def classificacao_tempo_formacao(tempo):
    if tempo == 0:
        return "Recém formado"
    elif 1 <= tempo <= 3:
        return "De 1 a 3 anos"
    elif 4 <= tempo <= 6:
        return "De 4 a 6 anos"
    elif 7 <= tempo <= 9:
        return "De 7 a 9 anos"
    elif tempo >= 10:
        return "A partir de 10 anos"

# Aplicando a função e criando a nova coluna
base_final_consolidada['Classificacao_tempo_de_formacao'] = base_final_consolidada['Tempo de formado'].apply(classificacao_tempo_formacao)
base_final_consolidada['Classificacao_tempo_de_formacao -  Ref PA'] = base_final_consolidada['Tempo de formado - Ref PA'].apply(classificacao_tempo_formacao)
status_filtrada['Classificacao_tempo_de_formacao'] = status_filtrada['Tempo de formado'].apply(classificacao_tempo_formacao)

# %%
#consolidando total de engajamento e giveback e concatenando com a base_consolidada

eventos_consolidados_agrupado_total =  eventos_consolidacao.pivot_table(
    index='ra',
    columns='tipo_participacao_aluno',
    values='horas_participadas',
    aggfunc='sum',
    fill_value=0
).reset_index()


eventos_consolidados_agrupado_total = eventos_consolidados_agrupado_total.rename(columns={
    'Giveback': 'horas_totais_giveback',
    'Engajamento': 'horas_totais_engajamento',
    'ra': 'RA'
})

eventos_consolidados_agrupado_total['horas_totais_participacao'] = eventos_consolidados_agrupado_total['horas_totais_giveback'] + eventos_consolidados_agrupado_total['horas_totais_engajamento'] 

eventos_consolidados_agrupado_total['10h+_giveback'] = (eventos_consolidados_agrupado_total['horas_totais_giveback'] >= 10).astype(int)
eventos_consolidados_agrupado_total['10h+_engajamento'] = (eventos_consolidados_agrupado_total['horas_totais_engajamento'] >= 10).astype(int)
eventos_consolidados_agrupado_total['10h+_participacao'] = (eventos_consolidados_agrupado_total['horas_totais_participacao'] >= 10).astype(int)


base_final_consolidada = pd.merge(base_final_consolidada, eventos_consolidados_agrupado_total, on='RA', how ='left')

# %%
eventos_consolidacao = eventos_consolidacao.rename(columns={
    'ra': 'RA'
})


#criando tabela mensal agrupando dados de engajamento 
eventos_agrupado = eventos_consolidacao.groupby(
    ['RA', 'mes', 'tipo_participacao_aluno'],
    as_index=False
)['horas_participadas'].sum()

eventos_agrupado = eventos_agrupado.sort_values(by=['RA', 'tipo_participacao_aluno', 'mes'])

eventos_agrupado['horas_participadas_acumuladas'] = (
    eventos_agrupado
    .groupby(['RA', 'tipo_participacao_aluno'])['horas_participadas']
    .cumsum()
)


eventos_agrupado['10h+'] = (eventos_agrupado['horas_participadas_acumuladas'] >= 10).astype(int)

eventos_pivotado = eventos_agrupado.pivot(
    index=['RA', 'mes'],
    columns='tipo_participacao_aluno',
    values=['horas_participadas', 'horas_participadas_acumuladas', '10h+']
).fillna(0)


eventos_pivotado.columns = [
    f"{col[0]}_{col[1].lower()}" for col in eventos_pivotado.columns
]


eventos_pivotado = eventos_pivotado.reset_index()

eventos_pivotado = eventos_pivotado.rename(columns={
    'horas_participadas_engajamento': 'horas_totais_engajamento',
    'horas_participadas_giveback': 'horas_totais_giveback',
    'horas_participadas_acumuladas_engajamento': 'horas_acumuladas_engajamento',
    'horas_participadas_acumuladas_giveback': 'horas_acumuladas_giveback',
    '10h+_engajamento': '10h+_engajamento',
    '10h+_giveback': '10h+_giveback'
})


eventos_pivotado['horas_totais_somados'] = (
    eventos_pivotado['horas_totais_engajamento'] + eventos_pivotado['horas_totais_giveback']
)


eventos_pivotado['horas_totais_somados_acumulados'] = (
    eventos_pivotado
    .sort_values(['RA', 'mes'])
    .groupby('RA')['horas_totais_somados']
    .cumsum()
)


eventos_pivotado['10h+totais'] = (eventos_pivotado['horas_totais_somados_acumulados'] >= 10).astype(int)




# %%
# 1. Extrai os meses únicos já no formato correto
meses = eventos_pivotado['mes'].drop_duplicates().sort_values().reset_index(drop=True)

# 2. Cria um DataFrame com esses meses
df_meses = pd.DataFrame({'mes': meses})

# 3. Adiciona uma coluna auxiliar em cada DataFrame para o cross join
status_filtrada_alumni['key'] = 1
df_meses['key'] = 1

# 4. Faz o cross join
status_alumni_mensal = pd.merge(status_filtrada_alumni, df_meses, on='key').drop(columns='key')
status_alumni_mensal['RA+Mês'] = status_alumni_mensal['RA'].astype(str) + status_alumni_mensal['mes'] 
eventos_pivotado['RA+Mês'] = eventos_pivotado['RA'].astype(str) + eventos_pivotado['mes']

eventos_pivotado.drop(['RA', 'mes'], axis=1, inplace=True)

eventos_consolidados_agrupado_mes = pd.merge(status_alumni_mensal,eventos_pivotado, on='RA+Mês', how ='left')

#adicionando coluna tempo de formação e a classificação 
eventos_consolidados_agrupado_mes['Tempo de formado'] = ano_atual - eventos_consolidados_agrupado_mes['Ano_Termino_Curso_Atual']
eventos_consolidados_agrupado_mes['Classificacao_tempo_de_formacao'] = eventos_consolidados_agrupado_mes['Tempo de formado'].apply(classificacao_tempo_formacao)


# %%
#adicionando outras colunas na tabela de eventos detalhados

#criei a variavel status_alumni_merge_eventos e criei a coluna RA + MES para fazer o merge com ela, assim eu apaguei as colunas RA e MES da status_alumni para não duplicar ela pq são são colunas que já existem na eventos_Consolidado


status_alumni_merge_eventos = status_alumni_mensal

status_alumni_merge_eventos['RA+Mês'] = status_alumni_merge_eventos['RA'].astype(str) + status_alumni_merge_eventos['mes'] 
eventos_consolidacao['RA+Mês'] = eventos_consolidacao['RA'].astype(str) + eventos_consolidacao['mes']

status_alumni_merge_eventos.drop(['RA', 'mes'], axis=1, inplace=True)


eventos_consolidacao = pd.merge(eventos_consolidacao, status_alumni_merge_eventos ,on='RA+Mês', how ='left')

#incluindo tempo de formação na eventos consolidação
eventos_consolidacao['Tempo de formado'] = ano_atual - eventos_consolidacao['Ano_Termino_Curso_Atual']

# %%
#consolidando na tabela de registros de sessoes a descrição dos eventos
mentoria_registros_sessoes = pd.merge(mentoria_registros_sessoes, eventos, on='id_evento', how='left')


#contando quantas sessoes cada mentoria teve e gerando uma tabela com isso
sessoes_totais = mentoria_registros_sessoes.groupby('nome_evento')['id_evento'].nunique().reset_index()

# renomenando nome dessas tabelas
sessoes_totais.columns = ['nome_evento', 'sessoes_totais']

#pivotando tabela para que o registro de participacao de cada mes seja uma coluna
mentoria_registros_sessoes_agrupado = mentoria_registros_sessoes.pivot_table(
    index=['RA', 'nome_evento'],
    columns='mes',
    values='realizacao',
    aggfunc='sum',
    fill_value=0
).reset_index()

#renomeando colunas de meses, mantendo apenas RA e nome_evento sem o prefixo "participacao_sessao"
novas_colunas = ['RA', 'nome_evento'] + [f'participacao_sessao_{col}' for col in mentoria_registros_sessoes_agrupado.columns[2:]]
mentoria_registros_sessoes_agrupado.columns = novas_colunas

#fazendo merge para ter a coluna "sessoes_Totais" na tabela
mentoria_registros_sessoes_agrupado = pd.merge(mentoria_registros_sessoes_agrupado, sessoes_totais, on='nome_evento', how='left')
mentoria_registros_sessoes_agrupado

#mapeando colunas que tem participacao e somando participacao total de cada mentorado com a coluna "sessoes_feitas"
col_participacao = [col for col in mentoria_registros_sessoes_agrupado.columns if col.startswith('participacao_sessao_')]
mentoria_registros_sessoes_agrupado['sessoes_feitas'] = mentoria_registros_sessoes_agrupado[col_participacao].sum(axis=1)

#criando coluna engajamento
mentoria_registros_sessoes_agrupado['engajamento_mentoria'] = (
    mentoria_registros_sessoes_agrupado['sessoes_feitas'] / mentoria_registros_sessoes_agrupado['sessoes_totais']
)




# %%
#criando "ID" ra + nome_mentoria para garantir consistência no merge, ou seja esteja puxando dados da mentoria correra

mentoria_base_geral['RA_nome_mentoria'] = mentoria_base_geral['RA'].astype(str) + mentoria_base_geral['nome_evento']
mentoria_registros_sessoes_agrupado['RA_nome_mentoria'] = mentoria_registros_sessoes_agrupado['RA'].astype(str) + mentoria_registros_sessoes_agrupado['nome_evento']

mentoria_registros_sessoes_agrupado.drop('RA', axis=1, inplace=True)
mentoria_registros_sessoes_agrupado.drop('nome_evento', axis=1, inplace=True)

# %%
#agrupando dados gerais da mentoria, desistencias e infos da status na base de registros empilhadas

mentoria_registros_sessoes = pd.merge(mentoria_registros_sessoes, mentoria_base_geral, on='RA', how='left')
mentoria_registros_sessoes = pd.merge(mentoria_registros_sessoes, mentoria_desistências, on='RA', how='left')
mentoria_registros_sessoes = pd.merge(mentoria_registros_sessoes, status_filtrada, on='RA', how='left')

#agrupando dados de registros agrupados e da status na base consolidada

#como o nome já existe na tabela de mentoria consolidado estou removendo da de eventos para não duplicar

mentoria_base_geral_consolidado = pd.merge(mentoria_base_geral, mentoria_registros_sessoes_agrupado, on='RA_nome_mentoria', how='left')
mentoria_base_geral_consolidado.drop('RA_nome_mentoria', axis=1, inplace=True)
mentoria_base_geral_consolidado = pd.merge(mentoria_base_geral_consolidado, mentoria_desistências, on='RA', how='left')
mentoria_base_geral_consolidado = pd.merge(mentoria_base_geral_consolidado, status_filtrada, on='RA', how='left')


# %%
#calculando status mentoria

# Defina as condições
condicoes = [
    mentoria_base_geral_consolidado['motivo_desistencias_agrupado'].notna(),  # Desistente
    (mentoria_base_geral_consolidado['engajamento_mentoria'].isna()) | (mentoria_base_geral_consolidado['engajamento_mentoria'] == 0),  # Desengajado
    (mentoria_base_geral_consolidado['engajamento_mentoria'] > 0) & (mentoria_base_geral_consolidado['engajamento_mentoria'] <= 0.75),  # Participacao parcial
    (mentoria_base_geral_consolidado['engajamento_mentoria'] > 0.75)  # Participacao total
]

# Defina os valores correspondentes
valores = [
    'Desistente',
    'Desengajado',
    'Participacao parcial',
    'Participacao total'
]

# Crie a nova coluna
mentoria_base_geral_consolidado['status_mentoria'] = np.select(condicoes, valores, default=np.nan)

# %%
# Define a função para classificar o status da meta
def classificar_meta(coluna):
    return np.select(
        [
            coluna >= 10,
            (coluna > 0) & (coluna < 5),
            (coluna > 4) & (coluna < 10),
            (coluna < 1) | (coluna.isna())
        ],
        [
            'Alto engajamento',
            'Baixo engajamento',
            'Engajamento mediano',
            'Sem engajamento'
        ]
    )

# Aplica a lógica para cada tipo
eventos_consolidados_agrupado_mes['status_meta_engajamento'] = classificar_meta(eventos_consolidados_agrupado_mes['horas_acumuladas_engajamento'])
eventos_consolidados_agrupado_mes['status_meta_giveback'] = classificar_meta(eventos_consolidados_agrupado_mes['horas_acumuladas_giveback'])
eventos_consolidados_agrupado_mes['status_meta_total'] = classificar_meta(eventos_consolidados_agrupado_mes['horas_totais_somados_acumulados'])

base_final_consolidada['status_meta_engajamento'] = classificar_meta(base_final_consolidada['horas_totais_engajamento'])
base_final_consolidada['status_meta_giveback'] = classificar_meta(base_final_consolidada['horas_totais_giveback'])
base_final_consolidada['status_meta_total'] = classificar_meta(base_final_consolidada['horas_totais_participacao'])


# %%
#adicionando "tempo de formação na tabela eventos_consolidadas"

eventos_consolidacao['Classificacao_tempo_de_formacao'] = eventos_consolidacao['Tempo de formado'].apply(classificacao_tempo_formacao)

# %%
eventos_consolidacao.to_excel(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\eventos_consolidados_detalhado.xlsx', index=False)
base_final_consolidada.to_excel(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\base_final_consolidada.xlsx', index=False)
pesquisa_alumni.to_excel(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\pesquuisa_alumni.xlsx', index=False)
eventos_consolidados_agrupado_mes.to_excel(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\eventos_consolidados_por_mes.xlsx', index=False)
mentoria_base_geral_consolidado.to_excel(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\mentoria_consolidado.xlsx', index=False)
mentoria_registros_sessoes.to_excel(r'C:\Users\mcerqueira\Documents\Streamlit\alumni_dash\bases\mentoria_registros_sessoes.xlsx', index=False)



