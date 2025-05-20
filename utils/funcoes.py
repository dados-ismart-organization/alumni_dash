import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#@st.cache_data()
st.cache_data.clear()
def importar_base(caminho, tipo='csv', **kwargs):
    """
    Importa uma base de dados do tipo CSV ou Excel.

    Parâmetros:
    - caminho (str): Caminho para o arquivo.
    - tipo (str): 'csv' ou 'excel'. Padrão: 'csv'.
    - **kwargs: Argumentos adicionais passados para pd.read_csv ou pd.read_excel.

    Retorna:
    - DataFrame pandas com os dados importados.
    """
    if tipo == 'csv':
        return pd.read_csv(caminho, **kwargs)
    elif tipo == 'excel':
        return pd.read_excel(caminho, **kwargs)
    else:
        raise ValueError("Tipo de arquivo não suportado. Use 'csv' ou 'excel'.")
    
def grafico_barras(
    df,
    coluna_x,
    nome_grafico,
    cores=None,
    template='plotly_white',
    bg_color='rgba(0,0,0,0)',
    ordem_categorias=None,  # 'alfabetica', 'maior_menor' ou lista
    tipo_agregacao='contagem',  # 'contagem' ou 'soma'
    coluna_valor=None  # necessária se tipo_agregacao == 'soma'
):
    if tipo_agregacao == 'soma':
        if coluna_valor is None:
            raise ValueError("Você deve fornecer 'coluna_valor' quando usar tipo_agregacao='soma'")
        df_agg = df.groupby(coluna_x)[coluna_valor].sum().reset_index()
        df_agg.columns = [coluna_x, 'quantidade']
    else:  # padrão: contagem
        df_agg = df[coluna_x].value_counts().reset_index()
        df_agg.columns = [coluna_x, 'quantidade']

    # Definir ordem das categorias
    if ordem_categorias == 'alfabetica':
        ordem_categorias = sorted(df_agg[coluna_x].unique())
    elif ordem_categorias == 'maior_menor':
        ordem_categorias = df_agg.sort_values('quantidade', ascending=False)[coluna_x].tolist()
    elif isinstance(ordem_categorias, list):
        # Usa a ordem fornecida
        pass
    else:
        # Se None ou não reconhecida, usa ordem natural dos dados
        ordem_categorias = df_agg[coluna_x].tolist()

    fig = px.bar(
        df_agg,
        x=coluna_x,
        y='quantidade',
        text='quantidade',
        template=template,
        color_discrete_sequence=cores,
        category_orders={coluna_x: ordem_categorias}
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title=coluna_x,
        yaxis_title="Soma" if tipo_agregacao == 'soma' else "# Quantidade",
        plot_bgcolor=bg_color,
        title={
            'text': f"<b>{nome_grafico}</b>",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    fig.update_yaxes(visible=False, showticklabels=False)

    return fig

def plot_barra_empilhada_percentual(
    df,
    coluna_grupo,
    coluna_categoria,
    titulo="Gráfico de barras empilhadas (100%)",
    cor_categoria=None,
    ordem_categorias=None,
    ordem_grupos=None,
    ordem_categorias_alfabetica_invertida=False,
    ordem_grupos_alfabetica_invertida=False,
    altura=400,
    orientacao='horizontal'  # Novo parâmetro: 'horizontal' ou 'vertical'
):
    """
    Gráfico de barras empilhadas com proporções e rótulos absolutos.

    Parâmetros:
    - orientacao: 'horizontal' (padrão) ou 'vertical'
    """

    tabela_abs = df.pivot_table(
        index=coluna_grupo,
        columns=coluna_categoria,
        aggfunc='size',
        fill_value=0
    )

    tabela_pct = tabela_abs.div(tabela_abs.sum(axis=1), axis=0) * 100

    categorias = tabela_pct.columns.tolist()

    if ordem_categorias_alfabetica_invertida:
        categorias = sorted(categorias, reverse=True)
    elif ordem_categorias:
        categorias = [cat for cat in ordem_categorias if cat in categorias]

    grupos = tabela_pct.index.tolist()

    if ordem_grupos_alfabetica_invertida:
        grupos = sorted(grupos, reverse=True)
    elif ordem_grupos:
        tabela_pct.index = pd.Categorical(tabela_pct.index, categories=ordem_grupos, ordered=True)
        tabela_abs.index = pd.Categorical(tabela_abs.index, categories=ordem_grupos, ordered=True)
        tabela_pct = tabela_pct.sort_index()
        tabela_abs = tabela_abs.sort_index()
        grupos = tabela_pct.index.tolist()

    cores = cor_categoria or {}
    default_colors = ['#2ca02c', '#d62728', '#1f77b4', '#ff7f0e', '#9467bd']

    fig = go.Figure()

    for i, cat in enumerate(categorias):
        cor = cores.get(cat, default_colors[i % len(default_colors)])
        valores_pct = tabela_pct[cat].tolist()
        valores_abs = tabela_abs[cat].tolist()

        if orientacao == 'horizontal':
            fig.add_trace(go.Bar(
                y=grupos,
                x=valores_pct,
                name=str(cat),
                orientation='h',
                marker_color=cor,
                text=valores_abs,
                textposition='inside'
            ))
        else:
            fig.add_trace(go.Bar(
                x=grupos,
                y=valores_pct,
                name=str(cat),
                orientation='v',
                marker_color=cor,
                text=valores_abs,
                textposition='inside'
            ))

    layout_config = dict(
        barmode='stack',
        title=titulo,
        height=altura,
        legend_title=coluna_categoria
    )

    if orientacao == 'horizontal':
        layout_config.update(dict(
            xaxis=dict(title="Percentual", range=[0, 100], ticksuffix="%", showgrid=True),
            yaxis_title=""
        ))
    else:
        layout_config.update(dict(
            yaxis=dict(title="Percentual", range=[0, 100], ticksuffix="%", showgrid=True),
            xaxis_title=""
        ))

    fig.update_layout(**layout_config)

    return fig

def selecionar_filtro(df, coluna, label=None, key=None):
    """
    Mostra o multiselect apenas uma vez e retorna a seleção feita.
    """
    opcoes = sorted(df[coluna].dropna().unique())
    selecao = st.multiselect(
        label or f"Filtrar por {coluna}",
        options=opcoes,
        default=opcoes,
        key=key
    )
    return selecao

def aplicar_filtro(df, coluna, selecao):
    """
    Aplica o filtro recebido no DataFrame.
    """
    return df[df[coluna].isin(selecao)]

def plot_scatter_generico_plotly(
    df,
    coluna_x,
    coluna_y,
    coluna_linha_referencia,
    coluna_categoria,
    coluna_nome_pessoa,
    label_linha_referencia='Linha de referência',
    titulo='Título do Gráfico',
    label_x='Eixo X',
    label_y='Eixo Y',
    ylim_max=72000,
    colors=None,
    marker='circle'
):
    
    
    if colors is None:
        colors = ['#D4EFFC','#008ED4',  '#002561','#924A7C', '#EE2D67','#F2665E', '#EBEA70','#8EC6B2']

    tipos_categoria = df[coluna_categoria].unique()
    cor_mapa = {tipo: colors[i % len(colors)] for i, tipo in enumerate(tipos_categoria)}

    fig = go.Figure()

    for tipo, df_tipo in df.groupby(coluna_categoria):
        fig.add_trace(go.Scatter(
            x=df_tipo[coluna_x],
            y=df_tipo[coluna_y],
            mode='markers',
            name=str(tipo),
            marker=dict(
                color=cor_mapa[tipo],
                symbol=marker,
                size=10,
                line=dict(width=1, color='black')
            ),
            text=df_tipo[coluna_nome_pessoa],
            hovertemplate=(
                f"<b>%{{text}}</b><br>" +
                f"{label_x}: %{{x}}<br>" +
                f"{label_y}: %{{y}}<extra></extra>"
            )
        ))


    df_linha = df[[coluna_x, coluna_linha_referencia]].sort_values(by=coluna_x)

    fig.add_trace(go.Scatter(
        x=df_linha[coluna_x],
        y=df_linha[coluna_linha_referencia],
        mode='lines',
        name=label_linha_referencia,
        line=dict(color='#002561', dash='dash')
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title=label_x,
        yaxis_title=label_y,
        yaxis=dict(range=[0, ylim_max]),
        legend=dict(orientation='v', x=1.02, y=1),
        margin=dict(r=150),
        height=600
    )

    return fig

def exibir_banner(caminho_imagem: str, altura_px: int = 100):
    """Exibe um banner centralizado em uma aplicação Streamlit.

    Args:
        caminho_imagem (str): Caminho para o arquivo de imagem.
        altura_px (int): Altura do banner em pixels. Padrão é 100.
    """
    # Lê e codifica a imagem em base64
    with open(caminho_imagem, 'rb') as f:
        imagem_base64 = base64.b64encode(f.read()).decode()

    # Aplica o estilo CSS
    st.markdown(
        """
        <style>
            .banner-container {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Monta o HTML do banner e exibe
    banner_html = f"""
    <div class="banner-container">
        <img src="data:image/png;base64,{imagem_base64}" alt="Banner" style="height:{altura_px}px;">
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)



def plot_barra_empilhada_percentual_subplots(
    df,
    coluna_grupo,
    coluna_categoria,
    titulo="Gráfico de barras empilhadas (100%)",
    cor_categoria=None,
    ordem_categorias=None,
    ordem_grupos=None,
    ordem_categorias_alfabetica_invertida=False,
    ordem_grupos_alfabetica_invertida=False,
    altura=400,
    orientacao='horizontal'  # Novo parâmetro: 'horizontal' ou 'vertical'
):
    """
    Gráfico de barras empilhadas com proporções e rótulos absolutos em subgráficos.

    Parâmetros:
    - orientacao: 'horizontal' (padrão) ou 'vertical'
    """

    # Criar uma lista de combinações únicas de (mes_y, nome_evento)
    grupos_unicos = df[coluna_grupo].drop_duplicates()

    # Calcular número de subgráficos
    num_subplots = len(grupos_unicos)

    # Criar o layout do gráfico com múltiplos subgráficos
    fig = make_subplots(
        rows=num_subplots, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.05,
        subplot_titles=[f"{grupo[0]} - {grupo[1]}" for grupo in grupos_unicos.values]
    )

    categorias = df[coluna_categoria].unique().tolist()

    # Ordenar as categorias caso necessário
    if ordem_categorias_alfabetica_invertida:
        categorias = sorted(categorias, reverse=True)
    elif ordem_categorias:
        categorias = [cat for cat in ordem_categorias if cat in categorias]

    cores = cor_categoria or {}
    default_colors = ['#2ca02c', '#d62728', '#1f77b4', '#ff7f0e', '#9467bd']

    # Loop para cada combinação de mes_y e nome_evento (grupo único)
    for i, grupo in enumerate(grupos_unicos.values):
        mes_y, nome_evento = grupo
        df_grupo = df[(df['mes_y'] == mes_y) & (df['nome_evento'] == nome_evento)]

        tabela_abs = df_grupo.pivot_table(
            index=coluna_grupo,
            columns=coluna_categoria,
            aggfunc='size',
            fill_value=0
        )

        tabela_pct = tabela_abs.div(tabela_abs.sum(axis=1), axis=0) * 100

        for j, cat in enumerate(categorias):
            cor = cores.get(cat, default_colors[j % len(default_colors)] )
            valores_pct = tabela_pct[cat].tolist()
            valores_abs = tabela_abs[cat].tolist()

            if orientacao == 'horizontal':
                fig.add_trace(go.Bar(
                    y=[str(grupo) for grupo in tabela_pct.index],
                    x=valores_pct,
                    name=str(cat),
                    orientation='h',
                    marker_color=cor,
                    text=valores_abs,
                    textposition='inside'
                ), row=i+1, col=1)
            else:
                fig.add_trace(go.Bar(
                    x=[str(grupo) for grupo in tabela_pct.index],
                    y=valores_pct,
                    name=str(cat),
                    orientation='v',
                    marker_color=cor,
                    text=valores_abs,
                    textposition='inside'
                ), row=i+1, col=1)

    fig.update_layout(
        barmode='stack',
        title=titulo,
        height=altura * num_subplots,  # Ajustar altura para múltiplos subgráficos
        showlegend=True,
        legend_title=coluna_categoria
    )

    # Ajustar título dos eixos conforme a orientação
    if orientacao == 'horizontal':
        fig.update_xaxes(title="Percentual", range=[0, 100], ticksuffix="%", showgrid=True)
        fig.update_yaxes(title="")
    else:
        fig.update_yaxes(title="Percentual", range=[0, 100], ticksuffix="%", showgrid=True)
        fig.update_xaxes(title="")

    return fig


