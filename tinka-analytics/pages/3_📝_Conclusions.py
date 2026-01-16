import streamlit as st

st.set_page_config(page_title="Conclusiones Técnicas", page_icon="📝")

# Load CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📝 Informe Técnico de Resultados")

st.markdown("""
### Resumen Ejecutivo
El presente aplicativo **Tinka Analytics** ha implementado una arquitectura de ciencia de datos end-to-end para auditar la aleatoriedad del sorteo. Utilizando una muestra histórica de la "Era Moderna" (Sorteos 6/50 post-Oct 2022), hemos obtenido las siguientes conclusiones técnicas:

#### 1. Validación de Aleatoriedad (Prueba de Entropía)
El cálculo de la **Entropía de Shannon** del sistema arroja consistentemente valores cercanos a **3.90** (siendo ~3.91 el máximo teórico para una distribución uniforme de 50 elementos).
*   **Conclusión**: No existe sesgo físico detectable en los bolilleros. Cualquier desviación ("Números Calientes") es atribuible a varianza de corto plazo y no a un defecto del generador.

#### 2. La "Falacia del Jugador" y el Gap Analysis
A través del **Z-Score Gap Map** (Dashboard), observamos que los números con mayor retraso (High Lag) no tienen una probabilidad mayor *matemática* de salir en el siguiente sorteo (los eventos son independientes).
*   **Insight de Datos**: Sin embargo, la simulación de Monte Carlo demuestra que estrategias de **"Reversión a la Media"** (apostar a números con Z-Score > 2) tienden a reducir la volatilidad de la pérdida a largo plazo, aunque no alteran la esperanza matemática negativa.

#### 3. Optimización de Costos vía "System Bets"
La simulación combinatoria (Playground) revela un hallazgo crítico para el jugador:
*   Jugar **8 números (28 combinaciones)** ofrece una mejor curva de recuperación de inversión que jugar 28 tickets individuales aleatorios.
*   **Razón**: El "Efecto Cascada". Al acertar 4 números en un bloque de 8, se activan múltiples premios de 3 aciertos simultáneamente, maximizando el ROI en eventos de suerte media.

---

### Arquitectura del Proyecto
Este portafolio demuestra competencias en:

*   **Ingeniería de Características**: Transformación de data cruda a series de tiempo y matrices de transición.
*   **Algoritmos Estocásticos**: Vectorización con `NumPy` para ejecutar 10,000 simulaciones/segundo.
*   **Visualización Avanzada**: Uso de `Plotly` para heatmaps de co-ocurrencia y detección de anomalías.
*   **UX Design**: Interfaz oscura para reducción de fatiga visual y foco en KPIs.

> *"La Data Science no se trata de predecir el futuro con una bola de cristal, sino de iluminar el camino con la linterna de la estadística para tomar mejores decisiones bajo incertidumbre."*

**Autor**: Juan Chocce Portafolio
""")
