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

# --- PANEL LATERAL (SELECTOR DE MODO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3204/3204094.png", width=100)
    st.header("⚙️ Configuración")
    
    # Selector clave entre 2D y 3D
    modo_analisis = st.radio("Selecciona el Tipo de Análisis:", ["Estructura 2D (Plana)", "Estructura 3D (Espacial)"])
    
    st.markdown("---")
    st.header("📖 Guía Rápida")
    if "2D" in modo_analisis:
        st.info("Modo 2D activo: Analiza armaduras en el plano XY con 2 GDL por nodo.")
    else:
        st.info("Modo 3D activo: Analiza armaduras espaciales en el plano XYZ con 3 GDL por nodo.")
    
    st.markdown("---")
    st.markdown("**Proyecto Universitario**\n\nDesarrollado por: *Nilo Jara*")

# --- TÍTULO PRINCIPAL ---
st.title(f"🏗 SYNCRET: Calculadora Matricial ({modo_analisis})")
st.markdown("*Análisis Estructural Automatizado por Rigidez Directa*")
st.markdown("---")

# --- 1. ENTRADA DE DATOS SEGÚN EL MODO ---
col_nodos, col_barras = st.columns(2)

if "2D" in modo_analisis:
    with col_nodos:
        st.subheader("📍 1. Coordenadas y Cargas (2D)")
        nodos_default = pd.DataFrame({
            "Nodo": [1, 2, 3, 4], 
            "X (m)": [0.0, 4.0, 0.0, 4.0], 
            "Y (m)": [0.0, 0.0, 3.0, 3.0],
            "Carga Fx (ton)": [0.0, 0.0, 2.0, 0.0], 
            "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0],
            "Restringido_X": [True, False, False, False], 
            "Restringido_Y": [True, True, False, False]
        })
        nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_2d", use_container_width=True)

    with col_barras:
        st.subheader("🔗 2. Conectividad de Barras (2D)")
        barras_default = pd.DataFrame({
            "Barra": [1, 2, 3, 4, 5, 6], 
            "Nodo_Inicial": [1, 2, 3, 1, 1, 2], 
            "Nodo_Final": [2, 4, 4, 3, 4, 3],
            "Área (m2)": [0.01, 0.01, 0.01, 0.01, 0.01, 0.01], 
            "E (ton/m2)": [2e7, 2e7, 2e7, 2e7, 2e7, 2e7]
        })
        barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_2d", use_container_width=True)
else:
    with col_nodos:
        st.subheader("📍 1. Coordenadas y Cargas (3D)")
        nodos_default = pd.DataFrame({
            "Nodo": [1, 2, 3, 4], 
            "X (m)": [0.0, 2.0, 2.0, 0.0], 
            "Y (m)": [0.0, 0.0, 2.0, 2.0],
            "Z (m)": [0.0, 0.0, 0.0, 3.0],
            "Carga Fx (ton)": [0.0, 0.0, 0.0, 5.0], 
            "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0],
            "Carga Fz (ton)": [0.0, 0.0, 0.0, -10.0],
            "Restringido_X": [True, True, True, False], 
            "Restringido_Y": [True, True, True, False],
            "Restringido_Z": [True, True, True, False]
        })
        nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_3d", use_container_width=True)

    with col_barras:
        st.subheader("🔗 2. Conectividad de Barras (3D)")
        barras_default = pd.DataFrame({
            "Barra": [1, 2, 3, 4], 
            "Nodo_Inicial": [1, 2, 3, 4], 
            "Nodo_Final": [4, 4, 4, 4],
            "Área (m2)": [0.01, 0.01, 0.01, 0.01], 
            "E (ton/m2)": [2e7, 2e7, 2e7, 2e7]
        })
        barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_3d", use_container_width=True)

# --- 2. VISTA PREVIA ---
st.subheader("👁️ Vista Previa de la Estructura")
if "2D" in modo_analisis:
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
else:
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(projection='3d')
    fig.patch.set_facecolor('#f0f2f6')
    for _, barra in barras_df.iterrows():
        try:
            n1 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
            n2 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Final"]].iloc[0]
            ax.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], [n1["Z (m)"], n2["Z (m)"]], color='#2c3e50', lw=2)
        except: pass 
    try:
        ax.scatter(nodos_df["X (m)"], nodos_df["Y (m)"], nodos_df["Z (m)"], c='#FF4B4B', s=100)
        for _, nodo in nodos_df.iterrows():
            ax.text(nodo["X (m)"], nodo["Y (m)"], nodo["Z (m)"], f" N{int(nodo['Nodo'])}", fontsize=10, fontweight='bold')
    except: pass
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    st.pyplot(fig)

st.markdown("---")

# --- 3. MOTOR MATRICIAL ---
if st.button("🚀 INICIAR CÁLCULO MATRICIAL"):
    try:
        if "2D" in modo_analisis:
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
                n1, n2 = nodos_clean.iloc[idx1], nodos_clean.iloc[idx2]
                dx, dy = n2["X (m)"] - n1["X (m)"], n2["Y (m)"] - n1["Y (m)"]
                L = np.sqrt(dx**2 + dy**2)
                c, s = dx / L, dy / L
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
                dx, dy = n2["X (m)"] - n1["X (m)"], n2["Y (m)"] - n1["Y (m)"]
                L = np.sqrt(dx**2 + dy**2)
                c, s = dx / L, dy / L
                u1, u2 = U[2*idx1], U[2*idx1+1]
                u3, u4 = U[2*idx2], U[2*idx2+1]
                dL = c*(u3 - u1) + s*(u4 - u2)
                N = np.round((barra["Área (m2)"] * barra["E (ton/m2)"] / L) * dL, 4)
                fuerzas_axiales.append(N)
                estados.append("Tracción" if N > 0 else ("Compresión" if N < 0 else "Nulo"))

            st.balloons()
            st.success("✅ ¡Estructura 2D resuelta con éxito!")
            tab1, tab2, tab3, tab4 = st.tabs(["📉 Desplazamientos y Reacciones", "🧮 Matriz de Rigidez (K)", "🔗 Fuerzas Axiales", "🎨 Gráfico de Esfuerzos"])
            
            with tab1:
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.write("**Desplazamientos Nodales 2D (m)**")
                    desp_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Dx": [f"{x:.6f}" for x in U[0::2]], "Dy": [f"{x:.6f}" for x in U[1::2]]})
                    st.dataframe(desp_df, hide_index=True, use_container_width=True)
                with res_col2:
                    st.write("**Reacciones en Apoyos 2D (ton)**")
                    reac_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Rx": np.round(R[0::2], 3), "Ry": np.round(R[1::2], 3)})
                    reac_df = reac_df[(nodos_clean["Restringido_X"].values) | (nodos_clean["Restringido_Y"].values)]
                    st.dataframe(reac_df, hide_index=True, use_container_width=True)

            with tab2:
                st.write("**Matriz de Rigidez Global 2D (K)**")
                gdl_labels = [f"N{int(n)}-{e}" for n in nodos_clean["Nodo"] for e in ['X', 'Y']]
                K_df = pd.DataFrame(K, columns=gdl_labels, index=gdl_labels)
                st.dataframe(K_df.style.format("{:.2f}"), use_container_width=True)

            with tab3:
                st.write("**Fuerzas Internas en los Elementos**")
                fuerzas_df = pd.DataFrame({"Barra": barras_clean["Barra"].astype(int), "Nodo Inicial": barras_clean["Nodo_Inicial"].astype(int), "Nodo Final": barras_clean["Nodo_Final"].astype(int), "Fuerza Axial (ton)": fuerzas_axiales, "Estado": estados})
                st.dataframe(fuerzas_df, hide_index=True, use_container_width=True)

            with tab4:
                st.write("**Gráfico de Esfuerzos y Reacciones (2D)**")
                fig2, ax2 = plt.subplots(figsize=(10, 5))
                fig2.patch.set_facecolor('#f0f2f6')
                ax2.set_facecolor('#ffffff')
                for idx, barra in barras_clean.iterrows():
                    n1 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
                    n2 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Final"]].iloc[0]
                    N = fuerzas_axiales[idx]
                    color = '#3498db' if N > 0 else ('#e74c3c' if N < 0 else '#95a5a6')
                    etiqueta = f"{abs(N):.2f} Tn (T)" if N > 0 else (f"{abs(N):.2f} Tn (C)" if N < 0 else "0.00 Tn")
                    ax2.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], color=color, lw=4, zorder=1)
                    ax2.text(np.mean([n1["X (m)"], n2["X (m)"]]), np.mean([n1["Y (m)"], n2["Y (m)"]]), etiqueta, color='black', fontsize=10, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
                ax2.scatter(nodos_clean["X (m)"], nodos_clean["Y (m)"], c='black', s=50, zorder=2)
                
                for idx, row in nodos_clean.iterrows():
                    n_idx = nodo_idx[int(row["Nodo"])]
                    rx, ry, x, y = R[2*n_idx], R[2*n_idx+1], row["X (m)"], row["Y (m)"]
                    if abs(rx) > 0.001:
                        ax2.annotate(f"{abs(rx):.2f} Tn", xy=(x, y), xytext=(x - (1 if rx > 0 else -1)*0.8, y), arrowprops=dict(facecolor='#8e44ad', edgecolor='#8e44ad', width=2, headwidth=8), fontsize=10, color='#8e44ad', fontweight='bold', ha='center', va='bottom', zorder=4)
                    if abs(ry) > 0.001:
                        ax2.annotate(f"{abs(ry):.2f} Tn", xy=(x, y), xytext=(x, y - (1 if ry > 0 else -1)*0.8), arrowprops=dict(facecolor='#8e44ad', edgecolor='#8e44ad', width=2, headwidth=8), fontsize=10, color='#8e44ad', fontweight='bold', ha='left', va='center', zorder=4)

                blue_patch, red_patch, gray_patch, purple_patch = mpatches.Patch(color='#3498db', label='Tracción (+)'), mpatches.Patch(color='#e74c3c', label='Compresión (-)'), mpatches.Patch(color='#95a5a6', label='Nulo (0)'), mpatches.Patch(color='#8e44ad', label='Reacciones')
                ax2.legend(handles=[blue_patch, red_patch, gray_patch, purple_patch], loc='upper right')
                min_x, max_x = nodos_clean["X (m)"].min(), nodos_clean["X (m)"].max()
                min_y, max_y = nodos_clean["Y (m)"].min(), nodos_clean["Y (m)"].max()
                margen = max((max_x - min_x)*0.25, (max_y - min_y)*0.25, 1.0)
                ax2.set_xlim(min_x - margen, max_x + margen)
                ax2.set_ylim(min_y - margen, max_y + margen)
                ax2.set_aspect('equal')
                ax2.grid(True, linestyle='--', alpha=0.5)
                st.pyplot(fig2)

        else: # MODO 3D
            nodos_clean = nodos_df.dropna(subset=["Nodo", "X (m)", "Y (m)", "Z (m)"])
            barras_clean = barras_df.dropna(subset=["Nodo_Inicial", "Nodo_Final"])
            n_nodos = len(nodos_clean)
            n_gdl = 3 * n_nodos
            
            nodo_idx = {int(row["Nodo"]): i for i, row in nodos_clean.iterrows()}
            F = np.zeros(n_gdl)
            gdl_restringidos = []
            
            for i, row in nodos_clean.iterrows():
                idx = nodo_idx[row["Nodo"]]
                F[3*idx]     = float(row["Carga Fx (ton)"]) if not pd.isna(row["Carga Fx (ton)"]) else 0.0
                F[3*idx + 1] = float(row["Carga Fy (ton)"]) if not pd.isna(row["Carga Fy (ton)"]) else 0.0
                F[3*idx + 2] = float(row["Carga Fz (ton)"]) if not pd.isna(row["Carga Fz (ton)"]) else 0.0
                if row["Restringido_X"]: gdl_restringidos.append(3*idx)
                if row["Restringido_Y"]: gdl_restringidos.append(3*idx + 1)
                if row["Restringido_Z"]: gdl_restringidos.append(3*idx + 2)
                
            gdl_libres = [i for i in range(n_gdl) if i not in gdl_restringidos]
            
            K = np.zeros((n_gdl, n_gdl))
            for _, barra in barras_clean.iterrows():
                idx1 = nodo_idx[int(barra["Nodo_Inicial"])]
                idx2 = nodo_idx[int(barra["Nodo_Final"])]
                n1, n2 = nodos_clean.iloc[idx1], nodos_clean.iloc[idx2]
                dx, dy, dz = n2["X (m)"] - n1["X (m)"], n2["Y (m)"] - n1["Y (m)"], n2["Z (m)"] - n1["Z (m)"]
                L = np.sqrt(dx**2 + dy**2 + dz**2)
                l, m, n_dir = dx/L, dy/L, dz/L
                EA_L = (barra["Área (m2)"] * barra["E (ton/m2)"]) / L
                v = np.array([l, m, n_dir])
                mat = np.outer(v, v)
                k_local = EA_L * np.block([[mat, -mat], [-mat, mat]])
                gdl = [3*idx1, 3*idx1+1, 3*idx1+2, 3*idx2, 3*idx2+1, 3*idx2+2]
                for i in range(6):
                    for j in range(6):
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
                dx, dy, dz = n2["X (m)"] - n1["X (m)"], n2["Y (m)"] - n1["Y (m)"], n2["Z (m)"] - n1["Z (m)"]
                L = np.sqrt(dx**2 + dy**2 + dz**2)
                l, m, n_dir = dx/L, dy/L, dz/L
                u = np.array([U[3*idx1], U[3*idx1+1], U[3*idx1+2], U[3*idx2], U[3*idx2+1], U[3*idx2+2]])
                delta_L = l*(u[3] - u[0]) + m*(u[4] - u[1]) + n_dir*(u[5] - u[2])
                N = np.round((barra["Área (m2)"] * barra["E (ton/m2)"] / L) * delta_L, 4)
                fuerzas_axiales.append(N)
                estados.append("Tracción" if N > 0 else ("Compresión" if N < 0 else "Nulo"))

            st.balloons()
            st.success("✅ ¡Estructura 3D resuelta con éxito!")
            tab1, tab2, tab3, tab4 = st.tabs(["📉 Desplazamientos y Reacciones", "🧮 Matriz de Rigidez Global (3D)", "🔗 Fuerzas Axiales", "🎨 Gráfico 3D de Esfuerzos"])
            
            with tab1:
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.write("**Desplazamientos Nodales 3D (m)**")
                    desp_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Dx": [f"{x:.6f}" for x in U[0::3]], "Dy": [f"{x:.6f}" for x in U[1::3]], "Dz": [f"{x:.6f}" for x in U[2::3]]})
                    st.dataframe(desp_df, hide_index=True, use_container_width=True)
                with res_col2:
                    st.write("**Reacciones en Apoyos 3D (ton)**")
                    reac_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Rx": np.round(R[0::3], 3), "Ry": np.round(R[1::3], 3), "Rz": np.round(R[2::3], 3)})
                    reac_df = reac_df[(nodos_clean["Restringido_X"].values) | (nodos_clean["Restringido_Y"].values) | (nodos_clean["Restringido_Z"].values)]
                    st.dataframe(reac_df, hide_index=True, use_container_width=True)

            with tab2:
                st.write("**Matriz de Rigidez Global 3D (K)**")
                gdl_labels = [f"N{int(n)}-{e}" for n in nodos_clean["Nodo"] for e in ['X', 'Y', 'Z']]
                K_df = pd.DataFrame(K, columns=gdl_labels, index=gdl_labels)
                st.dataframe(K_df.style.format("{:.2f}"), use_container_width=True)

            with tab3:
                st.write("**Fuerzas Internas en los Elementos 3D**")
                fuerzas_df = pd.DataFrame({"Barra": barras_clean["Barra"].astype(int), "Nodo Inicial": barras_clean["Nodo_Inicial"].astype(int), "Nodo Final": barras_clean["Nodo_Final"].astype(int), "Fuerza Axial (ton)": fuerzas_axiales, "Estado": estados})
                st.dataframe(fuerzas_df, hide_index=True, use_container_width=True)

            with tab4:
                st.write("**Gráfico Espacial de Esfuerzos (3D)**")
                fig2 = plt.figure(figsize=(10, 6))
                ax2 = fig2.add_subplot(projection='3d')
                fig2.patch.set_facecolor('#f0f2f6')
                for idx, barra in barras_clean.iterrows():
                    n1 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
                    n2 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Final"]].iloc[0]
                    N = fuerzas_axiales[idx]
                    color = '#3498db' if N > 0 else ('#e74c3c' if N < 0 else '#95a5a6')
                    etiqueta = f"{abs(N):.2f} Tn (T)" if N > 0 else (f"{abs(N):.2f} Tn (C)" if N < 0 else "0.00 Tn")
                    ax2.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], [n1["Z (m)"], n2["Z (m)"]], color=color, lw=4)
                    ax2.text(np.mean([n1["X (m)"], n2["X (m)"]]), np.mean([n1["Y (m)"], n2["Y (m)"]]), np.mean([n1["Z (m)"], n2["Z (m)"]]), etiqueta, color='black', fontsize=9, fontweight='bold')
                ax2.scatter(nodos_clean["X (m)"], nodos_clean["Y (m)"], nodos_clean["Z (m)"], c='black', s=50)
                blue_patch, red_patch, gray_patch = mpatches.Patch(color='#3498db', label='Tracción (+)'), mpatches.Patch(color='#e74c3c', label='Compresión (-)'), mpatches.Patch(color='#95a5a6', label='Nulo (0)')
                ax2.legend(handles=[blue_patch, red_patch, gray_patch], loc='upper right')
                ax2.set_xlabel('X (m)')
                ax2.set_ylabel('Y (m)')
                ax2.set_zlabel('Z (m)')
                st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ Error matemático. Verifica los datos ingresados. Detalle técnico: {e}")
