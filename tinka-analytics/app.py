import streamlit as st

st.set_page_config(
    page_title="Tinka Analytics",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar Context
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
st.sidebar.markdown("""
### Tinka Analytics
**Version:** 1.0.0
**Author:** Juan (Senior Data Scientist)
**Stack:** Python, Streamlit, Pandas, NumPy, Scipy
""")

# Hero Section
st.title("Tinka Analytics: Decidindo el Azar")
st.markdown("""
### ¿Es posible ganar a la casa usando Matemáticas?
Bienvenido. Esta aplicación no es un simple generador de números aleatorios. Es un demostrador de capacidad técnica que aplica **Inferencia Estadística**, **Cadenas de Markov** y **Simulación de Monte Carlo** para analizar el comportamiento histórico de la lotería peruana "La Tinka".

#### Módulos de la Aplicación:
1.  **📊 Dashboard Científico**: Visualiza patrones ocultos, análisis de gaps y entropía del sistema.
2.  **🧪 Monte Carlo Playground**: Pon a prueba tu "Jugada Maestra" contra 10,000 sorteos simulados en tiempo real.
3.  **📝 Conclusiones Éticas**: Interpretación honesta sobre las limitaciones del modelado predictivo en juegos de azar independientes.

---
> * "Dios no juega a los dados con el universo... pero la Tinka sí." *
""")

st.info("👈 Selecciona un módulo en la barra lateral para comenzar.")
