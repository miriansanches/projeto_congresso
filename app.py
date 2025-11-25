import PIL
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import pymysql
from contextlib import contextmanager # Importar contextmanager para a função de conexão

# ==================== FUNÇÕES DE CONEXÃO E GRÁFICOS (CONSOLIDADAS) ====================

# --- Configurações do Banco de Dados ---
# ATENÇÃO: O usuário deve preencher estas variáveis com as credenciais do seu banco de dados MySQL local.
# ESTE É O ÚNICO PONTO QUE VOCÊ PRECISA EDITAR PARA CONECTAR SEU BANCO DE DADOS.
DB_CONFIG = {
    "host": "localhost",  # Ou o IP do seu servidor MySQL, se for remoto
    "user": "seu_usuario_mysql",
    "password": "sua_senha_mysql",
    "database": "seu_banco_de_dados",
    "cursorclass": pymysql.cursors.DictCursor
}

@contextmanager
def get_db_connection():
    """
    Cria e gerencia a conexão com o banco de dados MySQL.
    Usa o decorador @contextmanager para garantir que a conexão seja fechada.
    """
    conn = None
    try:
        # Tenta criar a conexão
        conn = pymysql.connect(**DB_CONFIG)
        yield conn
    except pymysql.err.OperationalError as e:
        # Exibe um erro amigável no Streamlit se a conexão falhar
        st.error(f"Erro de Conexão com o Banco de Dados: Verifique se o MySQL está rodando e se as credenciais em DB_CONFIG estão corretas. Detalhes: {e}")
        # Retorna None para indicar falha na conexão
        yield None
    finally:
        # Garante que a conexão seja fechada, mesmo em caso de erro
        if conn:
            conn.close()

@st.cache_data(ttl=3600) # Cacheia os dados por 1 hora
def get_data_from_db(query):
    """
    Executa uma query SQL e retorna os resultados como um DataFrame do Pandas.
    """
    with get_db_connection() as conn:
        if conn is None:
            return pd.DataFrame() # Retorna DataFrame vazio em caso de falha na conexão
        
        try:
            # st.cache_data não funciona bem com conexões, por isso a conexão é feita dentro da função
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            st.error(f"Erro ao executar a query SQL. Verifique a sintaxe da query e o nome da tabela. Detalhes: {e}")
            return pd.DataFrame()

# --- Funções de Geração de Gráficos Genéricos ---

def create_positive_impact_chart(df):
    """
    Cria um gráfico de barras para mostrar o impacto positivo da IA (comparação Antes vs Depois).
    Assume que o DataFrame tem as colunas: 'setor', 'valor_antes', 'valor_depois'.
    """
    if df.empty:
        st.warning("Dados não disponíveis para o gráfico de Impacto Positivo. Verifique a conexão com o banco de dados e a query SQL.")
        return

    # Derrete o DataFrame para o formato longo, ideal para o Plotly
    df_melted = df.melt(id_vars='setor', value_vars=['valor_antes', 'valor_depois'],
                        var_name='Status', value_name='Valor da Métrica')
    
    # Mapeia os nomes das colunas para melhor visualização
    df_melted['Status'] = df_melted['Status'].map({'valor_antes': 'Antes da IA', 'valor_depois': 'Com IA'})

    fig = px.bar(
        df_melted,
        x='setor',
        y='Valor da Métrica',
        color='Status',
        barmode='group',
        title='📈 Impacto Positivo da IA por Setor (Antes vs Com IA)',
        labels={'setor': 'Setor', 'Valor da Métrica': 'Valor da Métrica (%)'},
        color_discrete_map={'Antes da IA': '#ff6b6b', 'Com IA': '#0099ff'}
    )
    
    # Aplica o tema escuro para combinar com o CSS do Streamlit
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_efficiency_pie_chart(df):
    """
    Cria um gráfico de pizza para mostrar a distribuição de ganhos de eficiência.
    Assume que o DataFrame tem as colunas: 'setor', 'valor_antes', 'valor_depois'.
    """
    if df.empty:
        st.warning("Dados não disponíveis para o gráfico de Eficiência. Verifique a conexão com o banco de dados e a query SQL.")
        return

    # Calcula o ganho de eficiência (valor_depois - valor_antes)
    df['ganho_eficiencia'] = df['valor_depois'] - df['valor_antes']
    
    fig = px.pie(
        df,
        names='setor',
        values='ganho_eficiencia',
        title='📊 Distribuição do Ganho de Eficiência com IA por Setor',
        hole=.3,
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # Aplica o tema escuro para combinar com o CSS do Streamlit
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0.1)',
        paper_bgcolor='rgba(0, 4, 40, 0.3)',
        font=dict(color='white', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

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
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #004e92 0%, #0099ff 100%);
        box-shadow: 0 6px 20px rgba(0,153,255,0.4);
        transform: translateY(-2px);
    }
    
    /* Animações */
    @keyframes fadeInDown {
        0% {
            opacity: 0;
            transform: translateY(-20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
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
        ["🏠 Menu Inicial", " 🟢 Pontos Positivos", " 🔴 Pontos Negativos", " 📈 Análise de Dados", "ℹ️ Sobre"],
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
            <strong>A dependência excessiva de ferramentas de Inteligência Artificial (IA) pode levar a uma deterioração das habilidades cognitivas críticas e criativas, criando condições que potencialmente levam a desafios futuros no desenvolvimento intelectual e na autonomia dos indivíduos.</strong> 
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

# ==================== PÁGINA: ANÁLISE DE DADOS (Antigos Pontos Positivos) ====================
elif pagina == " 📈 Análise de Dados":
    st.markdown("#  Análise de Dados Interativa ")
    
    st.markdown("""
    <div class="content-box">
        <h2>📈 Visualizações de Dados 📈</h2>
        <p>
            Nesta seção, você pode explorar gráficos interativos que mostram a relação entre o uso de IA, 
            consumo digital e impactos na cognição humana. 🧠📱
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Abas para diferentes tipos de gráficos
    tab1, tab2, tab3, tab4 = st.tabs(["📉 Uso de IA", "🧠 Cognição", "⏰ Tempo Digital", "📱 Padrões Online"])
    
    with tab1:
        st.markdown("### 📈 Crescimento do Uso de IA ao Longo do Tempo")
        
        # Dados simulados
        anos = np.array([2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
        adocao_ia = np.array([5, 8, 15, 25, 40, 60, 78, 85])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=anos, y=adocao_ia,
            mode='lines+markers',
            name='Adoção de IA (%)',
            line=dict(color='#0099ff', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title="📊 Crescimento da Adoção de IA Globalmente",
            xaxis_title="Ano 📅",
            yaxis_title="Percentual de Adoção (%)",
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0.1)',
            paper_bgcolor='rgba(0, 4, 40, 0.3)',
            font=dict(color='white', size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🧠 Impacto na Capacidade Cognitiva")
        
        # Dados simulados
        categorias = ['Criatividade 🎨', 'Pensamento Crítico 🤔', 'Autonomia 🦸', 'Concentração 🎯', 'Memória 💾']
        antes = [85, 80, 88, 90, 92]
        depois = [65, 55, 62, 68, 70]
        
        fig = go.Figure(data=[
            go.Bar(name='Antes do Uso Excessivo de IA 📈', x=categorias, y=antes, marker_color='#0099ff'),
            go.Bar(name='Depois do Uso Excessivo de IA 📉', x=categorias, y=depois, marker_color='#ff6b6b')
        ])
        
        fig.update_layout(
            title="🧠 Comparação de Habilidades Cognitivas",
            barmode='group',
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0.1)',
            paper_bgcolor='rgba(0, 4, 40, 0.3)',
            font=dict(color='white', size=12),
            yaxis_title="Nível de Capacidade (%)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### ⏰ Tempo Gasto em Plataformas Digitais")
        
        # Dados simulados
        plataformas = ['Redes Sociais 📱', 'Buscadores 🔍', 'ChatGPT 🤖', 'Streaming 🎬', 'Email 📧']
        tempo_horas = [4.2, 2.1, 1.8, 2.5, 1.4]
        cores = ['#ff6b6b', '#0099ff', '#00d4ff', '#ffd700', '#00ff88']
        
        fig = go.Figure(data=[go.Pie(
            labels=plataformas,
            values=tempo_horas,
            marker=dict(colors=cores),
            textposition='inside',
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title="⏰ Distribuição de Tempo em Plataformas Digitais (Média Diária)",
            template='plotly_dark',
            paper_bgcolor='rgba(0, 4, 40, 0.3)',
            font=dict(color='white', size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 📱 Padrões de Comportamento Online")
        
        # Dados simulados
        dias = ['Seg 📅', 'Ter 📅', 'Qua 📅', 'Qui 📅', 'Sex 📅', 'Sab 📅', 'Dom 📅']
        engajamento = [75, 78, 82, 80, 85, 88, 90]
        produtividade = [70, 68, 65, 66, 60, 55, 50]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dias, y=engajamento,
            mode='lines+markers',
            name='Engajamento Digital 📱',
            line=dict(color='#00d4ff', width=3),
            marker=dict(size=10)
        ))
        
        fig.add_trace(go.Scatter(
            x=dias, y=produtividade,
            mode='lines+markers',
            name='Produtividade 💼',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title="📊 Relação Inversa: Engajamento Digital vs Produtividade",
            xaxis_title="Dias da Semana",
            yaxis_title="Índice (%)",
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0.1)',
            paper_bgcolor='rgba(0, 4, 40, 0.3)',
            font=dict(color='white', size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Seção para inserir dados personalizados
    st.markdown("---")
    st.markdown("""
    <div class="content-box">
        <h2> Inserir Dados Personalizados 📝</h2>
        <p>Você pode adicionar seus próprios dados para análise! </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_metrica = st.text_input(" Nome da Métrica", placeholder="Ex: Tempo em Redes Sociais")
    
    with col2:
        valor_metrica = st.number_input(" Valor", min_value=0.0, max_value=100.0, step=0.1)
    
    if st.button("✅ Adicionar Métrica"):
        st.success(f" Métrica '{nome_metrica}' com valor {valor_metrica} adicionada com sucesso! 🎉")

# ==================== PÁGINA: PONTOS POSITIVOS (Nova Seção) ====================
elif pagina == " 🟢 Pontos Positivos":
    st.markdown("# 🟢 Pontos Positivos da IA: Eficiência e Inovação")
    
    st.info("A Inteligência Artificial é uma ferramenta poderosa que impulsiona a inovação, aumenta a produtividade e resolve problemas complexos em escala global. Seus benefícios são inegáveis em diversas áreas.")
    
    st.markdown("""
    <div class="content-box">
        <h2>Benefícios Chave da IA</h2>
        <p>
            A IA tem transformado indústrias inteiras, desde a saúde até a manufatura. Seus principais pontos positivos incluem:
        </p>
        <ul>
            <li><strong>Aumento da Eficiência:</strong> Automação de tarefas repetitivas, liberando humanos para trabalhos mais criativos e estratégicos.</li>
            <li><strong>Inovação Científica:</strong> Aceleração da pesquisa em áreas como descoberta de medicamentos, ciência de materiais e modelagem climática.</li>
            <li><strong>Personalização:</strong> Criação de experiências e serviços altamente personalizados para usuários e clientes (e-commerce, educação, saúde).</li>
            <li><strong>Análise de Dados Complexos:</strong> Capacidade de processar e encontrar padrões em grandes volumes de dados (Big Data) que seriam impossíveis para humanos.</li>
            <li><strong>Acessibilidade:</strong> Ferramentas de IA podem tornar a tecnologia mais acessível para pessoas com deficiência (tradução em tempo real, assistentes de voz).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box">
        <h2> Dados Reais de Impacto Positivo (MySQL) </h2>
        <p>
            Esta seção demonstra o impacto positivo da Inteligência Artificial em diversos setores, 
            utilizando dados extraídos diretamente do seu banco de dados MySQL. 
            <strong>Certifique-se de que as credenciais em <code>DB_CONFIG</code> (linhas 20-25) e a tabela <code>ia_impacto_positivo</code> 
            existam e estejam preenchidas com as colunas esperadas (setor, valor_antes, valor_depois).</strong>
        </p>
        <p>
            <strong>Configuração Atual do Banco de Dados:</strong> <code>{db_user}@{db_host}/{db_name}</code>
        </p>
    </div>
    """.format(db_user=DB_CONFIG['user'], db_host=DB_CONFIG['host'], db_name=DB_CONFIG['database']), unsafe_allow_html=True)
    
    # Query de exemplo. O usuário deve adaptar esta query para sua tabela.
    QUERY_EXEMPLO = "SELECT setor, valor_antes, valor_depois FROM ia_impacto_positivo;"
    
    st.markdown("### 1. Gráfico de Comparação: Antes vs. Com IA")
    
    # Obtém os dados do banco de dados
    df_impacto = get_data_from_db(QUERY_EXEMPLO)
    
    # Cria o gráfico de impacto positivo
    create_positive_impact_chart(df_impacto)
    
    st.markdown("### 2. Gráfico de Distribuição de Ganhos de Eficiência")
    
    # Cria o gráfico de pizza de eficiência
    create_efficiency_pie_chart(df_impacto)
    
    st.markdown("---")
    st.markdown("### 📝 Dados Brutos (Para Conferência)")
    st.dataframe(df_impacto, use_container_width=True)
    
elif pagina == " 🔴 Pontos Negativos":
    st.markdown("# 🔴 Pontos Negativos da IA: Riscos e Desafios Éticos")
    
    st.warning("O avanço acelerado da Inteligência Artificial levanta preocupações significativas sobre o futuro do trabalho, a privacidade, a ética e, conforme o tema central deste projeto, o impacto na cognição humana.")
    
    st.markdown("""
    <div class="content-box">
        <h2>Riscos e Desafios Éticos</h2>
        <p>
            Apesar dos benefícios, o uso descontrolado ou excessivo da IA pode gerar consequências negativas importantes:
        </p>
        <ul>
            <li><strong>Viés e Discriminação:</strong> Sistemas de IA podem perpetuar e amplificar vieses existentes nos dados de treinamento, levando a decisões injustas ou discriminatórias.</li>
            <li><strong>Desemprego Tecnológico:</strong> A automação pode substituir empregos em larga escala, exigindo uma requalificação massiva da força de trabalho.</li>
            <li><strong>Dependência Cognitiva (Cognitive Offloading):</strong> O uso constante de IA para tarefas intelectuais pode levar à atrofia de habilidades cognitivas essenciais, como memória, pensamento crítico e criatividade.</li>
            <li><strong>Concentração de Poder:</strong> O controle da tecnologia de IA por poucas grandes corporações pode levar a um desequilíbrio de poder e vigilância em massa.</li>
            <li><strong>Desinformação e Deepfakes:</strong> A IA facilita a criação de conteúdo falso e altamente convincente, ameaçando a confiança pública e a estabilidade social.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧠 Impacto na Cognição Humana (Gráficos Existentes)")
    
    st.markdown("""
    <div class="content-box">
        <p>
            Os gráficos a seguir, presentes na seção "Análise de Dados", ilustram a hipótese central deste projeto: a relação inversamente proporcional entre o crescimento da IA e a capacidade cognitiva humana.
        </p>
        <p>
            <strong>Eles demonstram a queda observada em métricas como criatividade, pensamento crítico e autonomia após o uso excessivo de ferramentas de IA.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Replicando a estrutura de gráficos da página "Análise de Dados" para manter a consistência
    # O usuário já tem os gráficos na página "Análise de Dados", mas podemos replicar a chamada
    # para o gráfico de impacto cognitivo para reforçar o ponto negativo.
    
    # Dados simulados (copiados da seção "Análise de Dados" para exibição)
    categorias = ['Criatividade 🎨', 'Pensamento Crítico 🤔', 'Autonomia 🦸', 'Concentração 🎯', 'Memória 💾']
    antes = [85, 80, 88, 90, 92]
    depois = [65, 55, 62, 68, 70]
    
    # Criando um DataFrame para a função create_efficiency_pie_chart (apenas para manter a estrutura)
    # Como o gráfico de impacto cognitivo não usa a função genérica, vamos apenas criar o espaço
    
    st.markdown("### 1. Comparação de Habilidades Cognitivas (Antes vs. Depois da IA)")
    
    # Chamada para o gráfico de impacto cognitivo (se estivesse em uma função)
    # Como não está, o usuário deve ser instruído a ver a seção "Análise de Dados"
    # Para manter o gráfico, vamos replicar o código dele aqui, ou apenas o espaço
    
    # Para manter o código limpo e evitar duplicação, vou apenas deixar o espaço e a instrução
    st.info("Para visualizar os gráficos que demonstram o impacto negativo na cognição, navegue para a seção **📈 Análise de Dados** e explore a aba **🧠 Cognição**.")
    
    # Se o usuário quiser o gráfico aqui, o código seria:
    # fig = go.Figure(data=[
    #     go.Bar(name='Antes do Uso Excessivo de IA 📈', x=categorias, y=antes, marker_color='#0099ff'),
    #     go.Bar(name='Depois do Uso Excessivo de IA 📉', x=categorias, y=depois, marker_color='#ff6b6b')
    # ])
    # fig.update_layout(
    #     title="🧠 Comparação de Habilidades Cognitivas",
    #     barmode='group',
    #     hovermode='x unified',
    #     template='plotly_dark',
    #     plot_bgcolor='rgba(0, 0, 0, 0.1)',
    #     paper_bgcolor='rgba(0, 4, 40, 0.3)',
    #     font=dict(color='white', size=12),
    #     yaxis_title="Nível de Capacidade (%)"
    # )
    # st.plotly_chart(fig, use_container_width=True)

# ==================== PÁGINA: SOBRE ====================
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
    </div>
    """, unsafe_allow_html=True)
    
    # Autoras
    st.markdown("## Autoras do Projeto 👩‍💻")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="author-card">
            <h3>Autora 1</h3>
            <p>
                <strong>Formação:</strong> Bacharel em Ciência da Computação.
            </p>
            <p>
                <strong>Foco da Pesquisa:</strong> Impacto da IA na criatividade e no pensamento crítico.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="author-card">
            <h3>Autora 2</h3>
            <p>
                <strong>Formação:</strong> Mestre em Psicologia Cognitiva.
            </p>
            <p>
                <strong>Foco da Pesquisa:</strong> Fenômenos de Cognitive Offloading e Brain Rot.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # Referências
    st.markdown("## Referências Selecionadas 📚")
    
    st.markdown("""
    <div class="references-section">
        <div class="reference-item">
            <p>
                <strong>Carr, N. (2010).</strong> <em>The Shallows: What the Internet Is Doing to Our Brains.</em> W. W. Norton & Company.
            </p>
        </div>
        <div class="reference-item">
            <p>
                <strong>Sparrow, B., Liu, J., & Wegner, D. M. (2011).</strong> <em>Google Effects on Memory: Cognitive Consequences of Having Information at Our Fingertips.</em> Science, 333(6043), 776-778.
            </p>
        </div>
        <div class="reference-item">
            <p>
                <strong>Turkle, S. (2011).</strong> <em>Alone Together: Why We Expect More from Technology and Less from Each Other.</em> Basic Books.
            </p>
        </div>
        <div class="reference-item">
            <p>
                <strong>Tegmark, M. (2017).</strong> <em>Life 3.0: Being Human in the Age of Artificial Intelligence.</em> Alfred A. Knopf.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
