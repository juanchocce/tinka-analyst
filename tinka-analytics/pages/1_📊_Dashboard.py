import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from modules import etl, analysis

st.set_page_config(page_title="Dashboard Científico", page_icon="📊", layout="wide")

# Load CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# LOAD DATA
df_draws, df_exploded = etl.load_data()

if df_draws.empty:
    st.error("No se encontró el archivo de datos. Por favor verifica 'data/tinka_data.csv'")
    st.stop()

st.title("📊 Panel de Control Estadístico")
st.markdown("Análisis de la era moderna de La Tinka (Oct 2022 - Presente | 50 Bolillas)")

# Top KPIs
current_sorteo = df_draws['Sorteo'].max() if 'Sorteo' in df_draws.columns else 0
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sorteos Analizados", len(df_draws))
with col2:
    entropy = analysis.get_entropy(df_exploded)
    st.metric("Entropía del Sistema", f"{entropy:.4f}", delta="Ideal: 3.91")
with col3:
    st.metric("Último Sorteo", str(current_sorteo))
with col4:
    last_draw = df_draws.iloc[0]['Bolillas'] if not df_draws.empty else "N/A"
    st.metric("Última Jugada", last_draw)

st.markdown("---")

# SECTION 1: Time Series & Entropy Stability
st.subheader("1. Estabilidad del Sistema (Entropía Temporal)")
st.markdown("¿Está la máquina cambiando su comportamiento? Una entropía estable indica aleatoriedad pura. Caídas bruscas sugieren patrones temporales.")

entropy_df = analysis.get_rolling_entropy(df_exploded, window=50)
if not entropy_df.empty:
    fig_ent = px.line(
        entropy_df, 
        x='End_Sorteo', 
        y='Entropy',
        title="Evolución de la Entropía (Ventana Móvil 50 Sorteos)",
        labels={'End_Sorteo': 'Sorteo', 'Entropy': 'Entropía de Shannon'}
    )
    fig_ent.add_hline(y=3.91, line_dash="dash", annotation_text="Max Entropía (Azar Puro)")
    fig_ent.update_layout(height=400)
    st.plotly_chart(fig_ent, use_container_width=True)
else:
    st.info("Se necesitan más datos para calcular la entropía móvil.")

# SECTION 2: PRESION ESTADISTICA (GAP ANALYSIS) FIX
st.subheader("2. Mapa de Presión Estadística (Gap Analysis)")
col_gap_desc, col_gap_chart = st.columns([1, 3])

with col_gap_desc:
    st.markdown("""
    **Interpretación:**
    Este mapa busca anomalías.
    
    * **Eje X (Media)**: Frecuencia habitual.
    * **Eje Y (Lag Actual)**: Cuánto tiempo lleva sin salir.
    * **Burbuja Roja Grande**: Número con alto Z-Score (Estadísticamente "atrasado" y presionado a salir por reversión a la media).
    """)

with col_gap_chart:
    gaps_df = analysis.get_gap_metrics(df_exploded, current_sorteo)
    
    # Use 'Plot_Size' which guarantees positive values for bubble size
    fig_scatter = px.scatter(
        gaps_df, 
        x='Mean_Gap', 
        y='Current_Gap', 
        size='Plot_Size', # FIXED: Normalized column
        color='Z_Score',
        text='Numero',
        color_continuous_scale='RdYlGn_r', # Red = High Pressure
        title="Gap Map: Detección de Anomalías",
        hover_data=['Z_Score', 'Current_Gap', 'Mean_Gap']
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

# SECTION 3: PARITY & MARKOV
st.markdown("---")
col_parity, col_markov = st.columns(2)

with col_parity:
    st.subheader("3. Distribución de Paridad")
    parity_dist = analysis.get_parity_analysis(df_draws)
    fig_par = px.bar(
        x=parity_dist.index, 
        y=parity_dist.values,
        title="Frecuencia de Pares/Impares (%)",
        labels={'x': 'Combinación', 'y': 'Porcentaje'},
        color=parity_dist.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_par, use_container_width=True)

with col_markov:
    st.subheader("4. Cadenas de Markov (Suma)")
    markov = analysis.get_markov_matrix(df_draws)
    fig_mk = px.imshow(
        markov,
        text_auto=".1%",
        color_continuous_scale="Greens",
        title="Probabilidad de Transición de Estado (Suma)",
        labels={'x': 'El_siguiente_sorteo_será...', 'y': 'Si_el_sorteo_anterior_fue...'},
        aspect="auto"
    )
    st.plotly_chart(fig_mk, use_container_width=True)

# SECTION 4: CO-OCURRENCIA
st.subheader("5. Redes de Co-ocurrencia")
matrix = analysis.get_cooccurrence_matrix(df_draws)
import numpy as np
np.fill_diagonal(matrix.values, 0)

fig_heat = px.imshow(
    matrix,
    labels=dict(x="Bolilla A", y="Bolilla B", color="Frecuencia"),
    color_continuous_scale='Viridis',
    title="Heatmap: ¿Qué números salen juntos?"
)
fig_heat.update_layout(height=600)
st.plotly_chart(fig_heat, use_container_width=True)
