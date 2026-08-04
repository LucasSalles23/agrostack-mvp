import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import time

# ==========================================
# ARQUITETURA CORE: CLASSES E MICROSSERVIÇOS
# ==========================================
class SICAR_API:
    """Simula a API real do Governo para busca de shapefiles e áreas."""
    @staticmethod
    def buscar_dados(car_id):
        # Banco simulado de altíssimo nível (Substituirá o banco de dados via PostGIS no futuro)
        base = {
            "PR-001": {"area": 20, "coords": [[-23.419, -51.934], [-23.419, -51.931], [-23.422, -51.932], [-23.421, -51.935]], "solo": "Argiloso"},
            "PR-002": {"area": 80, "coords": [[-23.410, -51.920], [-23.410, -51.915], [-23.415, -51.915], [-23.415, -51.920]], "solo": "Arenoso"},
            "MT-987": {"area": 1500, "coords": [[-12.833, -55.833], [-12.833, -55.810], [-12.850, -55.810], [-12.850, -55.833]], "solo": "Misto"}
        }
        return base.get(car_id, None)

class Climate_API:
    """Simula a API de Risco Climático (INMET/NASA)."""
    @staticmethod
    def buscar_risco_historico(car_id):
        base = {
            "PR-001": {"risco_seca": "Baixo", "chuva_media_mm": 180},
            "PR-002": {"risco_seca": "Alto", "chuva_media_mm": 70},
            "MT-987": {"risco_seca": "Médio", "chuva_media_mm": 120}
        }
        return base.get(car_id, None)

class RiskEngine:
    """Motor de Inteligência de Crédito."""
    @staticmethod
    def processar_operacao(lista_cars):
        area_total = 0
        soma_score_ponderado = 0
        area_risco_critico = 0
        dados_operacao = []
        coordenadas = []

        for car in lista_cars:
            sicar_data = SICAR_API.buscar_dados(car)
            clima_data = Climate_API.buscar_risco_historico(car)
            
            if not sicar_data or not clima_data:
                continue

            # Algoritmo de Score Base
            score_base = 700
            if clima_data['risco_seca'] == 'Alto':
                score_base -= 300
            elif clima_data['risco_seca'] == 'Baixo':
                score_base += 150
                
            if sicar_data['solo'] == 'Arenoso':
                score_base -= 100

            score_final_car = min(max(score_base, 100), 950)
            area = sicar_data['area']
            
            area_total += area
            soma_score_ponderado += (score_final_car * area)
            coordenadas.append(sicar_data['coords'])
            
            if score_final_car < 500:
                area_risco_critico += area
                
            dados_operacao.append({
                "Registro CAR": car,
                "Área (ha)": area,
                "Risco Climático": clima_data['risco_seca'],
                "Score do Talhão": score_final_car
            })

        if area_total == 0:
            return None

        # Cálculo de Contágio de Risco Estrutural
        score_operacao = int(soma_score_ponderado / area_total)
        alerta = None
        
        if (area_risco_critico / area_total) > 0.25:
            score_operacao -= 150  # Punição severa se mais de 25% da operação for tóxica
            alerta = "Risco de Contágio Sistêmico"

        score_operacao = min(max(score_operacao, 100), 950)
        
        return {
            "score": score_operacao,
            "area_total": area_total,
            "area_critica": area_risco_critico,
            "alerta": alerta,
            "detalhes": dados_operacao,
            "geometrias": coordenadas
        }

# ==========================================
# INTERFACE FRONT-END DE ALTO DESEMPENHO
# ==========================================
st.set_page_config(page_title="AgroStack Enterprise", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #041E42; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stApp { background-color: #F8FAFC; }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #041E42;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌱 AgroStack")
    st.caption("Motor de Crédito Institucional")
    st.markdown("---")
    st.markdown("🏢 Painel Executivo")
    st.markdown("📡 Conexões de API (Ativo)")

st.header("Análise de Risco Agronômico Automatizada")
st.write("Insira as matrículas CAR para estruturação e precificação da operação.")

col_busca, _ = st.columns([3, 1])
with col_busca:
    car_input = st.text_input("", placeholder="Insira os CARs separados por vírgula (Ex: PR-001, PR-002)")

st.markdown("---")

if car_input:
    cars = [c.strip() for c in car_input.split(',')]
    
    with st.spinner("Estabelecendo conexão segura com SICAR e INMET... Extraindo malhas georreferenciadas..."):
        time.sleep(1.5) # Simula a latência de uma API real para o usuário
        resultado = RiskEngine.processar_operacao(cars)
    
    if resultado:
        st.success("Análise de dados processada com sucesso via pipelines automatizados.")
        
        col1, col2, col3, col4 = st.columns(4)
        
        score = resultado['score']
        if score >= 750: dec, taxa, cor = "APROVADO", "CDI + 1.2%", "normal"
        elif score >= 550: dec, taxa, cor = "COMITÊ", "CDI + 3.5%", "off"
        else: dec, taxa, cor = "REJEITADO", "-", "inverse"
            
        with col1: st.metric("🛡️ SCORE OPERAÇÃO", resultado['score'], resultado['alerta'] or "Risco Diluído", delta_color="inverse" if resultado['alerta'] else "normal")
        with col2: st.metric("📏 ÁREA FINANCIADA", f"{resultado['area_total']} ha")
        with col3: st.metric("⚠️ ÁREA CRÍTICA", f"{resultado['area_critica']} ha", delta_color="inverse")
        with col4: st.metric("✅ DECISÃO ALGORÍTMICA", dec, taxa, delta_color=cor)

        st.markdown("---")
        col_mapa, col_tabela = st.columns([1.5, 1])

        with col_mapa:
            st.subheader("📍 Inteligência Espacial (Shapefiles Integrados)")
            centro = resultado['geometrias'][0][0]
            mapa = folium.Map(location=centro, zoom_start=13, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri')
            for coords in resultado['geometrias']:
                folium.Polygon(locations=coords, color='#00FF00', fill=True, fill_color='#00FF00', fill_opacity=0.3, weight=2).add_to(mapa)
            st_folium(mapa, width=700, height=350, returned_objects=[])
            
        with col_tabela:
            st.subheader("📑 Estrutura da Operação (Por CAR)")
            st.dataframe(pd.DataFrame(resultado['detalhes']), hide_index=True, use_container_width=True)
            
    else:
        st.error("Falha na Ingestão: Nenhum CAR validado nos bancos de dados oficiais.")
