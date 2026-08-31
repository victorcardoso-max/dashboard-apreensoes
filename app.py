import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página (Modo amplo com visual clean)
st.set_page_config(
    page_title="Histórico de Apreensões por Frota",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS personalizada para replicar os cards brancos e fontes modernas
st.markdown("""
<style>
    .main {
        background-color: #f4f5f7;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 13px;
        color: #6b7280;
        font-weight: 500;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
    }
    .metric-sub {
        font-size: 12px;
        color: #9ca3af;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. CARREGAMENTO DOS DADOS (Exemplo com arquivo local ou URL do Google Sheets)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Substitua pelo caminho do seu arquivo Excel ou link CSV do Google Sheets
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-.../pub?output=csv")
    return df

# Para teste rápido com dados simulados idênticos à tela:
df_semanas = pd.DataFrame({
    'Semana': ['11/Mai', '18/Mai', '25/Mai', '01/Jun', '08/Jun', '15/Jun', '22/Jun', '29/Jun', '06/Jul', '13/Jul', '20/Jul', '27/Jul', '03/Ago', '10/Ago', '17/Ago', '24/Ago'],
    'Custo Total': [2000, 533, 3600, 8600, 1500, 6100, 5800, 4400, 4600, 7900, 8800, 3100, 3000, 1400, 5400, 3000],
    'Motos': [4, 1, 4, 10, 2, 8, 7, 6, 5, 9, 12, 4, 5, 2, 8, 5]
})

df_motivos = pd.DataFrame({
    'Motivo': ['Sem CNH', 'Acidente', 'Local proibido', 'Bafômetro', 'Interr. via', 'Ativ. ilícitas', 'S/ equip. obrig.', 'Placa ilegível'],
    'Pct': [35.5, 8.8, 8.5, 7.5, 5.7, 5.7, 4.7, 4.4]
})

# ---------------------------------------------------------
# 2. CABEÇALHO E FILTROS TIPO "PILL"
# ---------------------------------------------------------
st.caption("PILAR 03 · RECUPERAÇÃO DE MOTOS — DADOS")
st.title("Histórico de Apreensões por Frota")

# Botões de navegação superior
col_aba1, col_aba2, _ = st.columns([1.5, 2, 6])
with col_aba1:
    st.button("Recuperação de Motos (318)", type="primary", use_container_width=True)
with col_aba2:
    st.button("Segunda Via de Placas (174)", type="secondary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. PAINEL PRINCIPAL (KPIs + GRÁFICO + TOP MOTIVOS)
# ---------------------------------------------------------
col_left, col_center, col_right = st.columns([1.2, 3.5, 1.8])

with col_left:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">apreensões (histórico)</div>
        <div class="metric-value" style="color: #FF6B00;">318</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">custo médio de remoção</div>
        <div class="metric-value" style="color: #38BDF8;">R$ 485</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">tempo médio de recuperação</div>
        <div class="metric-value" style="color: #22C55E;">8,5d</div>
    </div>
    """, unsafe_allow_html=True)

with col_center:
    # Controles superiores do gráfico
    ctrl_col1, ctrl_col2 = st.columns([2, 1])
    with ctrl_col2:
        opcao_visu = st.segmented_control("", options=["Qtd.", "Custo total", "Custo médio"], default="Custo total")

    # Cores das barras (destacando a barra de pico em Laranja)
    cores = ['#38BDF8' if c != 8800 else '#FF6B00' for c in df_semanas['Custo Total']]

    fig_barras = px.bar(
        df_semanas, 
        x='Semana', 
        y='Custo Total',
        text_auto='.2s',
        title="Custo total semanais — últimas 16 semanas"
    )
    fig_barras.update_traces(marker_color=cores, textposition='outside')
    fig_barras.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="",
        yaxis_title="",
        height=380,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_barras, use_container_width=True)

with col_right:
    st.markdown("**TOP MOTIVOS**")
    for _, row in df_motivos.iterrows():
        col_m1, col_m2 = st.columns([3, 1])
        col_m1.caption(row['Motivo'])
        col_m2.markdown(f"<span style='color:#FF6B00; font-weight:bold;'>{row['Pct']}%</span>", unsafe_allow_html=True)
        st.progress(row['Pct'] / 100)
