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

# Top KPIs across columns
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

# SECTION 1: PRESION ESTADISTICA (GAP ANALYSIS)
st.subheader("1. Mapa de Presión Estadística (Gap Analysis)")
st.markdown("""
Este gráfico compara el **Retraso Actual** (eje Y) contra el **Retraso Promedio Histórico** (eje X).
* **Puntos Superiores (Z-Score Alto)**: Números que "deberían" salir pronto por reversión a la media.
* **Puntos Inferiores**: Números que han salido recientemente ("fríos").
""")

gaps_df = analysis.get_gap_metrics(df_exploded, current_sorteo)

fig_scatter = px.scatter(
    gaps_df, 
    x='Mean_Gap', 
    y='Current_Gap', 
    size='Z_Score', 
    color='Z_Score',
    text='Numero',
    color_continuous_scale='RdYlGn_r', # Red = High Pressure (High Z)
    title="Gap Map: ¿Qué números están 'retrasados'?",
    labels={'Mean_Gap': 'Ciclo Medio de Aparición', 'Current_Gap': 'Sorteos de Ausencia Actual'}
)
fig_scatter.update_traces(textposition='top center')
fig_scatter.update_layout(height=600)
st.plotly_chart(fig_scatter, use_container_width=True)

# SECTION 2: HEATMAP DE CO-OCURRENCIA
st.subheader("2. Matriz de Co-ocurrencia")
st.markdown("Identifica parejas de números que tienden a salir juntos más allá del azar.")

matrix = analysis.get_cooccurrence_matrix(df_draws)
# Mask diagonal for better visualization
import numpy as np
np.fill_diagonal(matrix.values, 0)

fig_heat = px.imshow(
    matrix,
    labels=dict(x="Bolilla A", y="Bolilla B", color="Frecuencia"),
    color_continuous_scale='Viridis',
    title="Heatmap de Relaciones entre Bolillas"
)
fig_heat.update_layout(height=700)
st.plotly_chart(fig_heat, use_container_width=True)

# SECTION 3: MARKOV CHAINS
st.subheader("3. Transición de Estados (Suma de Bolillas)")
st.markdown("Probabilidad de que el siguiente sorteo tenga una Suma Alta/Baja basado en el sorteo anterior.")

col_glass, col_trans = st.columns([1, 2])

with col_glass:
    st.info("""
    **Estados Definidos:**
    * **Bajo**: Suma < 130
    * **Medio**: 130 <= Suma < 170
    * **Alto**: Suma >= 170
    
    *La Tinka busca el equilibrio (Campana de Gauss).*
    """)

with col_trans:
    markov = analysis.get_markov_matrix(df_draws)
    fig_mk = px.imshow(
        markov,
        text_auto=".1%",
        color_continuous_scale="Blues",
        title="Matriz de Probabilidad de Transición"
    )
    st.plotly_chart(fig_mk, use_container_width=True)
