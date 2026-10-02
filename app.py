import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SYNCRET - Análisis Estructural", layout="wide")
st.title("🏗 SYNCRET: Calculadora Matricial de Armaduras 2D")
st.markdown("**Desarrollado por: Nilo Jara**")

# --- 1. ENTRADA DE DATOS (Tablas Interactivas) ---
st.subheader("1. Coordenadas de Nodos, Cargas y Apoyos")
st.write("Agrega los nodos. Marca las casillas 'Restringido' si hay un apoyo en esa dirección.")
nodos_default = pd.DataFrame({
    "Nodo": [1, 2, 3],
    "X (m)": [0.0, 4.0, 2.0],
    "Y (m)": [0.0, 0.0, 3.0],
    "Carga Fx (ton)": [0.0, 0.0, 5.0],
    "Carga Fy (ton)": [0.0, 0.0, -10.0],
    "Restringido_X": [True, False, False],
    "Restringido_Y": [True, True, False]
})
nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos")

st.subheader("2. Conectividad de Barras (Elementos)")
st.write("Conecta los nodos e ingresa las propiedades (Área en m², Módulo E en ton/m²).")
barras_default = pd.DataFrame({
    "Barra": [1, 2, 3],
    "Nodo_Inicial": [1, 2, 1],
    "Nodo_Final": [2, 3, 3],
    "Área (m2)": [0.01, 0.01, 0.01],
    "E (ton/m2)": [2e7, 2e7, 2e7]
})
barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras")

# --- 2. VISUALIZACIÓN GRÁFICA ---
st.subheader("Vista de la Estructura")
fig, ax = plt.subplots(figsize=(8, 4))

# Dibujar barras (con protección de errores)
for _, barra in barras_df.iterrows():
    try:
        n1 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
        n2 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Final"]].iloc[0]
        ax.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], 'b-', lw=2, zorder=1)
    except:
        pass # Ignora si hay un error temporal por celdas vacías

# Dibujar nodos y apoyos (con protección de errores)
for _, nodo in nodos_df.iterrows():
    try:
        ax.scatter(nodo["X (m)"], nodo["Y (m)"], c='red', s=100, zorder=2)
        ax.annotate(str(int(nodo["Nodo"])), (nodo["X (m)"], nodo["Y (m)"]), 
                    xytext=(5, 5), textcoords="offset points", fontsize=12, fontweight='bold')
        if nodo["Restringido_X"] or nodo["Restringido_Y"]:
            ax.scatter(nodo["X (m)"], nodo["Y (m)"]-0.2, c='green', marker='^', s=150, zorder=0)
    except:
        pass # Ignora si el número de nodo está vacío

ax.set_aspect('equal')
ax.grid(True, linestyle='--')
st.pyplot(fig)

# --- 3. MOTOR DE CÁLCULO (Método de Rigidez) ---
if st.button("Calcular Desplazamientos y Reacciones", type="primary"):
    try:
        # Limpiar datos vacíos antes de calcular
        nodos_clean = nodos_df.dropna(subset=["Nodo", "X (m)", "Y (m)"])
        barras_clean = barras_df.dropna(subset=["Nodo_Inicial", "Nodo_Final"])
        
        n_nodos = len(nodos_clean)
        n_gdl = 2 * n_nodos
        
        nodo_idx = {int(row["Nodo"]): i for i, row in nodos_clean.iterrows()}
        F = np.zeros(n_gdl)
        gdl_restringidos = []
        
        for i, row in nodos_clean.iterrows():
            idx = nodo_idx[row["Nodo"]]
            F[2*idx] = float(row["Carga Fx (ton)"]) if not pd.isna(row["Carga Fx (ton)"]) else 0.0
            F[2*idx + 1] = float(row["Carga Fy (ton)"]) if not pd.isna(row["Carga Fy (ton)"]) else 0.0
            if row["Restringido_X"]: gdl_restringidos.append(2*idx)
            if row["Restringido_Y"]: gdl_restringidos.append(2*idx + 1)
            
        gdl_libres = [i for i in range(n_gdl) if i not in gdl_restringidos]
        
        K = np.zeros((n_gdl, n_gdl))
        for _, barra in barras_clean.iterrows():
            idx1 = nodo_idx[int(barra["Nodo_Inicial"])]
            idx2 = nodo_idx[int(barra["Nodo_Final"])]
            n1 = nodos_clean.iloc[idx1]
            n2 = nodos_clean.iloc[idx2]
            dx = n2["X (m)"] - n1["X (m)"]
            dy = n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            c = dx / L
            s = dy / L
            k_val = (barra["Área (m2)"] * barra["E (ton/m2)"]) / L
            k_local = k_val * np.array([
                [ c**2,  c*s, -c**2, -c*s],
                [ c*s,   s**2, -c*s,  -s**2],
                [-c**2, -c*s,  c**2,  c*s],
                [-c*s,  -s**2,  c*s,   s**2]
            ])
            gdl = [2*idx1, 2*idx1+1, 2*idx2, 2*idx2+1]
            for i in range(4):
                for j in range(4):
                    K[gdl[i], gdl[j]] += k_local[i, j]
                    
        K_libres = K[np.ix_(gdl_libres, gdl_libres)]
        F_libres = F[gdl_libres]
        U_libres = np.linalg.solve(K_libres, F_libres)
        
        U = np.zeros(n_gdl)
        U[gdl_libres] = U_libres
        R = np.dot(K, U)
        
        st.success("¡Cálculo exitoso!")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Desplazamientos Nodales (m)**")
            desp_df = pd.DataFrame({
                "Nodo": nodos_clean["Nodo"].astype(int),
                "Dx": [f"{x:.3e}" for x in U[0::2]],
                "Dy": [f"{x:.3e}" for x in U[1::2]]
            })
            st.dataframe(desp_df, hide_index=True)
            
        with col2:
            st.write("**Reacciones en Apoyos (ton)**")
            reac_df = pd.DataFrame({
                "Nodo": nodos_clean["Nodo"].astype(int),
                "Rx": np.round(R[0::2], 3),
                "Ry": np.round(R[1::2], 3)
            })
            reac_df = reac_df[(nodos_clean["Restringido_X"].values) | (nodos_clean["Restringido_Y"].values)]
            st.dataframe(reac_df, hide_index=True)

    except Exception as e:
        st.error(f"Error en el cálculo. Verifica los datos ingresados. Detalle: {e}")
