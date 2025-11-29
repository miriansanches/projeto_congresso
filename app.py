import PIL
from PIL import Image, UnidentifiedImageError
import base64
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import json
from io import StringIO

# Função para carregar e preparar os dados do Survey_AI.csv
@st.cache_data
def load_and_prepare_survey_data():
    try:
        # Caminho relativo: espera o arquivo na mesma pasta do app.py
        df = pd.read_csv('Survey_AI.csv', encoding='utf-8')
    except FileNotFoundError:
        st.error("Arquivo 'Survey_AI.csv' não encontrado. Coloque o arquivo na mesma pasta do app ou ajuste o caminho no código.")
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
        'Q14.Major': 'Curso',
        'Q15.Passed_exams': 'Exames_Aprovados',
        'Q16.GPA': 'GPA'
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

    # Mapeamento de cursos (ajuste os nomes conforme necessário)
    curso_map = {
        1: 'Curso 1',  # Ajuste para o nome real do curso
        2: 'Curso 2',  # Ajuste para o nome real do curso
        3: 'Curso 3'   # Ajuste para o nome real do curso
    }
    if 'Curso' in df.columns:
        df['Curso_Desc'] = df['Curso'].map(curso_map)
        # Se não tiver mapeamento, usar o valor original
        df['Curso_Desc'] = df['Curso_Desc'].fillna(df['Curso'])

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

    # Converter GPA para numérico se existir
    if 'GPA' in df.columns:
        df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')

    # Converter Exames_Aprovados para numérico se existir
    if 'Exames_Aprovados' in df.columns:
        df['Exames_Aprovados'] = pd.to_numeric(df['Exames_Aprovados'], errors='coerce')

    return df

# Função para carregar e preparar os dados do Impact_AI_v2.csv
@st.cache_data
def load_and_prepare_impact_data():
    try:
        # Caminho relativo: espera o arquivo na mesma pasta do app.py
        df = pd.read_csv('The impact of artificial intelligence on society.csv', encoding='utf-8')
    except FileNotFoundError:
        st.error("Arquivo 'The impact of artificial intelligence on society.csv' não encontrado. Coloque o arquivo na mesma pasta do app ou ajuste o caminho no código.")
        return None
    except Exception as e:
        try:
            df = pd.read_csv('The impact of artificial intelligence on society.csv', encoding='latin-1')
        except Exception as e_latin:
            st.error(f"Erro ao carregar 'The impact of artificial intelligence on society.csv' com latin-1: {e_latin}. Não foi possível carregar os dados.")
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
        'Could artificial intelligence (AI) one day become conscious like humans?': 'IA_Consciente',
        'What is your occupation? (optional)': 'Profissao',
        'How often do you use technological devices?': 'Frequencia_Dispositivos',
        'Please rate how actively you use AI-powered products in your daily life on a scale from 1 to 5.': 'Uso_IA_Produtos'
    }
    
    cols_to_rename = {k: v for k, v in column_mapping.items() if k in df.columns}
    df.rename(columns=cols_to_rename, inplace=True)

    # Mapeamento de valores para melhor visualização
    # Normalizamos espaços e consideramos todas as alternativas do questionário.
    confianca_map = {
        "I trust it": "Confio",
        "I don't trust it": "Não Confio",
        "I don't trust it at all": "Não Confio",
        "I'm undecided": "Neutro",
    }
    if 'Confiança_IA' in df.columns:
        conf_norm = df['Confiança_IA'].astype(str).str.strip()
        df['Confiança_IA_Desc'] = conf_norm.map(confianca_map)

    impacto_map = {
        "Definitely beneficial": "Definitivamente Benéfica",
        "More beneficial than harmful": "Mais Benéfica",
        "Both beneficial and harmful": "Ambos",
        "More harmful than beneficial": "Mais Prejudicial",
        "Definitely harmful": "Definitivamente Prejudicial",
        "I have no idea": "Não Sei",
    }
    if 'Impacto_Humanidade' in df.columns:
        impacto_norm = df['Impacto_Humanidade'].astype(str).str.strip()
        df['Impacto_Humanidade_Desc'] = impacto_norm.map(impacto_map)

    # Mapeamento para as colunas de concordância/discordância
    # Existem várias variações de texto no CSV original
    # (ex.: "Strongly disagree", "I disagree"), então
    # normalizamos tudo para minúsculas antes de mapear.
    agree_map_normalized = {
        "strongly agree": "Concordo Fortemente",
        "agree": "Concordo",
        # respostas neutras/indecisas serão exibidas como "Neutro" no gráfico
        "i'm undecided": "Neutro",
        "undecided": "Neutro",
        "i disagree": "Discordo",
        "disagree": "Discordo",
        "strongly disagree": "Discordo Fortemente",
    }
    
    for col_orig, col_desc in [
        ('Ameaça_Liberdades', 'Ameaça_Liberdades_Desc'),
        ('Limites_Éticos', 'Limites_Éticos_Desc')
    ]:
        if col_orig in df.columns:
            # cria uma versão normalizada em minúsculas para mapear
            normalized = df[col_orig].astype(str).str.strip().str.lower()
            df[col_desc] = normalized.map(agree_map_normalized)

    # Tradução das respostas sobre eliminação de profissões
    elimina_prof_map = {
        "Absolutely Can't handle it": "Com certeza não eliminará profissões",
        "Can't handle it": "Provavelmente não eliminará profissões",
        "Removes": "Eliminará algumas profissões",
        "Definitely Removes": "Com certeza eliminará profissões",
        "I have no idea": "Não sei se eliminará profissões",
    }
    if 'Elimina_Profissões' in df.columns:
        df['Elimina_Profissões_Desc'] = df['Elimina_Profissões'].astype(str).str.strip().map(elimina_prof_map)

    # Tradução das respostas sobre afetação do próprio emprego
    afeta_emprego_map = {
        "Definitely I don't think so": "Com certeza não será afetado",
        "I don't think so": "Acho que não será afetado",
        "I'm undecided": "Estou indeciso(a)",
        "Think": "Talvez seja afetado",
        "I definitely think": "Com certeza será afetado",
    }
    if 'Afeta_Emprego_Pessoal' in df.columns:
        df['Afeta_Emprego_Pessoal_Desc'] = df['Afeta_Emprego_Pessoal'].astype(str).str.strip().map(afeta_emprego_map)

    # Tradução das respostas sobre IA consciente
    ia_consciente_map = {
        "Becomes": "Sim, se tornará consciente",
        "Definitely Becomes": "Com certeza se tornará consciente",
        "Can't": "Não pode se tornar consciente",
        "It certainly can't be": "Certamente não pode se tornar consciente",
        "I'm undecided": "Estou indeciso(a)",
    }
    if 'IA_Consciente' in df.columns:
        df['IA_Consciente_Desc'] = df['IA_Consciente'].astype(str).str.strip().map(ia_consciente_map)

    # Tradução do nível de educação
    educacao_map = {
        "Primary education": "Ensino Fundamental",
        "High school": "Ensino Médio",
        "Bachelor's degree": "Graduação",
        "n Bachelor's degree": "Em Graduação",
    }
    educ_col = 'What is your education level?'
    if educ_col in df.columns:
        df['Nivel_Educacao_Desc'] = df[educ_col].astype(str).str.strip().map(educacao_map)

    # Tradução do status de emprego
    emprego_map = {
        "Student": "Estudante",
        "Employed": "Empregado",
        "Unemployed": "Desempregado",
    }
    status_col = 'What is your employment status?'
    if status_col in df.columns:
        df['Status_Emprego_Desc'] = df[status_col].astype(str).str.strip().map(emprego_map)

    # Normalizar e traduzir profissões
    if 'Profissao' in df.columns:
        # Normalizar: remover espaços no início/fim, converter para minúsculas
        df['Profissao_Normalizada'] = df['Profissao'].astype(str).str.strip().str.lower()
        
        # Mapeamento de tradução (baseado nos valores normalizados, sem espaços extras)
        profissao_map = {
            "student": "Estudante",
            "engineer": "Engenheiro(a)",
            "housewife": "Dona de Casa",
            "teacher": "Professor(a)",
            "textile": "Têxtil",
            "sales & marketing": "Vendas e Marketing",
            "sales &amp; marketing": "Vendas e Marketing",  # HTML encoded
            "child development": "Desenvolvimento Infantil",
            "accounting": "Contabilidade",
            "office driver": "Motorista",
            "merchandising": "Merchandising",
            "real estate agent": "Corretor(a) de Imóveis",
        }
        
        # Aplicar tradução
        df['Profissao_Desc'] = df['Profissao_Normalizada'].map(profissao_map)
        # Se não tiver tradução, usar o valor original capitalizado
        df['Profissao_Desc'] = df['Profissao_Desc'].fillna(df['Profissao'].astype(str).str.strip().str.title())
        
        # Garantir que valores vazios sejam tratados como NA
        df['Profissao_Desc'] = df['Profissao_Desc'].replace(['', 'nan', 'None'], pd.NA)

    # Tradução da frequência de uso de dispositivos tecnológicos
    if 'Frequencia_Dispositivos' in df.columns:
        freq_map = {
            "Between 0 to 2 hours per day": "0 a 2 horas por dia",
            "Between 2 to 5 hours per day": "2 a 5 horas por dia",
            "Between 5 to 10 hours per day": "5 a 10 horas por dia",
            "More than 10 hours per day": "Mais de 10 horas por dia",
        }
        df['Frequencia_Dispositivos_Desc'] = df['Frequencia_Dispositivos'].astype(str).str.strip().map(freq_map)
        df['Frequencia_Dispositivos_Desc'] = df['Frequencia_Dispositivos_Desc'].fillna(df['Frequencia_Dispositivos'])

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

def plot_conhecimento_por_genero(df):
    """Barras agrupadas: distribuição do nível de conhecimento de IA por gênero."""
    if df is None or 'Conhecimento_IA' not in df.columns or 'Genero_Desc' not in df.columns:
        st.warning("Dados para 'Conhecimento_IA' ou 'Gênero' não disponíveis.")
        return

    st.markdown("### 3. Perfil de Conhecimento sobre IA por Gênero")

    # Criar tabela cruzada: gênero vs nível de conhecimento
    cross = pd.crosstab(df['Genero_Desc'], df['Conhecimento_IA'])
    
    # Ordenar por nível de conhecimento
    cross = cross.sort_index(axis=1)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Distribuição do Nível de Conhecimento sobre IA por Gênero',
        labels={
            'Genero_Desc': 'Gênero',
            'value': 'Número de Respondentes',
            'variable': 'Nível de Conhecimento (1-10)'
        },
        color_discrete_sequence=px.colors.sequential.Viridis,
        barmode='group'
    )

    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
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
    
    # Criar gráfico de linha (estilo sugerido)
    fig = px.line(
        df_count,
        x='Conhecimento_IA',
        y='Quantidade',
        color='Sentimentos_IA_Desc',
        markers=True,  # Adiciona pontos nas linhas
        title='Quantidade de Respondentes por Nível de Conhecimento e Sentimento',
        labels={
            'Conhecimento_IA': 'Nível de Conhecimento (1-10)',
            'Quantidade': 'Número de Pessoas',
            'Sentimentos_IA_Desc': 'Sentimento'
        },
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_traces(
        mode='lines+markers',
        hovertemplate='<b>%{fullData.name}</b><br>Conhecimento: %{x}<br>Pessoas: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        template='plotly_dark',
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        hovermode='x unified'
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

def plot_uso_ia_vs_confianca(df):
    """Barras agrupadas: distribuição do uso de produtos de IA por nível de confiança."""
    if df is None or 'Confiança_IA_Desc' not in df.columns or 'Uso_IA_Produtos' not in df.columns:
        st.warning("Dados para 'Confiança_IA' ou 'Uso_IA_Produtos' não disponíveis.")
        return

    st.markdown("### 9. Uso Ativo de Produtos de IA vs Nível de Confiança")

    # Converter uso de IA para numérico se necessário
    df_clean = df.copy()
    if df_clean['Uso_IA_Produtos'].dtype == 'object':
        df_clean['Uso_IA_Produtos'] = pd.to_numeric(df_clean['Uso_IA_Produtos'], errors='coerce')

    # Filtrar valores válidos
    df_clean = df_clean[df_clean['Uso_IA_Produtos'].notna() & df_clean['Confiança_IA_Desc'].notna()]

    if len(df_clean) == 0:
        st.warning("Não há dados válidos para exibir o gráfico.")
        return

    # Criar categorias de uso de IA para melhor visualização
    df_clean['Uso_IA_Categoria'] = pd.cut(
        df_clean['Uso_IA_Produtos'],
        bins=[0, 1, 2, 3, 4, 5],
        labels=['Muito Baixo (1)', 'Baixo (2)', 'Médio (3)', 'Alto (4)', 'Muito Alto (5)'],
        include_lowest=True
    )

    # Criar tabela cruzada
    cross = pd.crosstab(df_clean['Confiança_IA_Desc'], df_clean['Uso_IA_Categoria'])

    # Ordem das categorias de uso
    ordem_uso = ['Muito Baixo (1)', 'Baixo (2)', 'Médio (3)', 'Alto (4)', 'Muito Alto (5)']
    cross = cross.reindex(columns=ordem_uso, fill_value=0)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Distribuição do Uso de Produtos de IA por Nível de Confiança',
        labels={
            'Confiança_IA_Desc': 'Nível de Confiança na IA',
            'value': 'Número de Respondentes',
            'variable': 'Nível de Uso de Produtos de IA'
        },
        color_discrete_sequence=px.colors.sequential.Viridis,
        barmode='group'
    )

    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_profissoes_vs_emprego(df):
    """
    Barras empilhadas: faixa etária vs crença de que a IA vai eliminar profissões.
    Mostra, para cada faixa de idade, como se distribuem as respostas sobre
    eliminação de profissões.
    """
    idade_col = 'What is your age range?'
    if df is None or 'Elimina_Profissões_Desc' not in df.columns or idade_col not in df.columns:
        st.warning("Dados para idade ou para eliminação de profissões não disponíveis.")
        return

    st.markdown("### 10. Idade vs Crença na Eliminação de Profissões pela IA")

    # Tabela cruzada em porcentagem por faixa etária
    cross = pd.crosstab(df[idade_col], df['Elimina_Profissões_Desc'], normalize='index') * 100
    cross = cross.round(1)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Percepção de Eliminação de Profissões pela IA por Faixa Etária',
        labels={
            'index': 'Faixa etária',
            'value': 'Percentual dentro de cada faixa etária'
        },
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        xaxis={'title': 'Faixa etária'},
        yaxis={
            'gridcolor': 'rgba(255,255,255,0.1)',
            'title': 'Percentual dentro de cada faixa etária'
        },
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_impacto_por_conhecimento(df):
    """Impacto percebido da IA na humanidade por nível de conhecimento (faixas)."""
    if df is None or 'Conhecimento_IA' not in df.columns or 'Impacto_Humanidade_Desc' not in df.columns:
        st.warning("Dados para 'Conhecimento_IA' ou 'Impacto_Humanidade' não disponíveis.")
        return

    st.markdown("### 11. Impacto da IA na Humanidade por Nível de Conhecimento")

    # Mapear conhecimento textual para faixas (Baixo/Médio/Alto)
    conhec_raw = df['Conhecimento_IA'].astype(str).str.strip()
    baixa = ["I have no knowledge", "I've heard a little about it"]
    media = ["I have basic knowledge"]
    alta = ["I have a good level of knowledge"]

    def map_conhecimento(val):
        if val in baixa:
            return "Baixo"
        if val in media:
            return "Médio"
        if val in alta:
            return "Alto"
        return "Outro"

    df_local = df.copy()
    df_local['Conhecimento_IA_Faixa'] = conhec_raw.map(map_conhecimento)
    # Manter apenas as faixas Baixo/Médio/Alto no gráfico
    df_local = df_local[df_local['Conhecimento_IA_Faixa'].isin(['Baixo', 'Médio', 'Alto'])]

    cross = pd.crosstab(df_local['Conhecimento_IA_Faixa'], df_local['Impacto_Humanidade_Desc'], normalize='index') * 100
    cross = cross.round(1)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Percepção de Impacto da IA na Humanidade por Nível de Conhecimento',
        labels={
            'Conhecimento_IA_Faixa': 'Nível de Conhecimento em IA',
            'value': 'Percentual dentro de cada faixa de conhecimento'
        },
        color_discrete_sequence=px.colors.sequential.Sunset
    )

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_curso_vs_substituicao_emprego(df):
    """Barras agrupadas: curso vs percepção de substituição de empregos."""
    if df is None or 'Curso_Desc' not in df.columns or 'Substituicao_Emprego_Desc' not in df.columns:
        st.warning("Dados para 'Curso' ou 'Substituicao_Emprego' não disponíveis.")
        return

    st.markdown("### 12. Percepção de Substituição de Empregos por Curso")

    # Criar tabela cruzada usando a coluna descritiva
    cross = pd.crosstab(df['Curso_Desc'], df['Substituicao_Emprego_Desc'])
    
    # Ordem das categorias Likert
    ordem_likert = ['Discordo Fortemente', 'Discordo', 'Neutro', 'Concordo', 'Concordo Fortemente']
    cross = cross.reindex(columns=ordem_likert, fill_value=0)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Percepção de Substituição de Empregos pela IA por Curso',
        labels={
            'Curso': 'Curso',
            'value': 'Número de Respondentes',
            'variable': 'Nível de Concordância'
        },
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='group'
    )

    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_gpa_vs_conhecimento(df):
    """Scatter plot: GPA vs conhecimento sobre IA com linha de tendência."""
    if df is None or 'GPA' not in df.columns or 'Conhecimento_IA' not in df.columns:
        st.warning("Dados para 'GPA' ou 'Conhecimento_IA' não disponíveis.")
        return

    st.markdown("### 13. Relação entre GPA e Conhecimento sobre IA")

    # Filtrar valores válidos
    df_clean = df[df['GPA'].notna() & df['Conhecimento_IA'].notna()].copy()
    
    if len(df_clean) == 0:
        st.warning("Não há dados válidos para exibir o gráfico.")
        return

    # Criar scatter plot sem trendline (para evitar dependência de statsmodels)
    fig = px.scatter(
        df_clean,
        x='GPA',
        y='Conhecimento_IA',
        title='Relação entre GPA e Nível de Conhecimento sobre IA',
        labels={
            'GPA': 'GPA (Grade Point Average)',
            'Conhecimento_IA': 'Nível de Conhecimento sobre IA (1-10)'
        },
        color='Conhecimento_IA',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    # Adicionar linha de tendência simples usando numpy (sem statsmodels)
    if len(df_clean) > 1:
        x_vals = df_clean['GPA'].values
        y_vals = df_clean['Conhecimento_IA'].values
        
        # Calcular regressão linear simples
        coeffs = np.polyfit(x_vals, y_vals, 1)
        line_x = np.linspace(x_vals.min(), x_vals.max(), 100)
        line_y = np.polyval(coeffs, line_x)
        
        # Adicionar linha de tendência ao gráfico
        fig.add_trace(go.Scatter(
            x=line_x,
            y=line_y,
            mode='lines',
            name='Linha de Tendência',
            line=dict(color='#0099ff', width=2, dash='dash'),
            showlegend=True
        ))

    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'dtick': 1},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_fontes_ia(df):
    """Gráfico de barras: fontes de informação sobre IA."""
    if df is None:
        st.warning("Dados não disponíveis.")
        return

    st.markdown("### 14. Fontes de Informação sobre IA")

    # Verificar se as colunas de fontes existem
    fontes_cols = {
        'Internet': 'Q2#1.Internet',
        'Livros/Artigos': 'Q2#2.Books/Papers',
        'Redes Sociais': 'Q2#3.Social_media',
        'Discussões': 'Q2#4.Discussions',
        'Não me informo': 'Q2#5.NotInformed'
    }

    # Contar quantas pessoas usam cada fonte
    fontes_counts = {}
    for nome_pt, col_orig in fontes_cols.items():
        if col_orig in df.columns:
            # Contar quantos têm valor 1 (usam essa fonte)
            count = (df[col_orig] == 1).sum()
            fontes_counts[nome_pt] = count

    if len(fontes_counts) == 0:
        st.warning("Dados de fontes de informação sobre IA não disponíveis.")
        return

    # Criar DataFrame para o gráfico
    df_fontes = pd.DataFrame({
        'Fonte': list(fontes_counts.keys()),
        'Quantidade': list(fontes_counts.values())
    }).sort_values('Quantidade', ascending=False)

    # Criar gráfico de barras
    fig = px.bar(
        df_fontes,
        x='Fonte',
        y='Quantidade',
        title='Fontes de Informação sobre IA Utilizadas pelos Respondentes',
        labels={
            'Fonte': 'Fonte de Informação',
            'Quantidade': 'Número de Respondentes'
        },
        color='Quantidade',
        color_continuous_scale=px.colors.sequential.Plasma
    )

    fig.update_layout(
        template='plotly_dark',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'tickangle': -45},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_limites_eticos_vs_ia_consciente(df):
    """Barras empilhadas: limites éticos vs crença em IA consciente."""
    if df is None or 'Limites_Éticos_Desc' not in df.columns or 'IA_Consciente_Desc' not in df.columns:
        st.warning("Dados para 'Limites_Éticos' ou 'IA_Consciente' não disponíveis.")
        return

    st.markdown("### 14. Limites Éticos vs Crença em IA Consciente")

    cross = pd.crosstab(df['Limites_Éticos_Desc'], df['IA_Consciente_Desc'], normalize='index') * 100
    cross = cross.round(1)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Crença em Limites Éticos para IA vs Crença em IA Consciente',
        labels={
            'Limites_Éticos_Desc': 'Posição sobre Limites Éticos',
            'value': 'Percentual dentro de cada posição sobre limites éticos',
            'variable': 'Crença em IA Consciente'
        },
        color_discrete_sequence=px.colors.sequential.Mint
    )

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        xaxis={'categoryorder': 'array', 'categoryarray': ['Discordo Fortemente', 'Discordo', 'Neutro', 'Concordo', 'Concordo Fortemente']},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_educacao_vs_confianca(df):
    """Barras empilhadas: nível de educação vs confiança em IA."""
    if df is None or 'Nivel_Educacao_Desc' not in df.columns or 'Confiança_IA_Desc' not in df.columns:
        st.warning("Dados para 'Nível de Educação' ou 'Confiança_IA' não disponíveis.")
        return

    st.markdown("### 15. Nível de Educação vs Confiança em IA")

    cross = pd.crosstab(df['Nivel_Educacao_Desc'], df['Confiança_IA_Desc'], normalize='index') * 100
    cross = cross.round(1)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Confiança em IA por Nível de Educação',
        labels={
            'Nivel_Educacao_Desc': 'Nível de Educação',
            'value': 'Percentual dentro de cada nível de educação',
            'variable': 'Nível de Confiança'
        },
        color_discrete_sequence=px.colors.sequential.Sunset
    )

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_status_emprego_vs_risco(df):
    """Barras empilhadas: status de emprego vs risco ao próprio emprego."""
    if df is None or 'Status_Emprego_Desc' not in df.columns or 'Afeta_Emprego_Pessoal_Desc' not in df.columns:
        st.warning("Dados para 'Status de Emprego' ou 'Afeta_Emprego_Pessoal' não disponíveis.")
        return

    st.markdown("### 16. Status de Emprego vs Percepção de Risco ao Próprio Emprego")

    cross = pd.crosstab(df['Status_Emprego_Desc'], df['Afeta_Emprego_Pessoal_Desc'], normalize='index') * 100
    cross = cross.round(1)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Percepção de Risco ao Próprio Emprego por Status de Emprego',
        labels={
            'Status_Emprego_Desc': 'Status de Emprego',
            'value': 'Percentual dentro de cada status de emprego',
            'variable': 'Percepção de Risco'
        },
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_profissao_vs_risco_emprego(df):
    """Barras empilhadas: profissão vs percepção de risco ao próprio emprego."""
    if df is None or 'Profissao_Desc' not in df.columns or 'Afeta_Emprego_Pessoal_Desc' not in df.columns:
        st.warning("Dados para 'Profissão' ou 'Afeta_Emprego_Pessoal' não disponíveis.")
        return

    st.markdown("### 17. Profissão vs Percepção de Risco ao Próprio Emprego")

    # Filtrar apenas linhas com profissão informada (não vazia)
    df_clean = df[df['Profissao_Desc'].notna() & (df['Profissao_Desc'].astype(str).str.strip() != '')].copy()
    
    if len(df_clean) == 0:
        st.warning("Não há dados de profissão disponíveis para exibir o gráfico.")
        return

    # Limitar a profissões com pelo menos 3 respondentes para melhor visualização
    profissao_counts = df_clean['Profissao_Desc'].value_counts()
    profissoes_frequentes = profissao_counts[profissao_counts >= 3].index
    df_clean = df_clean[df_clean['Profissao_Desc'].isin(profissoes_frequentes)]

    if len(df_clean) == 0:
        st.warning("Não há profissões com número suficiente de respondentes para exibir o gráfico.")
        return

    # Criar tabela cruzada usando a coluna traduzida
    cross = pd.crosstab(df_clean['Profissao_Desc'], df_clean['Afeta_Emprego_Pessoal_Desc'], normalize='index') * 100
    cross = cross.round(1)

    # Ordenar profissões por frequência (mais respondentes primeiro)
    ordem_profissoes = df_clean['Profissao_Desc'].value_counts().index
    cross = cross.reindex(ordem_profissoes)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Percepção de Risco ao Próprio Emprego por Profissão',
        labels={
            'Profissao': 'Profissão',
            'value': 'Percentual dentro de cada profissão',
            'variable': 'Percepção de Risco'
        },
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'tickangle': -45},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_dispositivos_vs_uso_ia(df):
    """Barras agrupadas: frequência de uso de dispositivos tecnológicos vs uso de produtos de IA."""
    if df is None or 'Frequencia_Dispositivos_Desc' not in df.columns or 'Uso_IA_Produtos' not in df.columns:
        st.warning("Dados para 'Frequencia_Dispositivos' ou 'Uso_IA_Produtos' não disponíveis.")
        return

    st.markdown("### 18. Frequência de Uso de Dispositivos Tecnológicos vs Uso de Produtos de IA")

    # Filtrar valores válidos
    df_clean = df[df['Frequencia_Dispositivos_Desc'].notna() & df['Uso_IA_Produtos'].notna()].copy()
    
    if len(df_clean) == 0:
        st.warning("Não há dados válidos para exibir o gráfico.")
        return

    # Converter uso de IA para numérico se necessário
    if df_clean['Uso_IA_Produtos'].dtype == 'object':
        df_clean['Uso_IA_Produtos'] = pd.to_numeric(df_clean['Uso_IA_Produtos'], errors='coerce')

    # Criar categorias de uso de IA para melhor visualização
    df_clean['Uso_IA_Categoria'] = pd.cut(
        df_clean['Uso_IA_Produtos'],
        bins=[0, 1, 2, 3, 4, 5],
        labels=['Muito Baixo (1)', 'Baixo (2)', 'Médio (3)', 'Alto (4)', 'Muito Alto (5)'],
        include_lowest=True
    )

    # Criar tabela cruzada
    cross = pd.crosstab(df_clean['Frequencia_Dispositivos_Desc'], df_clean['Uso_IA_Categoria'], normalize='index') * 100
    cross = cross.round(1)

    # Ordem das frequências de dispositivos
    ordem_freq = ["0 a 2 horas por dia", "2 a 5 horas por dia", "5 a 10 horas por dia", "Mais de 10 horas por dia"]
    ordem_freq = [f for f in ordem_freq if f in cross.index]
    cross = cross.reindex(ordem_freq)

    fig = px.bar(
        cross,
        x=cross.index,
        y=cross.columns,
        title='Distribuição do Uso de Produtos de IA por Frequência de Uso de Dispositivos Tecnológicos',
        labels={
            'Frequencia_Dispositivos_Desc': 'Frequência de Uso de Dispositivos Tecnológicos',
            'value': 'Percentual dentro de cada frequência de uso',
            'variable': 'Nível de Uso de Produtos de IA'
        },
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'tickangle': -45},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_impacto_humanidade(df):
    if df is None or 'Impacto_Humanidade_Desc' not in df.columns:
        st.warning("Dados para 'Impacto_Humanidade' não disponíveis.")
        return
    
    st.markdown("### 7. Percepção do Impacto da IA na Humanidade")
    
    # Contagem de frequência
    impacto_counts = df['Impacto_Humanidade_Desc'].value_counts()
    
    # Criar o gráfico de pizza com Plotly
    fig = px.pie(
        impacto_counts,
        names=impacto_counts.index,
        values=impacto_counts.values,
        title='Percepção do Impacto da IA na Humanidade',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0, 0])
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_limites_eticos(df):
    if df is None or 'Limites_Éticos_Desc' not in df.columns:
        st.warning("Dados para 'Limites_Éticos' não disponíveis.")
        return
    
    st.markdown("### 8. Crença na Necessidade de Limites Éticos para a IA")
    
    # Definir a ordem correta para a escala Likert
    # Usamos "Neutro" para manter consistência com o restante dos gráficos.
    order = ['Discordo Fortemente', 'Discordo', 'Neutro', 'Concordo', 'Concordo Fortemente']
    
    # Contagem de frequência
    counts = df['Limites_Éticos_Desc'].value_counts().reindex(order).fillna(0)
    
    # Criar o gráfico de barras com Plotly
    fig = px.bar(
        counts,
        x=counts.index,
        y=counts.values,
        labels={'x': 'Nível de Concordância', 'y': 'Contagem de Respondentes'},
        title='A IA deve ser limitada por regras éticas?',
        color=counts.values,
        color_continuous_scale=px.colors.sequential.Mint
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
            plot_conhecimento_por_genero(df_survey)
            plot_conhecimento_vs_sentimento(df_survey)
            plot_gpa_vs_conhecimento(df_survey)
            plot_fontes_ia(df_survey)
        else:
            st.error("Não foi possível carregar os dados da Pesquisa Acadêmica. Verifique o arquivo 'Survey_AI.csv'.")

    with tab_impact:
        st.markdown("## Resultados da Pesquisa de Impacto Geral (Impact_AI_v2)")
        if df_impact is not None:
            plot_confianca_ia(df_impact)
            plot_impacto_humanidade(df_impact)
            plot_likert_scale(df_impact, 'Ameaça_Liberdades_Desc', '9. Ameaça às Liberdades Individuais pela IA')
            plot_limites_eticos(df_impact)
            plot_uso_ia_vs_confianca(df_impact)
            plot_profissoes_vs_emprego(df_impact)
            plot_impacto_por_conhecimento(df_impact)
        else:
            st.error("Não foi possível carregar os dados da Pesquisa de Impacto Geral. Verifique o arquivo 'Impact_AI_v2.csv'.")



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
            plot_conhecimento_por_genero(df_survey)
            plot_conhecimento_vs_sentimento(df_survey)
            plot_gpa_vs_conhecimento(df_survey)
            plot_fontes_ia(df_survey)
        else:
            st.error("Não foi possível carregar os dados da Pesquisa Acadêmica. Verifique o arquivo 'Survey_AI.csv'.")

    with tab_impact:
        st.markdown("## Resultados da Pesquisa de Impacto Geral (Impact_AI_v2)")
        if df_impact is not None:
            plot_confianca_ia(df_impact)
            plot_impacto_humanidade(df_impact)
            plot_likert_scale(df_impact, 'Ameaça_Liberdades_Desc', '9. Ameaça às Liberdades Individuais pela IA')
            plot_limites_eticos(df_impact)
            plot_uso_ia_vs_confianca(df_impact)
            plot_profissoes_vs_emprego(df_impact)
            plot_impacto_por_conhecimento(df_impact)
            plot_limites_eticos_vs_ia_consciente(df_impact)
            plot_educacao_vs_confianca(df_impact)
            plot_status_emprego_vs_risco(df_impact)
            plot_profissao_vs_risco_emprego(df_impact)
            plot_dispositivos_vs_uso_ia(df_impact)
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
        # Card Nicoli Felipe (imagem embutida em HTML para ficar dentro da caixa)
        try:
            with open("nicoli.felipe.jpg.jpeg", "rb") as f:
                img_bytes = f.read()
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")

            nicoli_html = f"""
            <div class="author-card">
                <img src="data:image/jpeg;base64,{img_b64}" class="profile-img" />
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
            """
            st.markdown(nicoli_html, unsafe_allow_html=True)
        except (FileNotFoundError, UnidentifiedImageError):
            st.warning("Não foi possível carregar a imagem da autora Nicoli. Verifique se o arquivo '../nicoli.felipe.jpg.jpeg' existe e é uma imagem JPEG válida.")
    
    with col2:
        # Card Mirian Sanches Fiorini (imagem embutida em HTML para ficar dentro da caixa)
        try:
            with open("mirian.sanches.jpg.jpeg", "rb") as f:
                img_bytes = f.read()
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")

            mirian_html = f"""
            <div class="author-card">
                <img src="data:image/jpeg;base64,{img_b64}" class="profile-img" />
                <h3> Mirian Sanches Fiorini</h3>
                <p>
                    <strong>Formação:</strong><br>
                    🎓 Graduanda em Ciência de Dados pela Faculdade SENAI de Informática (2025-2026)<br>
                    🎓 Técnica em Música pela Fundação das Artes (2022)<br><br>
                    <strong>ORCID:</strong> 0009-0003-1680-2542<br>
                    📧 sanchesmirian489@gmail.com
                </p>
            </div>
            """
            st.markdown(mirian_html, unsafe_allow_html=True)
        except (FileNotFoundError, UnidentifiedImageError):
            st.warning("Não foi possível carregar a imagem da autora Mirian. Verifique se o arquivo '../mirian.sanches.jpg.jpeg' existe e é uma imagem JPEG válida.")
    
    # Sobre a Orientadora
    st.markdown("## Sobre a Orientadora")
    
    try:
        with open("/Users/miriansanchesfiorini/Desktop/Arquivo 2/imagens/WhatsApp Image 2025-11-29 at 05.51.35.jpeg", "rb") as f:
            img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        jessica_html = f"""
        <div class="author-card">
            <img src="data:image/jpeg;base64,{img_b64}" class="profile-img" />
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
        """
        st.markdown(jessica_html, unsafe_allow_html=True)
    except (FileNotFoundError, UnidentifiedImageError):
        st.warning("Não foi possível carregar a imagem da orientadora Jéssica. Verifique se o arquivo '../jessica.franzon.jpg.jpeg' existe e é uma imagem JPEG válida.")
    
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
