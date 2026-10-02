import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SYNCRET - Análisis Estructural", layout="wide")
st.title("🏗️️ SYNCRET: Calculadora Matricial de Armaduras 2D")
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

# Dibujar barras
for _, barra in barras_df.iterrows():
    try:
        n1 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
        n2 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Final"]].iloc[0]
        ax.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], 'b-', lw=2, zorder=1)
    except:
        pass # Ignora si hay un error de tipeo temporal del usuario

# Dibujar nodos y apoyos
ax.scatter(nodos_df["X (m)"], nodos_df["Y (m)"], c='red', s=100, zorder=2)
for _, nodo in nodos_df.iterrows():
    ax.annotate(str(int(nodo["Nodo"])), (nodo["X (m)"], nodo["Y (m)"]), 
                xytext=(5, 5), textcoords="offset points", fontsize=12, fontweight='bold')
    # Símbolos básicos de apoyo
    if nodo["Restringido_X"] or nodo["Restringido_Y"]:
        ax.scatter(nodo["X (m)"], nodo["Y (m)"]-0.2, c='green', marker='^', s=150, zorder=0)

ax.set_aspect('equal')
ax.grid(True, linestyle='--')
st.pyplot(fig)

# --- 3. MOTOR DE CÁLCULO (Método de Rigidez) ---
if st.button("Calcular Desplazamientos y Reacciones", type="primary"):
    try:
        # Pre-procesamiento de grados de libertad (GDL)
        n_nodos = len(nodos_df)
        n_gdl = 2 * n_nodos
        
        # Mapeo de nodos a índices
        nodo_idx = {int(row["Nodo"]): i for i, row in nodos_df.iterrows()}
        
        # Vector de fuerzas globales y GDL restringidos
        F = np.zeros(n_gdl)
        gdl_restringidos = []
        
        for i, row in nodos_df.iterrows():
            idx = nodo_idx[row["Nodo"]]
            F[2*idx] = row["Carga Fx (ton)"]
            F[2*idx + 1] = row["Carga Fy (ton)"]
            if row["Restringido_X"]: gdl_restringidos.append(2*idx)
            if row["Restringido_Y"]: gdl_restringidos.append(2*idx + 1)
            
        gdl_libres = [i for i in range(n_gdl) if i not in gdl_restringidos]
        
        # Ensamblaje de Matriz Global K
        K = np.zeros((n_gdl, n_gdl))
        for _, barra in barras_df.iterrows():
            idx1 = nodo_idx[barra["Nodo_Inicial"]]
            idx2 = nodo_idx[barra["Nodo_Final"]]
            
            n1 = nodos_df.iloc[idx1]
            n2 = nodos_df.iloc[idx2]
            
            dx = n2["X (m)"] - n1["X (m)"]
            dy = n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            c = dx / L
            s = dy / L
            
            # Matriz local
            k_val = (barra["Área (m2)"] * barra["E (ton/m2)"]) / L
            k_local = k_val * np.array([
                [ c**2,  c*s, -c**2, -c*s],
                [ c*s,   s**2, -c*s,  -s**2],
                [-c**2, -c*s,  c**2,  c*s],
                [-c*s,  -s**2,  c*s,   s**2]
            ])
            
            # Ensamblaje
            gdl = [2*idx1, 2*idx1+1, 2*idx2, 2*idx2+1]
            for i in range(4):
                for j in range(4):
                    K[gdl[i], gdl[j]] += k_local[i, j]
                    
        # Solución del sistema U = K^-1 * F (Solo en GDL libres)
        K_libres = K[np.ix_(gdl_libres, gdl_libres)]
        F_libres = F[gdl_libres]
        
        U_libres = np.linalg.solve(K_libres, F_libres)
        
        # Reconstruir vector de desplazamientos global
        U = np.zeros(n_gdl)
        U[gdl_libres] = U_libres
        
        # Calcular Reacciones
        R = np.dot(K, U)
        
        # Mostrar Resultados
        st.success("¡Cálculo exitoso!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Desplazamientos Nodales (m)**")
            desp_df = pd.DataFrame({
                "Nodo": nodos_df["Nodo"],
                "Dx": U[0::2],
                "Dy": U[1::2]
            })
            st.dataframe(desp_df, hide_index=True)
            
        with col2:
            st.write("**Reacciones en Apoyos (ton)**")
            reac_df = pd.DataFrame({
                "Nodo": nodos_df["Nodo"],
                "Rx": R[0::2],
                "Ry": R[1::2]
            })
            # Filtrar solo los nodos que tenían restricción
            reac_df = reac_df[(nodos_df["Restringido_X"]) | (nodos_df["Restringido_Y"])]
            st.dataframe(reac_df, hide_index=True)

    except Exception as e:
        st.error(f"Error en el cálculo. Verifica que la armadura sea estable y los datos correctos. Detalle: {e}")
