import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Configuración inicial
st.set_page_config(page_title="SYNCRET - Análisis Estructural", page_icon="🏗️", layout="wide")

# --- DISEÑO VISUAL Y COLORES ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom right, #0e1117, #1a202c); }
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; font-size: 22px; font-weight: bold;
        padding: 15px 30px; border-radius: 12px; border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s ease; width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff3333; transform: translateY(-3px); box-shadow: 0 8px 15px rgba(255, 75, 75, 0.4);
    }
    h1, h2, h3 { color: #4B90FF !important; }
</style>
""", unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3204/3204094.png", width=100)
    st.header("📖 ¿Cómo usar SYNCRET?")
    st.info("Sigue estos pasos para analizar cualquier armadura:")
    with st.expander("Paso 1: Nodos y Apoyos"):
        st.write("Define coordenadas (X, Y) y cargas. Marca 'Restringido' si hay un apoyo.")
    with st.expander("Paso 2: Barras"):
        st.write("Une los nodos indicando Área (m²) y Elasticidad E (ton/m²).")
    with st.expander("Paso 3: Calcular"):
        st.write("Presiona el botón para generar las matrices, fuerzas axiales y gráficos de esfuerzos.")
    st.markdown("---")
    st.markdown("**Proyecto Universitario**\n\nDesarrollado por: *Nilo Jara*")

# --- TÍTULO PRINCIPAL ---
st.title("🏗 SYNCRET: Calculadora Matricial Integral")
st.markdown("*Análisis por Rigidez Directa: Desplazamientos, Reacciones y Esfuerzos Internos*")
st.markdown("---")

# --- 1. ENTRADA DE DATOS ---
col_nodos, col_barras = st.columns(2)

with col_nodos:
    st.subheader("📍 1. Coordenadas y Cargas")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4], 
        "X (m)": [0.0, 4.0, 0.0, 4.0], 
        "Y (m)": [0.0, 0.0, 3.0, 3.0],
        "Carga Fx (ton)": [0.0, 0.0, 2.0, 0.0], 
        "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0],
        "Restringido_X": [True, False, False, False], 
        "Restringido_Y": [True, True, False, False]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos", use_container_width=True)

with col_barras:
    st.subheader("🔗 2. Conectividad de Barras")
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3, 4, 5, 6], 
        "Nodo_Inicial": [1, 2, 3, 1, 1, 2], 
        "Nodo_Final": [2, 4, 4, 3, 4, 3],
        "Área (m2)": [0.01, 0.01, 0.01, 0.01, 0.01, 0.01], 
        "E (ton/m2)": [2e7, 2e7, 2e7, 2e7, 2e7, 2e7]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras", use_container_width=True)

# --- 2. VISTA PREVIA ---
st.subheader("👁️ Vista Previa de la Estructura")
fig, ax = plt.subplots(figsize=(10, 3))
fig.patch.set_facecolor('#f0f2f6')
ax.set_facecolor('#ffffff')

for _, barra in barras_df.iterrows():
    try:
        n1 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
        n2 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Final"]].iloc[0]
        ax.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], color='#2c3e50', lw=2, zorder=1)
    except: pass 

for _, nodo in nodos_df.iterrows():
    try:
        ax.scatter(nodo["X (m)"], nodo["Y (m)"], c='#34495e', s=100, zorder=2)
        ax.annotate(str(int(nodo["Nodo"])), (nodo["X (m)"], nodo["Y (m)"]), xytext=(8, 8), textcoords="offset points", fontsize=12, fontweight='bold')
        if nodo["Restringido_X"] or nodo["Restringido_Y"]:
            ax.scatter(nodo["X (m)"], nodo["Y (m)"]-0.2, c='#2ecc71', marker='^', s=150, zorder=0)
    except: pass 

ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)
st.markdown("---")

# --- 3. MOTOR MATRICIAL ---
if st.button("🚀 INICIAR CÁLCULO MATRICIAL"):
    try:
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
        
        fuerzas_axiales = []
        estados = []
        for _, barra in barras_clean.iterrows():
            idx1 = nodo_idx[int(barra["Nodo_Inicial"])]
            idx2 = nodo_idx[int(barra["Nodo_Final"])]
            n1, n2 = nodos_clean.iloc[idx1], nodos_clean.iloc[idx2]
            dx = n2["X (m)"] - n1["X (m)"]
            dy = n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            c, s = dx / L, dy / L
            
            u1, u2 = U[2*idx1], U[2*idx1+1]
            u3, u4 = U[2*idx2], U[2*idx2+1]
            
            dL = c*(u3 - u1) + s*(u4 - u2)
            N = (barra["Área (m2)"] * barra["E (ton/m2)"] / L) * dL
            N = np.round(N, 4) 
            
            fuerzas_axiales.append(N)
            if N > 0: estados.append("Tracción")
            elif N < 0: estados.append("Compresión")
            else: estados.append("Nulo")

        # --- MOSTRAR RESULTADOS ---
        st.balloons()
        st.success("✅ ¡Sistema resuelto con éxito! Explora los resultados en las pestañas inferiores.")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📉 Desplazamientos y Reacciones", "🧮 Matriz de Rigidez (K)", "🔗 Fuerzas Axiales", "🎨 Gráfico de Esfuerzos"])
        
        with tab1:
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.write("**Desplazamientos Nodales (m)**")
                desp_df = pd.DataFrame({
                    "Nodo": nodos_clean["Nodo"].astype(int),
                    "Dx": [f"{x:.6f}" for x in U[0::2]],
                    "Dy": [f"{x:.6f}" for x in U[1::2]]
                })
                st.dataframe(desp_df, hide_index=True, use_container_width=True)
            with res_col2:
                st.write("**Reacciones en Apoyos (ton)**")
                reac_df = pd.DataFrame({
                    "Nodo": nodos_clean["Nodo"].astype(int),
                    "Rx": np.round(R[0::2], 3),
                    "Ry": np.round(R[1::2], 3)
                })
                reac_df = reac_df[(nodos_clean["Restringido_X"].values) | (nodos_clean["Restringido_Y"].values)]
                st.dataframe(reac_df, hide_index=True, use_container_width=True)

        with tab2:
            st.write("**Matriz de Rigidez Global del Sistema (K)**")
            gdl_labels = [f"N{int(n)}-{e}" for n in nodos_clean["Nodo"] for e in ['X', 'Y']]
            K_df = pd.DataFrame(K, columns=gdl_labels, index=gdl_labels)
            # Modificado para mostrar decimales normales
            st.dataframe(K_df.style.format("{:.2f}"), use_container_width=True)

        with tab3:
            st.write("**Fuerzas Internas en los Elementos**")
            fuerzas_df = pd.DataFrame({
                "Barra": barras_clean["Barra"].astype(int),
                "Nodo Inicial": barras_clean["Nodo_Inicial"].astype(int),
                "Nodo Final": barras_clean["Nodo_Final"].astype(int),
                "Fuerza Axial (ton)": fuerzas_axiales,
                "Estado": estados
            })
            st.dataframe(fuerzas_df, hide_index=True, use_container_width=True)

        with tab4:
            st.write("**Estado de los Elementos y Reacciones**")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            fig2.patch.set_facecolor('#f0f2f6')
            ax2.set_facecolor('#ffffff')
            
            # Dibujar barras y etiquetas (T)/(C) con "Tn"
            for idx, barra in barras_clean.iterrows():
                n1 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
                n2 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Final"]].iloc[0]
                x_coords = [n1["X (m)"], n2["X (m)"]]
                y_coords = [n1["Y (m)"], n2["Y (m)"]]
                
                N = fuerzas_axiales[idx]
                if N > 0: 
                    color = '#3498db'
                    etiqueta = f"{abs(N):.2f} Tn (T)"
                elif N < 0: 
                    color = '#e74c3c'
                    etiqueta = f"{abs(N):.2f} Tn (C)"
                else: 
                    color = '#95a5a6'
                    etiqueta = "0.00 Tn"
                    
                ax2.plot(x_coords, y_coords, color=color, lw=4, zorder=1)
                mid_x, mid_y = np.mean(x_coords), np.mean(y_coords)
                ax2.text(mid_x, mid_y, etiqueta, color='black', fontsize=10, 
                         ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

            # Dibujar nodos encima
            ax2.scatter(nodos_clean["X (m)"], nodos_clean["Y (m)"], c='black', s=50, zorder=2)

            # Dibujar flechas de Reacciones (Morado)
            for idx, row in nodos_clean.iterrows():
                n_idx = nodo_idx[int(row["Nodo"])]
                rx = R[2*n_idx]
                ry = R[2*n_idx+1]
                x, y = row["X (m)"], row["Y (m)"]
                
                if abs(rx) > 0.001:
                    sentido = 1 if rx > 0 else -1
                    start_x = x - sentido * 0.8
                    ax2.annotate(f"{abs(rx):.2f} Tn", xy=(x, y), xytext=(start_x, y),
                                 arrowprops=dict(facecolor='#8e44ad', edgecolor='#8e44ad', width=2, headwidth=8),
                                 fontsize=10, color='#8e44ad', fontweight='bold', ha='center', va='bottom', zorder=4)
                
                if abs(ry) > 0.001:
                    sentido = 1 if ry > 0 else -1
                    start_y = y - sentido * 0.8
                    ax2.annotate(f"{abs(ry):.2f} Tn", xy=(x, y), xytext=(x, start_y),
                                 arrowprops=dict(facecolor='#8e44ad', edgecolor='#8e44ad', width=2, headwidth=8),
                                 fontsize=10, color='#8e44ad', fontweight='bold', ha='left', va='center', zorder=4)
            
            # Leyenda actualizada
            blue_patch = mpatches.Patch(color='#3498db', label='Tracción (+)')
            red_patch = mpatches.Patch(color='#e74c3c', label='Compresión (-)')
            gray_patch = mpatches.Patch(color='#95a5a6', label='Nulo (0)')
            purple_patch = mpatches.Patch(color='#8e44ad', label='Reacciones')
            ax2.legend(handles=[blue_patch, red_patch, gray_patch, purple_patch], loc='upper right')

            # Expandir los límites de la gráfica para que quepan las flechas
            min_x, max_x = nodos_clean["X (m)"].min(), nodos_clean["X (m)"].max()
            min_y, max_y = nodos_clean["Y (m)"].min(), nodos_clean["Y (m)"].max()
            margen = max((max_x - min_x)*0.25, (max_y - min_y)*0.25, 1.0)
            ax2.set_xlim(min_x - margen, max_x + margen)
            ax2.set_ylim(min_y - margen, max_y + margen)
            
            ax2.set_aspect('equal')
            ax2.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ Error matemático. Verifica los datos ingresados. Detalle técnico: {e}")
