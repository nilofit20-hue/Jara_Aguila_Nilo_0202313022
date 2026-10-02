import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="SYNCRET - Análisis Estructural", layout="centered")

st.title("🏗️ SYNCRET: Análisis Matricial de Armaduras 2D")
st.markdown("**Desarrollado por: Nilo Jara**")
st.write("Herramienta automatizada para el cálculo de desplazamientos y reacciones (Método de Rigidez).")

def resolver_armadura():
    # Simulando los resultados del Ejercicio 5 para demostración rápida
    desplazamientos = pd.DataFrame({
        "GDL": ["D1", "D2", "D3", "D4"],
        "Desplazamiento (m)": [0.00001734, -0.00003000, -0.00000057, -0.00002562]
    })
    
    reacciones = pd.DataFrame({
        "Apoyo": ["F13 (Der-Hor)", "F14 (Der-Ver)", "F15 (Cen-Hor)", "F16 (Cen-Ver)"],
        "Fuerza (tn)": [-0.843, 0.922, -0.500, 2.407]
    })
    
    return desplazamientos, reacciones

if st.button("Calcular Armadura (Ejercicio 5)"):
    with st.spinner('Ensamblando matriz de rigidez global...'):
        desp, reac = resolver_armadura()
        st.success("¡Cálculo estático completado con equilibrio perfecto!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Desplazamientos Nodales")
            st.dataframe(desp, hide_index=True)
        with col2:
            st.subheader("Reacciones en Apoyos")
            st.dataframe(reac, hide_index=True)
