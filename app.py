import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="AgroStack - Score Agro", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1892/1892751.png", width=50)
    st.title("SCORE AGRO")
    st.markdown("---")
    st.button("🏠 Dashboard")
    st.button("🔍 Consulta de Score")
    st.button("👥 Produtores")
    st.button("📊 Análises")

st.header("Score Agro - Sistema de Análise")
st.write("Consulte o score de produtores rurais para decisões de crédito")

col_busca, col_vazia = st.columns([3, 1])
with col_busca:
    cpf_busca = st.text_input("Digite o CPF do produtor:", placeholder="Ex: 123.456.789-00")

st.markdown("---")

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

col_mapa, col_detalhes = st.columns([1.5, 1])

with col_mapa:
    st.subheader("📍 Localização da Fazenda")
    mapa_fazenda = folium.Map(location=[-23.4205, -51.9333], zoom_start=15, tiles='Stamen Terrain')
    folium.Polygon(
        locations=[[-23.419, -51.934], [-23.419, -51.931], [-23.422, -51.932], [-23.421, -51.935]],
        color='green', fill=True, fill_color='lightgreen', fill_opacity=0.6
    ).add_to(mapa_fazenda)
    st_folium(mapa_fazenda, width=700, height=350)
    
with col_detalhes:
    st.subheader("📊 Detalhes do Produtor")
    dados_produtor = pd.DataFrame({
        "Critério": ["👤 Nome", "🪪 CPF", "🧪 Análise de Solo", "💧 Pivô/Irrigação"],
        "Status": ["João Silva", "123.456.789-00", "✅ Sim", "✅ Sim"],
        "Impacto Score": ["-", "-", "(+50)", "(+40)"]
    })
    st.dataframe(dados_produtor, hide_index=True, use_container_width=True)
    st.success("📝 Histórico: 5 anos sem inadimplência")
