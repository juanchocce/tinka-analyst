import streamlit as st
import pandas as pd
import time
from modules import simulation

st.set_page_config(page_title="Monte Carlo Playground", page_icon="🧪")

# Load CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🧪 Laboratorio de Simulación")
st.markdown("""
Aquí es donde la teoría encuentra la realidad. Ingresa tu jugada y ejecutaremos **10,000 sorteos simulados** (equivalente a ~96 años de jugar 2 veces por semana) para ver tu rendimiento real.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Tu Estrategia")
    user_input = st.multiselect(
        "Elige 6 Números:",
        options=list(range(1, 51)),
        default=[13, 12, 26, 31, 28, 7], # Default based on "Hot" numbers from analysis
        max_selections=6
    )
    
    st.caption("Costo por jugada: S/ 5.00")
    
    run_btn = st.button("🎰 EJECUTAR SIMULACIÓN", use_container_width=True)

with col2:
    if run_btn:
        if len(user_input) != 6:
            st.warning("Por favor selecciona exactamente 6 números.")
        else:
            n_sims = 10000
            
            # Progress Bar Effect
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                time.sleep(0.005) # Fake crunching time for UX
                progress_bar.progress(i + 1)
                status_text.text(f"Simulando sorteo {int((i+1)/100 * n_sims)} de {n_sims}...")
            
            start_time = time.time()
            results, roi = simulation.run_simulation(user_input, n_simulations=n_sims)
            elapsed = time.time() - start_time
            
            status_text.success(f"Simulación completada en {elapsed:.2f} segundos.")
            
            # Display Results
            st.divider()
            
            # ROI Metric - Color coded
            roi_color = "red" if roi < 0 else "green"
            st.markdown(f"### ROI Esperado: <span style='color:{roi_color}'>{roi:.2f}%</span>", unsafe_allow_html=True)
            st.text(f"Inversión Total: S/ {n_sims * 5:,.2f} | Retorno Total: S/ {(n_sims * 5 * (1 + roi/100)):,.2f}")
            
            # Hits Breakdown
            st.subheader("Desglose de Aciertos")
            res_df = pd.DataFrame.from_dict(results, orient='index', columns=['Frecuencia'])
            res_df.index.name = 'Aciertos'
            
            # Chart
            st.bar_chart(res_df.loc[3:]) # Show only 3+ hits generally as 0-2 are useless
            
            st.dataframe(res_df.T)
            
            if results[6] > 0:
                st.balloons()
                st.success(f"¡INCREÍBLE! Ganaste el Pozo Millonario {results[6]} veces en {n_sims} intentos.")
            else:
                st.info("No ganaste el Pozo Millonario esta vez. Bienvenido a la estadística.")

    else:
        st.info("Define tus números y presiona Ejecutar.")
