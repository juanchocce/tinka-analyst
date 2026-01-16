import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon="📝")

# Load CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📝 Data Storytelling & Ética")

st.markdown("""
### La Verdad Incomoda de la Probabilidad
Tras analizar miles de sorteos y ejecutar millones de simulaciones, la conclusión científica es clara: **La Tinka es un sistema robustamente aleatorio.**

Sin embargo, como Data Scientist, hemos observado fenómenos interesantes:
1.  **Reversión a la Media**: Los números "fríos" eventualmente despiertan.
2.  **Agrupamientos Temporales**: Ciertos pares muestran adhesión en ventanas cortas de tiempo.
3.  **Ineficiencia Humana**: La mayoría de jugadores eligen fechas (1-31), dejando el rango 32-50 menos poblado. *Jugar en este rango no aumenta tu probabilidad de ganar, pero sí reduce la probabilidad de compartir el pozo si ganas.*

#### Reflexión Profesional
Este proyecto demuestra habilidades en:
*   **Ingeniería de Datos**: ETL y limpieza de ruido.
*   **Inferencia Bayesiana y Frecuentista**: Entender distribuciones.
*   **Computación Numérica**: Optimización vectorial para simulaciones masivas.
*   **Desarrollo Fullstack**: Creación de herramientas interactivas orientadas al usuario.

> *"La lotería es un impuesto voluntario a la esperanza, pero entender la matemática detrás nos permite pagar ese impuesto con los ojos abiertos."*

**Contacto:**
*   [LinkedIn](https://linkedin.com)
*   [GitHub](https://github.com)
""")
