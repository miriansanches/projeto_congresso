import PIL
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np


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
    
    st.markdown("### 🧠 1. Cognitive Offloading")
    st.markdown("""
    Terceirizar etapas do raciocínio para ferramentas externas (listas, GPS, buscadores, IA) a fim de reduzir esforço. 
    Este processo altera a fronteira funcional entre o que mantemos "na cabeça" e o que deixamos "no mundo", 
    especialmente sob hiper acesso à informação. 
    """)
    
    st.markdown("### 🔴 2. Brain Rot - Apodrecimento Mental")
    st.markdown("""
    Termo cunhado por Henry David Thoreau no século XIX, ganhou ressignificação moderna relacionada ao uso excessivo de redes sociais. 
    Refere-se ao fenômeno de sobrecarga cerebral com processamento rápido de grande volume de informações superficiais. 
    Em dezembro de 2024, foi escolhido como expressão do ano pelo Dicionário Oxford! 
    """)
    
    st.markdown("### 🌫️ 3. Mental Fog - Confusão Mental")
    st.markdown("""
    Estado de confusão mental caracterizado por dificuldade de concentração, lapsos de memória, lentidão no raciocínio 
    e sensação de exaustão cognitiva. Associado a alterações na memória de trabalho, atenção seletiva e fluência verbal. 😵
    """)
    
    st.markdown("### 💊 4. Dependência de Ferramentas de IA")
    st.markdown("""
    A dependência de ferramentas como ChatGPT pode afetar negativamente a concentração, memória, aprendizagem a longo prazo 
    e capacidade de resolução autônoma de problemas entre estudantes. Diminui a interação social e os debates, 
    limitando o desenvolvimento de habilidades comunicativas e colaborativas. 
    """)
    
    # Estatísticas e Dados
    st.markdown("##  Dados Importantes ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-box">
            <h4>5.4%</h4>
            <p>Ganho em novidade com 1 sugestão de IA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-box">
            <h4>8.1%</h4>
            <p>Ganho em novidade com 5 sugestões de IA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-box">
            <h4>3.7%</h4>
            <p>Ganho em utilidade com 1 sugestão</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-box">
            <h4>9.0%</h4>
            <p>Ganho em utilidade com 5 sugestões</p>
        </div>
        """, unsafe_allow_html=True)
    
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
        <h2>📝 Inserir Dados Personalizados 📝</h2>
        <p>Você pode adicionar seus próprios dados para análise! 🚀</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_metrica = st.text_input("📊 Nome da Métrica", placeholder="Ex: Tempo em Redes Sociais")
    
    with col2:
        valor_metrica = st.number_input("📈 Valor", min_value=0.0, max_value=100.0, step=0.1)
    
    if st.button("✅ Adicionar Métrica"):
        st.success(f"✨ Métrica '{nome_metrica}' com valor {valor_metrica} adicionada com sucesso! 🎉")

# ==================== PÁGINA: SOBRE ====================
elif pagina == "ℹ️ Sobre":
    st.markdown("# ℹ️ Sobre o Projeto ℹ️")
    
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
    st.markdown("## 👩‍🎓 Sobre as Autoras 👩‍🎓")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="author-card">
            <img src="nicoli_felipe.jpg" class="profile-img"> <!-- Imagem da Autora -->
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
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="author-card">
            <img src="nicoli_felipe.jpg" class="profile-img"> <!-- Imagem da Autora -->
            <h3> Mirian Sanches Fiorini</h3>
            <p>
                <strong>Formação:</strong><br>
                🎓 Graduanda em Ciência de Dados pela Faculdade SENAI de Informática (2025-2026)<br>
                🎓 Técnica em Música pela Fundação das Artes (2022)<br><br>
                <strong>ORCID:</strong> 0009-0003-1680-2542<br>
                📧 sanchesmirian489@gmail.com
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
</div>
""", unsafe_allow_html=True)

