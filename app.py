import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# ==========================================
# 1. BANCO DE DADOS SIMULADO (MVP)
# ==========================================
# Aqui ficam os dados que no futuro virão do SICAR e do produtor
banco_de_dados = {
    "PR-12345": {
        "nome": "Lucas Xavier",
        "cultura": "Soja",
        "area_total": 200,
        "area_arrendada": 20, # O detalhe que você bem observou!
        "chuva_mm": 180,
        "irrigacao": "Sim",
        "zarc": "Dentro do ZARC",
        "tecnologia": "Alto",
        "coords": [[-23.419, -51.934], [-23.419, -51.931], [-23.422, -51.932], [-23.421, -51.935]]
    },
    "MT-98765": {
        "nome": "Fazenda Querência",
        "cultura": "Milho",
        "area_total": 1500,
        "area_arrendada": 1500,
        "chuva_mm": 80, # Seca!
        "irrigacao": "Não",
        "zarc": "Fora do ZARC",
        "tecnologia": "Médio",
        "coords": [[-12.833, -55.833], [-12.833, -55.810], [-12.850, -55.810], [-12.850, -55.833]]
    }
}

# ==========================================
# 2. MOTOR DE CÁLCULO (O Cérebro do Colab)
# ==========================================
def calcular_score(dados):
    score = 500
    chuva = dados['chuva_mm']
    
    if dados['cultura'] == 'Soja':
        if 120 <= chuva <= 200: score += 120
        elif chuva < 90:
            if dados['irrigacao'] == 'Sim': score += 50
            else: score -= 200
    else:
        if 150 <= chuva <= 250: score += 120
        elif chuva < 110:
            if dados['irrigacao'] == 'Sim': score += 50
            else: score -= 220

    if dados['tecnologia'] == 'Alto': score += 100
    if dados['zarc'] == 'Dentro do ZARC': score += 120
    else: score -= 300

    score = min(max(score, 100), 950)
    
    if score >= 750: return score, "APROVAR", "BAIXO", "green", "Taxa: 8,5% a.a."
    elif score >= 600: return score, "REVISÃO", "MÉDIO", "orange", "Análise Manual"
    else: return score, "NEGAR", "ALTO", "red", "Risco de Quebra"

# ==========================================
# 3. INTERFACE VISUAL (CSS e Layout)
# ==========================================
st.set_page_config(page_title="AgroStack - Score Agro", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0A3A60; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stApp { background-color: #F4F7F6; }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF; border: 1px solid #E0E6ED; padding: 15px; border-radius: 12px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌱 SCORE AGRO")
    st.markdown("---")
    st.markdown("🏠 Dashboard")
    st.markdown("🔍 Consulta de Score")

st.header("Score Agro - Análise de Risco Georreferenciada")
st.write("Digite o número do CAR para iniciar a análise em tempo real.")

col_busca, _ = st.columns([3, 1])
with col_busca:
    car_busca = st.text_input("", placeholder="Digite o CAR (Ex: PR-12345 ou MT-98765)")

st.markdown("---")

# ==========================================
# 4. LÓGICA DE EXIBIÇÃO DINÂMICA
# ==========================================
if car_busca in banco_de_dados:
    fazenda = banco_de_dados[car_busca]
    score, recomendacao, risco, cor, taxa = calcular_score(fazenda)
    
    # Renderiza os Cards Dinâmicos
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="🛡️ SCORE FINAL", value=score, delta=f"Risco: {risco}")
    with col2: st.metric(label="📏 ÁREA AVALIADA", value=f"{fazenda['area_arrendada']} ha", delta=f"de {fazenda['area_total']} ha totais")
    with col3: st.metric(label="🌧️ CHUVA NA FLORADA", value=f"{fazenda['chuva_mm']} mm", delta=fazenda['zarc'])
    with col4: st.metric(label="✅ RECOMENDAÇÃO", value=recomendacao, delta=taxa)

    st.markdown("---")
    col_mapa, col_detalhes = st.columns([1.5, 1])

    with col_mapa:
        st.subheader("📍 Localização do CAR")
        centro_mapa = fazenda['coords'][0]
        mapa = folium.Map(location=centro_mapa, zoom_start=14, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri')
        
        folium.Polygon(
            locations=fazenda['coords'], color='#00FF00', fill=True, fill_color='#00FF00', fill_opacity=0.4, weight=3
        ).add_to(mapa)
        
        st_folium(mapa, width=700, height=350, returned_objects=[])
        
    with col_detalhes:
        st.subheader("📊 Resumo Agronômico")
        df_detalhes = pd.DataFrame({
            "Critério": ["👤 Produtor", "🌱 Cultura", "💧 Irrigação", "⚙️ Tecnologia"],
            "Status": [fazenda['nome'], fazenda['cultura'], fazenda['irrigacao'], fazenda['tecnologia']]
        })
        st.dataframe(df_detalhes, hide_index=True, use_container_width=True)
        
elif car_busca:
    st.warning("CAR não encontrado na base de dados. Tente 'PR-12345' ou 'MT-98765'.")
