import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="AgroStack - Score Agro", layout="wide", initial_sidebar_state="expanded")

# 2. INJEÇÃO DE CSS (A MÁGICA DO DESIGN PREMIUM)
st.markdown("""
    <style>
    /* Cor de fundo do menu lateral (Azul Escuro Corporativo) */
    [data-testid="stSidebar"] {
        background-color: #0A3A60;
    }
    /* Letras do menu lateral em branco */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Fundo da tela principal levemente cinza para destacar os cards */
    .stApp {
        background-color: #F4F7F6;
    }
    
    /* Estilo dos Cards de Score (Bordas, fundo branco e sombra) */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E6ED;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Ajuste na barra de busca */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #0A3A60;
    }
    </style>
""", unsafe_allow_html=True)

# 3. MENU LATERAL
with st.sidebar:
    st.title("🌱 SCORE AGRO")
    st.markdown("---")
    st.markdown("🏠 Dashboard")
    st.markdown("🔍 Consulta de Score")
    st.markdown("👥 Produtores")
    st.markdown("📊 Análises")

# 4. CABEÇALHO E BUSCA
st.header("Score Agro - Sistema de Análise para Instituições Financeiras")
st.write("Consulte o score de produtores rurais para decisões de crédito")

col_busca, col_vazia = st.columns([3, 1])
with col_busca:
    cpf_busca = st.text_input("", placeholder="Digite o CPF do produtor (Ex: 123.456.789-00)")

st.markdown("---")

# 5. CARDS DE SCORE
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="🛡️ SCORE FINAL", value="750", delta="Risco: BAIXO", delta_color="normal")
with col2:
    st.metric(label="📍 SCORE REGIONAL", value="420", delta="Maringá - PR", delta_color="off")
with col3:
    st.metric(label="👤 SCORE INDIVIDUAL", value="330", delta="+78% acima da média", delta_color="normal")
with col4:
    st.metric(label="✅ RECOMENDAÇÃO", value="APROVAR", delta="Taxa: 8,5% a.a.", delta_color="normal")

st.markdown("---")

# 6. MAPA DE SATÉLITE E TABELA
col_mapa, col_detalhes = st.columns([1.5, 1])

with col_mapa:
    st.subheader("📍 Localização da Fazenda")
    
    # Conserto do Mapa: Usando imagem real de satélite (Esri World Imagery)
    mapa_fazenda = folium.Map(
        location=[-23.4205, -51.9333], 
        zoom_start=15, 
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri'
    )
    
    # Desenhando o talhão verde da fazenda
    folium.Polygon(
        locations=[[-23.419, -51.934], [-23.419, -51.931], [-23.422, -51.932], [-23.421, -51.935]],
        color='#00FF00', fill=True, fill_color='#00FF00', fill_opacity=0.4, weight=3
    ).add_to(mapa_fazenda)
    
    st_folium(mapa_fazenda, width=700, height=350, returned_objects=[])
    
with col_detalhes:
    st.subheader("📊 Detalhes do Produtor")
    dados_produtor = pd.DataFrame({
        "Critério": ["👤 Nome", "🪪 CPF", "🧪 Análise de Solo", "💧 Pivô/Irrigação", "💰 Sem Dívidas", "📈 Hedge"],
        "Status": ["João Silva", "123.456.789-00", "✅ Sim", "✅ Sim", "✅ Sim", "✅ Sim"],
        "Impacto": ["-", "-", "(+50)", "(+40)", "(+50)", "(+30)"]
    })
    st.dataframe(dados_produtor, hide_index=True, use_container_width=True)
    st.success("📝 Histórico: 5 anos sem inadimplência")
