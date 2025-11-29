import PIL
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import json
from io import StringIO
from pathlib import Path


# Função para carregar e preparar os dados do Survey_AI.csv
@st.cache_data
def load_and_prepare_survey_data():
    # O arquivo Survey_AI.csv não foi fornecido diretamente, mas o código do notebook
    # sugere que ele está em 'upload/Survey_AI.csv'.
    # O usuário deve colocar o arquivo 'Survey_AI.csv' na pasta 'upload'
    
    # Tentativa de carregar o arquivo real se ele existir
    try:
        df = pd.read_csv('Survey_AI.csv', encoding='utf-8')
    except FileNotFoundError:
        st.error("Arquivo 'Survey_AI.csv' não encontrado. Por favor, certifique-se de que ele está na pasta 'upload'.")
        return None
    except Exception as e:
        st.warning(f"Erro ao carregar 'Survey_AI.csv' com utf-8: {e}. Tentando 'latin-1'.")
        try:
            df = pd.read_csv('Survey_AI.csv', encoding='latin-1')
        except Exception as e_latin:
            st.error(f"Erro ao carregar 'Survey_AI.csv' com latin-1: {e_latin}. Não foi possível carregar os dados.")
            return None

    # Renomear e mapear colunas (baseado em graficos_output_survey_ai.ipynb)
    column_mapping = {
        'Q1.AI_knowledge': 'Conhecimento_IA',
        'Q3#2.Job_replacement': 'Substituicao_Emprego',
        'Q3#3.Problem_solving': 'Resolucao_Problemas',
        'Q3#4.AI_rulling_society': 'IA_Governa_Sociedade',
        'Q4#3.Economic_growth': 'Crescimento_Economico',
        'Q4#4.Job_loss': 'Perda_Emprego',
        'Q5.Feelings': 'Sentimentos_IA',
        'Q12.Gender': 'Genero',
        'Q13.Year_of_study': 'Ano_Estudo',
        'Q14.Major': 'Curso'
    }
    
    # Aplicar o mapeamento apenas se as colunas existirem
    cols_to_rename = {k: v for k, v in column_mapping.items() if k in df.columns}
    df.rename(columns=cols_to_rename, inplace=True)

    # Mapeamento de valores para melhor visualização
    sentimentos_map = {1: 'Otimista', 2: 'Ansioso', 3: 'Indiferente', 4: 'Cético'}
    if 'Sentimentos_IA' in df.columns:
        df['Sentimentos_IA_Desc'] = df['Sentimentos_IA'].map(sentimentos_map)

    genero_map = {1: 'Masculino', 2: 'Feminino'}
    if 'Genero' in df.columns:
        df['Genero_Desc'] = df['Genero'].map(genero_map)

    likert_map = {
        1: 'Discordo Fortemente', 2: 'Discordo', 3: 'Neutro', 4: 'Concordo', 5: 'Concordo Fortemente'
    }
    
    for col_orig, col_desc in [
        ('Substituicao_Emprego', 'Substituicao_Emprego_Desc'),
        ('Resolucao_Problemas', 'Resolucao_Problemas_Desc'),
        ('IA_Governa_Sociedade', 'IA_Governa_Sociedade_Desc'),
        ('Crescimento_Economico', 'Crescimento_Economico_Desc'),
        ('Perda_Emprego', 'Perda_Emprego_Desc')
    ]:
        if col_orig in df.columns:
            df[col_desc] = df[col_orig].map(likert_map)

    return df

# Função para carregar e preparar os dados do Impact_AI_v2.csv
@st.cache_data
def load_and_prepare_impact_data():
    # O arquivo Impact_AI_v2.csv não foi fornecido diretamente, mas o código do notebook
    # sugere que ele está em 'upload/Impact_AI_v2.csv'.
    # O usuário deve colocar o arquivo 'Impact_AI_v2.csv' na pasta 'upload'
    
    try:
        df = pd.read_csv('/Users/miriansanchesfiorini/Desktop/projeto_congresso/The impact of artificial intelligence on society.csv', encoding='utf-8')
    except FileNotFoundError:
        st.error("Arquivo 'Impact_AI_v2.csv' não encontrado. Por favor, certifique-se de que ele está na pasta 'upload'.")
        return None
    except Exception as e:
        
        try:
            df = pd.read_csv('/Users/miriansanchesfiorini/Desktop/projeto_congresso/The impact of artificial intelligence on society.csv', encoding='latin-1')
        except Exception as e_latin:
            st.error(f"Erro ao carregar 'Impact_AI_v2.csv' com latin-1: {e_latin}. Não foi possível carregar os dados.")
            return None

    # Renomear e mapear colunas (baseado em graficos_output_impact_ai_v2.ipynb)
    column_mapping = {
        'How much knowledge do you have about artificial intelligence (AI) technologies?': 'Conhecimento_IA',
        'Do you generally trust artificial intelligence (AI)?': 'Confiança_IA',
        'Do you think artificial intelligence (AI) will be generally beneficial or harmful to humanity?': 'Impacto_Humanidade',
        'I think artificial intelligence (AI) could threaten individual freedoms.': 'Ameaça_Liberdades',
        'Could artificial intelligence (AI) completely eliminate some professions?': 'Elimina_Profissões',
        'Do you think your own job could be affected by artificial intelligence (AI)?': 'Afeta_Emprego_Pessoal',
        'Do you believe that artificial intelligence (AI) should be limited by ethical rules?': 'Limites_Éticos',
        'Could artificial intelligence (AI) one day become conscious like humans?': 'IA_Consciente'
    }
    
    cols_to_rename = {k: v for k, v in column_mapping.items() if k in df.columns}
    df.rename(columns=cols_to_rename, inplace=True)

    # Mapeamento de valores para melhor visualização
    confianca_map = {
        "I trust it": "Confio",
        "I don't trust it": "Não Confio",
        "I'm undecided": "Indeciso"
    }
    if 'Confiança_IA' in df.columns:
        df['Confiança_IA_Desc'] = df['Confiança_IA'].map(confianca_map)

    impacto_map = {
        "More beneficial than harmful": "Mais Benéfica",
        "More harmful than beneficial": "Mais Prejudicial",
        "Both beneficial and harmful": "Ambos",
        "I have no idea": "Não Sei"
    }
    if 'Impacto_Humanidade' in df.columns:
        df['Impacto_Humanidade_Desc'] = df['Impacto_Humanidade'].map(impacto_map)

    # Mapeamento para as colunas de concordância/discordância
    agree_map = {
        "Strongly Agree": "Concordo Fortemente",
        "Agree": "Concordo",
        
        
        
    }
    
    for col_orig, col_desc in [
        ('Ameaça_Liberdades', 'Ameaça_Liberdades_Desc'),
        ('Limites_Éticos', 'Limites_Éticos_Desc')
    ]:
        if col_orig in df.columns:
            df[col_desc] = df[col_orig].map(agree_map)

    return df

# ==============================================================================
# GRÁFICOS DO SURVEY_AI (Notebook 1)
# ==============================================================================

def plot_conhecimento_ia(df):
    if df is None or 'Conhecimento_IA' not in df.columns:
        st.warning("Dados para 'Conhecimento_IA' não disponíveis.")
        return
    
    st.markdown("### 1. Distribuição do Nível de Conhecimento sobre IA (Q1)")
    
    # Contagem de frequência
    conhecimento_counts = df['Conhecimento_IA'].value_counts().sort_index()
    
    # Criar o gráfico de barras com Plotly
    fig = px.bar(
        conhecimento_counts,
        x=conhecimento_counts.index,
        y=conhecimento_counts.values,
        labels={'x': 'Nível de Conhecimento (Escala 1-10)', 'y': 'Contagem de Respondentes'},
        title='Distribuição do Nível de Conhecimento sobre IA',
        color=conhecimento_counts.values,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        template='plotly_dark',
        xaxis={'tickmode': 'linear'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_sentimentos_ia(df):
    if df is None or 'Sentimentos_IA_Desc' not in df.columns:
        st.warning("Dados para 'Sentimentos_IA' não disponíveis.")
        return
    
    st.markdown("### 2. Sentimentos em Relação à IA (Q5)")
    
    # Contagem de frequência
    sentimentos_counts = df['Sentimentos_IA_Desc'].value_counts()
    
    # Criar o gráfico de pizza com Plotly
    fig = px.pie(
        sentimentos_counts,
        names=sentimentos_counts.index,
        values=sentimentos_counts.values,
        title='Sentimentos Predominantes em Relação à IA',
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0, 0])
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_likert_scale(df, column, title):
    if df is None or column not in df.columns:
        st.warning(f"Dados para '{title}' não disponíveis.")
        return
    
    st.markdown(f"### {title}")
    
    # Definir a ordem correta para a escala Likert
    order = ['Discordo Fortemente', 'Discordo', 'Neutro', 'Concordo', 'Concordo Fortemente']
    
    # Contagem de frequência
    counts = df[column].value_counts().reindex(order).fillna(0)
    
    # Criar o gráfico de barras com Plotly
    fig = px.bar(
        counts,
        x=counts.index,
        y=counts.values,
        labels={'x': 'Nível de Concordância', 'y': 'Contagem de Respondentes'},
        title=title,
        color=counts.values,
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        template='plotly_dark',
        xaxis={'categoryorder': 'array', 'categoryarray': order},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_conhecimento_vs_sentimento(df):
    if df is None or 'Conhecimento_IA' not in df.columns or 'Sentimentos_IA_Desc' not in df.columns:
        st.warning("Dados para 'Conhecimento_IA' ou 'Sentimentos_IA' não disponíveis.")
        return
    
    st.markdown("### 5. Distribuição de Conhecimento por Sentimento")
    
    # Contar quantas pessoas estão em cada nível de conhecimento por sentimento
    df_count = df.groupby(['Sentimentos_IA_Desc', 'Conhecimento_IA']).size().reset_index(name='Quantidade')
    
    # Criar gráfico de linha
    fig = px.line(
        df_count,
        x='Conhecimento_IA',
        y='Quantidade',
        color='Sentimentos_IA_Desc',
        markers=True,  # Adiciona pontos nas linhas
        title='Quantidade de Respondentes por Nível de Conhecimento e Sentimento',
        labels={'Conhecimento_IA': 'Nível de Conhecimento (1-10)', 'Quantidade': 'Número de Pessoas', 'Sentimentos_IA_Desc': 'Sentimento'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_traces(mode='lines+markers', hovertemplate='<b>%{fullData.name}</b><br>Conhecimento: %{x}<br>Pessoas: %{y}<extra></extra>')
    
    fig.update_layout(
        template='plotly_dark',
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    def plot_confianca_vs_conhecimento(df):
        """
        Gráfico que mostra a distribuição de Confiança em relação à IA
        agrupada por Nível de Conhecimento
        """
    if df is None or 'Confiança_IA_Desc' not in df.columns or 'Conhecimento_IA' not in df.columns:
        st.warning("Dados para 'Confiança_IA' ou 'Conhecimento_IA' não disponíveis.")
        return
    
    st.markdown("### 10. Distribuição de Confiança na IA por Nível de Conhecimento")
    
    # Criar mapeamento de nível de conhecimento em categorias
    def categorizar_conhecimento(valor):
        if valor <= 2:
            return 'Sem Conhecimento'
        elif valor <= 4:
            return 'Pouco Conhecimento'
        elif valor <= 6:
            return 'Conhecimento Básico'
        elif valor <= 8:
            return 'Bom Conhecimento'
        else:
            return 'Conhecimento Especialista'
    
    df['Conhecimento_Cat'] = df['Conhecimento_IA'].apply(categorizar_conhecimento)
    
    # Criar tabela de frequência cruzada
    crosstab = pd.crosstab(
        df['Conhecimento_Cat'],
        df['Confiança_IA_Desc'],
        normalize='index'
    ) * 100
    
    # Reordenar as colunas de confiança
    ordem_confianca = ['Não Confio', 'Indeciso', 'Confio']
    crosstab = crosstab[[col for col in ordem_confianca if col in crosstab.columns]]
    
    # Reordenar as linhas
    ordem_conhecimento = ['Sem Conhecimento', 'Pouco Conhecimento', 'Conhecimento Básico', 
                          'Bom Conhecimento', 'Conhecimento Especialista']
    crosstab = crosstab.reindex([cat for cat in ordem_conhecimento if cat in crosstab.index])
    
    # Cores semânticas
    color_map = {
        'Não Confio': '#d62728',   # Vermelho
        'Indeciso': '#ffdd57',     # Amarelo
        'Confio': '#7b3ff2'        # Roxo/Azul
    }
    
    # Criar gráfico de barras empilhadas
    fig = go.Figure()
    
    for confianca in ordem_confianca:
        if confianca in crosstab.columns:
            fig.add_trace(go.Bar(
                x=crosstab.index,
                y=crosstab[confianca],
                name=confianca,
                marker_color=color_map.get(confianca, '#gray'),
                text=crosstab[confianca].round(1),
                textposition='inside',
                hovertemplate=f'<b>{confianca}</b><br>Percentagem: %{{y:.1f}}%<extra></extra>'
            ))
    
    fig.update_layout(
        barmode='stack',
        title='Distribuição de Confiança na IA por Nível de Conhecimento',
        xaxis_title='Nível de Conhecimento sobre IA',
        yaxis_title='Percentagem (%)',
        template='plotly_dark',
        xaxis={'tickangle': -45},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
def plot_distribuicao_faixa_etaria(df):
    """
    Gráfico de Pizza: Distribuição por Faixa Etária
    Adaptado para o seu dashboard
    """
    if df is None or 'What is your age range?' not in df.columns:
        st.warning("Dados para 'Faixa Etária' não disponíveis.")
        return
    
    st.markdown("### 11. Distribuição dos Respondentes por Faixa Etária")
    
    # Contagem de frequência
    age_counts = df['What is your age range?'].value_counts()
    
    # Criar gráfico de pizza
    fig = px.pie(
        names=age_counts.index,
        values=age_counts.values,
        title='📊 Distribuição por Faixa Etária',
        hole=0.4,  # Gráfico de Rosca
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textinfo='percent+label',
        pull=[0.05] * len(age_counts),  # Leve separação dos segmentos
        hovertemplate='<b>%{label}</b><br>Respondentes: %{value}<br>Percentagem: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)




# ==============================================================================
# GRÁFICOS DO IMPACT_AI_V2 (Notebook 2)
# ==============================================================================

def plot_confianca_ia(df):
    if df is None or 'Confiança_IA_Desc' not in df.columns:
        st.warning("Dados para 'Confiança_IA' não disponíveis.")
        return
    
    st.markdown("### 6. Confiança Geral na Inteligência Artificial")
    
    # Contagem de frequência
    confianca_counts = df['Confiança_IA_Desc'].value_counts()
    
    # Criar o gráfico de barras com Plotly
    fig = px.bar(
        confianca_counts,
        x=confianca_counts.index,
        y=confianca_counts.values,
        labels={'x': 'Nível de Confiança', 'y': 'Contagem de Respondentes'},
        title='Confiança Geral na Inteligência Artificial',
        color=confianca_counts.values,
        color_continuous_scale=px.colors.sequential.Sunset
    )
    
    fig.update_layout(
        template='plotly_dark',
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_impacto_humanidade(df):
    if df is None or 'Impacto_Humanidade_Desc' not in df.columns:
        st.warning("Dados para 'Impacto_Humanidade' não disponíveis.")
        return
    
    st.markdown("### 7. Percepção do Impacto da IA na Humanidade")
    
    # Contagem de frequência
    impacto_counts = df['Impacto_Humanidade_Desc'].value_counts().reset_index()
    impacto_counts.columns = ['Impacto', 'Quantidade']
    
    # Calcular percentual
    impacto_counts['Percentual'] = (impacto_counts['Quantidade'] / impacto_counts['Quantidade'].sum() * 100).round(1)
    
    # Ordenar para visualização (maior para menor)
    impacto_counts = impacto_counts.sort_values('Quantidade', ascending=True)
    
    # Criar texto customizado para mostrar quantidade e percentual
    impacto_counts['Label'] = impacto_counts.apply(
        lambda row: f"{row['Quantidade']} respondentes ({row['Percentual']}%)", 
        axis=1
    )
    
    # Criar gráfico de barras horizontal
    fig = px.bar(
        impacto_counts,
        y='Impacto',
        x='Quantidade',
        orientation='h',
        color='Quantidade',
        color_continuous_scale='Plasma',
        title='O que os respondentes acham sobre o Impacto da IA na Humanidade?',
        labels={'Quantidade': 'Número de Respondentes', 'Impacto': 'Percepção'},
        text='Label'  # Mostra rótulo customizado
    )
    
    fig.update_traces(textposition='outside', hovertemplate='<b>%{y}</b><br>Respondentes: %{x}<extra></extra>')
    
    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_ameaca_liberdades(df):
    if df is None or 'Ameaça_Liberdades_Desc' not in df.columns:
        st.warning("Dados para 'Ameaça_Liberdades' não disponíveis.")
        return
    
    st.markdown("### 9. Ameaça às Liberdades Individuais pela IA")
    
    # Definir a ordem correta para a escala Likert
    order = ['Discordo Fortemente', 'Discordo', 'Indeciso', 'Concordo', 'Concordo Fortemente']
    
    # Contagem de frequência
    counts = df['Ameaça_Liberdades_Desc'].value_counts().reindex(order).fillna(0).reset_index()
    counts.columns = ['Resposta', 'Quantidade']
    
    # Calcular percentual
    total = counts['Quantidade'].sum()
    counts['Percentual'] = (counts['Quantidade'] / total * 100).round(1)
    counts['Label'] = counts.apply(lambda x: f"{x['Quantidade']} ({x['Percentual']}%)", axis=1)
    
    # Cores Semânticas (Traffic Light)
    color_map = {
        'Concordo': '#ff7f0e',             # Laranja
        'Concordo Fortemente': '#d62728'   # Vermelho (é ameaça)
    }
    
    fig = px.bar(
        counts,
        y='Resposta',
        x='Quantidade',
        orientation='h',
        color='Resposta',
        color_discrete_map=color_map,
        text='Label',
        title='A IA ameaça as liberdades individuais?',
        labels={'Quantidade': 'Número de Respondentes', 'Resposta': 'Opinião'}
    )
    
    fig.update_traces(textposition='outside', hovertemplate='<b>%{y}</b><br>Respondentes: %{x}<extra></extra>')
    
    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_distribuicao_faixa_etaria(df):
    if df is None or 'What is your age range?' not in df.columns:
        st.warning("Dados para 'Faixa Etária' não disponíveis.")
        return
    
    st.markdown("### 11. Distribuição dos Respondentes por Faixa Etária")
    
    # Contagem de frequência
    age_counts = df['What is your age range?'].value_counts()
    
    # Criar gráfico de pizza
    fig = px.pie(
        names=age_counts.index,
        values=age_counts.values,
        title='📊 Distribuição por Faixa Etária',
        hole=0.4,  # Gráfico de Rosca
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textinfo='percent+label',
        pull=[0.05] * len(age_counts),  # Leve separação dos segmentos
        hovertemplate='<b>%{label}</b><br>Respondentes: %{value}<br>Percentagem: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
def plot_confianca_vs_conhecimento(df):
    if df is None or 'Confiança_IA_Desc' not in df.columns or 'Conhecimento_IA' not in df.columns:
        st.warning("Dados para 'Confiança_IA' ou 'Conhecimento_IA' não disponíveis.")
        return
    
    st.markdown("### 10. Distribuição de Confiança na IA por Nível de Conhecimento")
    
    # Criar mapeamento de nível de conhecimento em categorias
    def categorizar_conhecimento(valor):
        if valor <= 2:
            return 'Sem Conhecimento'
        elif valor <= 4:
            return 'Pouco Conhecimento'
        elif valor <= 6:
            return 'Conhecimento Básico'
        elif valor <= 8:
            return 'Bom Conhecimento'
        else:
            return 'Conhecimento Especialista'
    
    df['Conhecimento_Cat'] = df['Conhecimento_IA'].apply(categorizar_conhecimento)
    
    # Criar tabela de frequência cruzada
    crosstab = pd.crosstab(
        df['Conhecimento_Cat'],
        df['Confiança_IA_Desc'],
        normalize='index'
    ) * 100
    
    # Reordenar as colunas de confiança
    ordem_confianca = ['Não Confio', 'Indeciso', 'Confio']
    crosstab = crosstab[[col for col in ordem_confianca if col in crosstab.columns]]
    
    # Reordenar as linhas
    ordem_conhecimento = ['Sem Conhecimento', 'Pouco Conhecimento', 'Conhecimento Básico', 
                          'Bom Conhecimento', 'Conhecimento Especialista']
    crosstab = crosstab.reindex([cat for cat in ordem_conhecimento if cat in crosstab.index])
    
    # Cores semânticas
    color_map = {
        'Não Confio': '#d62728',   # Vermelho
        'Indeciso': '#ffdd57',     # Amarelo
        'Confio': '#7b3ff2'        # Roxo/Azul
    }
    
    # Criar gráfico de barras empilhadas
    fig = go.Figure()
    
    for confianca in ordem_confianca:
        if confianca in crosstab.columns:
            fig.add_trace(go.Bar(
                x=crosstab.index,
                y=crosstab[confianca],
                name=confianca,
                marker_color=color_map.get(confianca, '#gray'),
                text=crosstab[confianca].round(1),
                textposition='inside',
                hovertemplate=f'<b>{confianca}</b><br>Percentagem: %{{y:.1f}}%<extra></extra>'
            ))
    
    fig.update_layout(
        barmode='stack',
        title='Distribuição de Confiança na IA por Nível de Conhecimento',
        xaxis_title='Nível de Conhecimento sobre IA',
        yaxis_title='Percentagem (%)',
        template='plotly_dark',
        xaxis={'tickangle': -45},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)





def plot_limites_eticos(df):
    if df is None or 'Limites_Éticos_Desc' not in df.columns:
        st.warning("Dados para 'Limites_Éticos' não disponíveis.")
        return
    
    st.markdown("### 8. Consenso sobre Limites Éticos para a IA")
    
    # Ordem lógica
    order = ['Indeciso', 'Concordo', 'Concordo Fortemente']
    
    # Contagem
    counts = df['Limites_Éticos_Desc'].value_counts().reindex(order).fillna(0).reset_index()
    counts.columns = ['Resposta', 'Quantidade']
    
    # Calcular percentual para o rótulo
    total = counts['Quantidade'].sum()
    counts['Percentual'] = (counts['Quantidade'] / total * 100).round(1)
    counts['Label'] = counts.apply(lambda x: f"{x['Quantidade']} ({x['Percentual']}%)", axis=1)
    
    # Cores Semânticas (Traffic Light)
    color_map = {
        'Indeciso': '#7f7f7f',            # Cinza
        'Concordo': '#2ca02c',            # Verde
        'Concordo Fortemente': '#1f77b4'  # Azul ou Verde Escuro (#006400)
    }

    # Ajustando para Verde Escuro no Concordo Fortemente para ficar mais intuitivo
    color_map['Concordo Fortemente'] = '#006400' 
    
    fig = px.bar(
        counts,
        y='Resposta',
        x='Quantidade',
        orientation='h', # Horizontal facilita a leitura dos rótulos longos
        color='Resposta',
        color_discrete_map=color_map,
        text='Label',
        title='A IA deve ser limitada por regras éticas?',
        labels={'Quantidade': 'Número de Respondentes', 'Resposta': 'Opinião'}
    )
    
    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# FUNÇÃO PRINCIPAL PARA A PÁGINA DE GRÁFICOS
# ==============================================================================

def show_graficos_page():
    st.markdown("# 📊 Análise de Dados e Gráficos")
    
    st.markdown("""
    <div class="content-box">
        <h2> Análise da Percepção e Impacto da IA </h2>
        <p>
            Esta seção apresenta os resultados da pesquisa sobre a percepção da Inteligência Artificial, 
            dividida em duas análises principais: uma focada no **Survey Acadêmico** e outra no **Impacto Geral da IA**.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df_survey = load_and_prepare_survey_data()
    df_impact = load_and_prepare_impact_data()
    
    tab_survey, tab_impact = st.tabs(["Pesquisa Acadêmica (Survey_AI)", "Impacto Geral (Impact_AI_v2)"])
    
    with tab_survey:
        st.markdown("## Resultados da Pesquisa Acadêmica (Survey_AI)")
        if df_survey is not None:
            plot_conhecimento_ia(df_survey)
            plot_sentimentos_ia(df_survey)
            plot_likert_scale(df_survey, 'Substituicao_Emprego_Desc', '3. Percepção sobre Substituição de Empregos pela IA')
            plot_likert_scale(df_survey, 'Crescimento_Economico_Desc', '4. Percepção sobre Crescimento Econômico pela IA')
            plot_conhecimento_vs_sentimento(df_survey)
        else:
            st.error("Não foi possível carregar os dados da Pesquisa Acadêmica. Verifique o arquivo 'Survey_AI.csv'.")

    with tab_impact:
        st.markdown("## Resultados da Pesquisa de Impacto Geral (Impact_AI_v2)")
    if df_impact is not None:
        plot_confianca_ia(df_impact)
        plot_impacto_humanidade(df_impact)
        plot_ameaca_liberdades(df_impact)
        plot_limites_eticos(df_impact)
        plot_confianca_vs_conhecimento(df_impact)  # ← NOVO
        plot_distribuicao_faixa_etaria(df_impact)  # ← NOVO
    else:
        st.error("Não foi possível carregar os dados...")




# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="Relação de crescimento inversamente proporcional entre Inteligência Artificial e Inteligência Humana",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS PERSONALIZADO ====================
st.markdown("""
<style>
    /* Importar fontes do Google */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Estilo global */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Fundo gradiente azul e preto */
    .stApp {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
    }
    
    /* Sidebar personalizada */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #1a1a2e 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background-color: rgba(0, 78, 146, 0.2);
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Títulos principais */
    h1 {
        color: #ffffff;
        text-align: center;
        font-weight: 700;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        padding: 1.5rem;
        background: linear-gradient(90deg, rgba(0,78,146,0.3), rgba(0,4,40,0.3));
        border-radius: 20px;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-in-out;
    }
    
    h2 {
        color: #ffffff;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-top: 2rem;
        padding: 1rem;
        background: rgba(0,78,146,0.3);
        border-radius: 15px;
        border-left: 5px solid #0099ff;
    }
    
    h3 {
        color: #0099ff;
        font-weight: 600;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Caixas de conteúdo */
    .content-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(0,78,146,0.3);
        animation: fadeIn 1.5s ease-in-out;
    }
    
    .content-box p {
        color: #1a1a2e;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: justify;
    }
    
    .content-box ul, .content-box li {
        color: #1a1a2e;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: justify;
    }
    
    /* Cards de autoras */
    .author-card {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        margin: 1.5rem 0;
        color: white;
        transition: transform 0.3s ease;
    }
    
    .author-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 50px rgba(0,153,255,0.5);
    }
    
    .author-card h3 {
        color: #0099ff;
        margin-bottom: 1rem;
        font-size: 1.8rem;
    }
    
    .author-card p {
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    /* Estilo para a imagem do perfil */
    .profile-img {
        width: 100px; /* Tamanho da imagem */
        height: 100px;
        border-radius: 50%; /* Deixa a imagem redonda */
        object-fit: cover; /* Garante que a imagem preencha o espaço */
        margin-bottom: 1rem;
        border: 3px solid #0099ff; /* Borda azul */
    }
    
    /* Caixas de destaque */
    .highlight-box {
        background: linear-gradient(135deg, #0099ff 0%, #004e92 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        font-size: 1.2rem;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 5px 25px rgba(0,0,0,0.3);
        margin: 2rem 0;
        animation: pulse 2s infinite;
    }
    
    /* Referências */
    .reference-item {
        background: rgba(255,255,255,0.9);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #0099ff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .reference-item:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 20px rgba(0,153,255,0.3);
    }
    
    .reference-item p {
        color: #1a1a2e;
        margin: 0;
        font-size: 1rem;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(90deg, #0099ff 0%, #004e92 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        border: none;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,153,255,0.4);
    }
    
    /* Animações */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0099ff;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a2e;
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #0099ff;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #0099ff;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0,78,146,0.2);
        border-radius: 10px;
        font-weight: 600;
        color: white;
    }
    
    /* Seção de referências */
    .references-section {
        background: rgba(0, 78, 146, 0.1);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(0, 153, 255, 0.3);
        margin-top: 2rem;
    }
    
    /* Estatísticas */
    .stat-box {
        background: linear-gradient(135deg, rgba(0, 153, 255, 0.2), rgba(0, 78, 146, 0.2));
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid rgba(0, 153, 255, 0.5);
        margin: 1rem 0;
        text-align: center;
    }
    
    .stat-box h4 {
        color: #0099ff;
        font-size: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .stat-box p {
        color: #ffffff;
        font-size: 1.2rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("# IA vs Cognição ")
    st.markdown("---")
    
    pagina = st.radio(
        "📋 Navegação",
        ["🏠 Menu Inicial", "📊 Gráficos", "ℹ️ Sobre"],
        label_visibility="collapsed"
    )
    
# ==================== PÁGINA: MENU INICIAL ====================
if pagina == "🏠 Menu Inicial":
    st.markdown("# Inteligência Artificial vs Inteligência Humana ")
    
    # Introdução
    st.markdown("""
    <div class="content-box">
        <h2> Relação entre "Inteligências" </h2>
        <p>
            A Inteligência Artificial (IA) está revolucionando a forma como vivemos, trabalhamos e pensamos. 
            Este projeto explora uma questão fundamental: <strong>qual é o impacto do uso excessivo de IA na capacidade cognitiva humana?</strong> 
        </p>
        <p>
            Investigamos como conteúdos instantâneos, pesquisas rápidas e respostas prontas podem enfraquecer a capacidade criativa, 
            o pensamento crítico e a autonomia intelectual. Através de análises detalhadas, gráficos interativos e referências científicas, 
            apresentamos uma visão abrangente de um fenômeno crescente na sociedade contemporânea. 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Destaques principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="highlight-box">
            🧠 Cognitive Offloading<br>
            Terceirização do raciocínio
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
            🔴 Brain Rot<br>
            Deterioração cerebral
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="highlight-box">
            🌫️ Mental Fog<br>
            Confusão mental
        </div>
        """, unsafe_allow_html=True)
    
    # Hipótese Central
    st.markdown("""
    <div class="content-box">
        <h2> Hipótese Central de nosso Estudo </h2>
        <p>
            <strong>Embora a tecnologia facilite o acesso à informação e amplie horizontes, o uso excessivo pode adormecer habilidades 
            críticas e criativas, criando condições que potencialmente levam a desafios futuros no desenvolvimento intelectual e na autonomia dos indivíduos.</strong> 
        </p>
        <p>
            A sociedade está usufruindo de grandes facilidades tecnológicas e, pode estar semeando, ainda que de forma inconsciente, 
            os próprios desafios do futuro. O conforto e as comodidades atuais, ao mesmo tempo em que ampliam horizontes, também tendem 
            a adormecer a capacidade crítica e criativa do ser humano. 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Principais Fenômenos
    st.markdown("## Principais Fenômenos Investigados 🔍")
    
    st.markdown("### 1. Cognitive Offloading")
    st.markdown("""
    Terceirizar etapas do raciocínio para ferramentas externas (listas, GPS, buscadores, IA) a fim de reduzir esforço. 
    Este processo altera a fronteira funcional entre o que mantemos "na cabeça" e o que deixamos "no mundo", 
    especialmente sob hiper acesso à informação. 
    """)
    
    st.markdown("### 2. Brain Rot - Apodrecimento Mental")
    st.markdown("""
    Termo cunhado por Henry David Thoreau no século XIX, ganhou ressignificação moderna relacionada ao uso excessivo de redes sociais. 
    Refere-se ao fenômeno de sobrecarga cerebral com processamento rápido de grande volume de informações superficiais. 
    Em dezembro de 2024, foi escolhido como expressão do ano pelo Dicionário Oxford! 
    """)
    
    st.markdown("### 3. Mental Fog - Confusão Mental")
    st.markdown("""
    Estado de confusão mental caracterizado por dificuldade de concentração, lapsos de memória, lentidão no raciocínio 
    e sensação de exaustão cognitiva. Associado a alterações na memória de trabalho, atenção seletiva e fluência verbal. 😵
    """)
    
    st.markdown("### 4. Dependência de Ferramentas de IA")
    st.markdown("""
    A dependência de ferramentas como ChatGPT pode afetar negativamente a concentração, memória, aprendizagem a longo prazo 
    e capacidade de resolução autônoma de problemas entre estudantes. Diminui a interação social e os debates, 
    limitando o desenvolvimento de habilidades comunicativas e colaborativas. 
    """)
    

    # Objetivos da Pesquisa
    st.markdown("""
    <div class="content-box">
        <h2>Objetivos da Pesquisa </h2>
        <p>
            ✅ Analisar impactos da IA sobre criatividade, pensamento crítico e autonomia<br>
            ✅ Investigar padrões de consumo digital e suas relações com vício, dopamina e estagnação mental<br>
            ✅ Avaliar possíveis consequências de longo prazo para a inteligência humana<br>
            ✅ Relacionar teorias psicológicas e de engenharia social com o comportamento online<br>
            ✅ Propor estratégias que promovam o uso equilibrado da IA 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== PÁGINA: GRÁFICOS ====================
elif pagina == "📊 Gráficos":
    st.markdown("# 📊 Análise de Dados e Gráficos")
    
    st.markdown("""
    <div class="content-box">
        <h2> Análise da Percepção e Impacto da IA </h2>
        <p>
            Esta seção apresenta os resultados da pesquisa sobre a percepção da Inteligência Artificial, 
            dividida em duas análises principais: uma focada no **Survey Acadêmico** e outra no **Impacto Geral da IA**.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df_survey = load_and_prepare_survey_data()
    df_impact = load_and_prepare_impact_data()
    
    tab_survey, tab_impact = st.tabs(["Pesquisa Acadêmica (Survey_AI)", "Impacto Geral (Impact_AI_v2)"])
    
    with tab_survey:
        st.markdown("## Resultados da Pesquisa Acadêmica (Survey_AI)")
        if df_survey is not None:
            plot_conhecimento_ia(df_survey)
            plot_sentimentos_ia(df_survey)
            plot_likert_scale(df_survey, 'Substituicao_Emprego_Desc', '3. Percepção sobre Substituição de Empregos pela IA')
            plot_likert_scale(df_survey, 'Crescimento_Economico_Desc', '4. Percepção sobre Crescimento Econômico pela IA')
            plot_conhecimento_vs_sentimento(df_survey)
        else:
            st.error("Não foi possível carregar os dados da Pesquisa Acadêmica. Verifique o arquivo 'Survey_AI.csv'.")

    with tab_impact:
        st.markdown("## Resultados da Pesquisa de Impacto Geral (Impact_AI_v2)")
        if df_impact is not None:
            plot_confianca_ia(df_impact)
            plot_impacto_humanidade(df_impact)
            plot_likert_scale(df_impact, 'Ameaça_Liberdades_Desc', '9. Ameaça às Liberdades Individuais pela IA')
            plot_limites_eticos(df_impact)
        else:
            st.error("Não foi possível carregar os dados da Pesquisa de Impacto Geral. Verifique o arquivo 'Impact_AI_v2.csv'.")
# ==================== PÁGINA: SOBRE =====================
elif pagina == "ℹ️ Sobre":
    st.markdown("# Sobre o Projeto ")
    
    # Descrição do Projeto
    st.markdown("""
    <div class="content-box">
        <h2> Descrição Detalhada do Projeto </h2>
        <p>
            Este projeto acadêmico investiga a relação de crescimento inversamente proporcional entre a Inteligência Artificial 
            e a Inteligência Humana.  Através de uma abordagem quantitativa e qualitativa, analisamos como o uso excessivo 
            de ferramentas de IA pode comprometer habilidades cognitivas essenciais como criatividade, pensamento crítico e autonomia. 
        </p>
        <p>
            <strong>Metodologia:</strong> A pesquisa utiliza Python para coleta de dados, SQL para manipulação de banco de dados, 
            e Streamlit para criação de dashboards interativos que permitem visualizar os resultados de forma clara e acessível. 
        </p>
        <p>
            <strong>Relevância:</strong> Este estudo é fundamental para compreender criticamente os efeitos da tecnologia no 
            desenvolvimento humano, considerando tanto os benefícios quanto os malefícios do uso excessivo. Propõe estratégias 
            que promovam o uso equilibrado da IA, estimulando competências cognitivas e criativas. 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Conclusões Principais
    st.markdown("## Conclusões Principais ")
    
    st.markdown("""
    <div class="content-box">
        <p><strong>1. Deslocamento Cognitivo:</strong> A facilidade de acesso a respostas por meio de IA e buscas instantâneas convive com sinais de redução do esforço cognitivo deliberado em tarefas que exigem elaboração própria. 🧠❌</p>
        <p><strong>2. Padrão de Uso é Crucial:</strong> O ponto de atenção reside menos na ferramenta e mais no padrão de uso. Quando o uso é constante e automático, emergem sinais de queda na autorregulação e no pensamento crítico. Quando é pontual e consciente, os ganhos de eficiência tendem a não comprometer a autonomia. ⚖️</p>
        <p><strong>3. Semeando Desafios Futuros:</strong> A sociedade colhe facilidades substanciais com IA e internet, mas pode semear desafios futuros se a prática cotidiana consolidar respostas imediatas como substitutas e não complementares da elaboração própria. 🌱⚠️</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sobre as Autoras
    st.markdown("##  Sobre as Autoras ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.html("""
        <div class="author-card">
            <h3> Nicoli Felipe</h3>
            <p>
                <strong>Formação:</strong><br>
                🎓 Graduanda em Ciência de Dados pela Faculdade SENAI de Informática (2025-2026)<br>
                🎓 Graduanda em Informática para Negócios pela Fatec (2025-2027)<br>
                🎓 Técnica em Administração pela ETEC de Mauá (2024)<br><br>
                <strong>ORCID:</strong> 0009-0001-5123-5059<br>
                📧 nicolifelipe01@gmail.com
            </p>
        </div>
        """)
    
    with col2:
        st.markdown("""
        <div class="author-card">
            <h3> Mirian Sanches Fiorini</h3>
            <p>
                <strong>Formação:</strong><br>
                <p>
                🎓 Graduanda em Ciência de Dados pela Faculdade SENAI de Informática (2025-2026)<br>
                🎓 Técnica em Música pela Fundação das Artes (2022)<br><br>
                <p>
                <p>
                <p>
                <strong>ORCID:</strong> 0009-0003-1680-2542<br>
                📧 sanchesmirian489@gmail.com
                <p>
                <p>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sobre a Orientadora
    st.markdown("""
    <div class="author-card">
        <h3> Jéssica Franzon Cruz do Espírito Santo (Orientadora)</h3>
        <p>
            <strong>Formação Acadêmica:</strong><br>
            🎓 Bacharelado em Ciência da Computação (2018-2021) - Universidade Paulista (UNIP)<br>
            🎓 Pós-graduação em Gestão Educacional na Perspectiva Inclusiva (2022) - Universidade Federal de Pelotas (UFPEL)<br>
            🎓 Pós-graduação em Psicopedagogia (2024) - Faculdade das Américas (FAM)<br>
            🎓 Mestranda em Engenharia da Informação - UFABC<br><br>
            <strong>Atuação Profissional:</strong><br>
            👨‍🏫 Professora na Faculdade SENAI (Campus Paulo Antônio Skaf) - Curso de Ciência de Dados<br>
            💡 Especialista em educação inclusiva e psicopedagogia aplicada à tecnologia
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Referências Principais
    st.markdown("## 📚 Referências Principais 📚")
    
    st.markdown("""
    <div class="content-box">
        <p style="color: #1a1a2e;">
            - **🔗 Cognitive Offloading:** Gerlich, M. (2025). AI Tools in Society: Impacts on Cognitive Offloading and the Future of Critical Thinking. Societies.
        </p>
        <p style="color: #1a1a2e;">
            - **🔗 Brain Rot:** Thoreau, H. D. (2006). Walden: a vida nos bosques. Tradução de Denise Bottmann. São Paulo: Martin Claret.
        </p>
        <p style="color: #1a1a2e;">
            - **🔗 Internet e Distração:** Carr, N. (2011). A geração superficial: o que a internet está fazendo com nossos cérebros. Rio de Janeiro: Agir.
        </p>
        <p style="color: #1a1a2e;">
            - **🔗 Mental Fog:** Cleveland Clinic (2024). Brain fog: symptoms, causes and treatment. Disponível em: https://my.clevelandclinic.org/health/symptoms/brain-fog
        </p>
        <p style="color: #1a1a2e;">
            - **🔗 IA e Aprendizado:** Fan, Y. et al. (2024). Beware of metacognitive laziness: Effects of generative artificial intelligence on learning motivation, processes, and performance. arXiv.
        </p>
        <p style="color: #1a1a2e;">
            - **🔗 IA e Criatividade:** Doshi, A. R.; Hauser, O. P. (2024). Generative artificial intelligence enhances creativity but reduces the collective diversity of novel content. Science Advances, v. 10, n. 28.
        </p>
        <p style="color: #1a1a2e;">
            - **🔗 Cognitive Overload:** Cell (2025). Cognitive overload and brain fog in modern life. Trends in Neurosciences.
        </p>
        <p style="color: #1a1a2e;">
            - **🔗 BMC Public Health:** BMC Public Health (2025). Brain fog and cognitive difficulties: impact on work and social life.
        </p>
    </div>
    """, unsafe_allow_html=True)
    

# ==================== RODAPÉ ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #0099ff; padding: 2rem; font-size: 0.9rem;">
    <p><strong>Relação de Crescimento Inversamente Proporcional Entre a Inteligência Artificial e a Inteligência Humana</strong> </p>
    <p>Faculdade SENAI Paulo Antônio Skaf - Ciência de Dados </p>
    <p>© 2025 - Todos os direitos reservados ©</p>
</div>""", unsafe_allow_html = True)
