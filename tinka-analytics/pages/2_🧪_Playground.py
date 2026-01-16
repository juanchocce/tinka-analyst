import streamlit as st
import pandas as pd
import time
from modules import simulation

st.set_page_config(page_title="Monte Carlo Playground", page_icon="🧪")

# Load CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🧪 Laboratorio de Simulación (System Bets)")
st.markdown("""
A diferencia de la lotería convencional, aquí puedes probar **Jugadas Múltiples**. Selecciona hasta 15 números y el sistema calculará todas las combinaciones posibles contra 10,000 sorteos futuros.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Configura tu System Bet")
    # Updated to allow up to 15
    user_input = st.multiselect(
        "Elige tus números (6 - 15):",
        options=list(range(1, 51)),
        default=[13, 12, 26, 31, 28, 7], 
        max_selections=15
    )
    
    n_played = len(user_input)
    
    # Cost calculation display
    from scipy.special import comb
    n_combos = int(comb(n_played, 6)) if n_played >= 6 else 0
    total_cost = n_combos * 5
    
    st.info(f"""
    **Resumen de Jugada:**
    * Números: {n_played}
    * Combinaciones Generadas: {n_combos}
    * Costo Real (por Sorteo): S/ {total_cost:,.2f}
    """)
    
    run_btn = st.button("🎰 EJECUTAR SIMULACIÓN", use_container_width=True)

with col2:
    if run_btn:
        if n_played < 6:
            st.warning("Debes seleccionar al menos 6 números.")
        else:
            n_sims = 10000
            
            # Progress Bar for UX
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                time.sleep(0.005) 
                progress_bar.progress(i + 1)
                status_text.text(f"Simulando {n_sims} sorteos contra tus {n_combos} combinaciones...")
            
            start_time = time.time()
            # Run updated simulation
            results, roi, unique_matches, total_revenue = simulation.run_simulation(user_input, n_simulations=n_sims)
            elapsed = time.time() - start_time
            
            status_text.success(f"Simulación vectorizada completada en {elapsed:.2f} segundos.")
            
            # Results Display
            st.divider()
            
            # ROI Metric - Color coded
            cost_total_sim = total_cost * n_sims
            profit = total_revenue - cost_total_sim
            roi_color = "green" if profit > 0 else "red"
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Inversión Total", f"S/ {cost_total_sim:,.0f}")
            c2.metric("Retorno Total (Premios)", f"S/ {total_revenue:,.0f}")
            c3.markdown(f"### ROI: <span style='color:{roi_color}'>{roi:.2f}%</span>", unsafe_allow_html=True)
            
            st.caption("*Nota: El cálculo incluye premios cascada (ej. acertar 4 en una jugada de 8 paga múltiples premios de 3).*")
            
            # Histogram
            st.subheader("Frecuencia de Aciertos (Mejor Match por Sorteo)")
            res_df = pd.DataFrame.from_dict(results, orient='index', columns=['Cantidad'])
            res_df.index.name = 'Aciertos (Max)'
            st.bar_chart(res_df)
            
            if results.get(6, 0) > 0:
                st.balloons()
                st.success(f"¡FELICIDADES! Ganaste el POZO {results[6]} veces.")
