import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Configuración inicial
st.set_page_config(page_title="SYNCRET - Proyectos 3D", page_icon="🏗️", layout="wide")

# --- DISEÑO VISUAL Y ESTILOS ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom right, #0e1117, #1a202c); }
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; font-size: 20px; font-weight: bold;
        padding: 12px 24px; border-radius: 10px; border: none; width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff3333; transform: translateY(-2px);
    }
    h1, h2, h3 { color: #4B90FF !important; }
</style>
""", unsafe_allow_html=True)

# --- PANEL LATERAL: SELECTOR DE LOS 4 EJERCICIOS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3204/3204094.png", width=80)
    st.header("📚 Panel de Ejercicios 3D")
    st.info("Selecciona el sistema estructural solicitado por el docente:")
    
    ejercicio_seleccionado = st.radio(
        "Ejercicios del Trabajo:",
        ["Ejercicio 1 (Torre Piramidal Base Triangular)", "Ejercicio 2 (Torre Espacial de Clases)", "Ejercicio 3 (Armadura Espacial Múltiple)", "Ejercicio 4"]
    )
    
    st.markdown("---")
    st.markdown("**Universidad Nacional del Santa**\n*Curso: Análisis Estructural II*[cite: 21]\nDesarrollado por: *Nilo Jara*[cite: 21]")

# --- TÍTULO PRINCIPAL ---
st.title(f"🏗 SYNCRET: {ejercicio_seleccionado}")
st.markdown("*Sistematización del Método de Rigidez - Armaduras Espaciales 3D*[cite: 21]")
st.markdown("---")

# --- CARGAR DATOS Y MOSTRAR ENUNCIADO E IMAGEN ---
if "Ejercicio 1" in ejercicio_seleccionado:
    st.info("📌 **Enunciado Ejercicio 1:** Torre piramidal espacial 3D con 3 apoyos en la base y un nudo superior D con carga vertical de 20 Ton.")
    try: st.image("ej1.jpg", caption="Esquema Referencial - Ejercicio 1", width=500)
    except: st.warning("⚠️ Sube la imagen 'ej1.jpg' a tu repositorio.")

    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4], "X (m)": [0.0, 2.0, 1.0, 0.8], "Y (m)": [0.0, 0.0, 1.6, 1.0], "Z (m)": [0.0, 0.0, 0.0, 2.5],
        "Carga Fx (ton)": [0.0, 0.0, 0.0, 0.0], "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0], "Carga Fz (ton)": [0.0, 0.0, 0.0, -20.0],
        "Restringido_X": [True, True, True, False], "Restringido_Y": [True, True, True, False], "Restringido_Z": [True, True, True, False]
    })
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3, 4, 5, 6], "Nodo_Inicial": [1, 2, 1, 2, 3, 1], "Nodo_Final": [4, 4, 2, 3, 4, 3],
        "Área (m2)": [0.01]*6, "E (ton/m2)": [2e7]*6
    })

elif "Ejercicio 2" in ejercicio_seleccionado:
    st.info("📌 **Enunciado Ejercicio 2 (Clase):** Armadura espacial 3D con 4 apoyos en la base, altura de 10.00m y cargas de 60 KN y 80 KN[cite: 14].")
    try: st.image("ej2.jpg", caption="Esquema Referencial - Ejercicio 2 (Clase)", width=600)
    except: st.warning("⚠️ Sube la imagen 'ej2.jpg' a tu repositorio.")
    
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4, 5], "X (m)": [-4.0, 4.0, 0.0, 4.0, -4.0], "Y (m)": [-3.0, -3.0, 0.0, 3.0, 3.0], "Z (m)": [0.0, 0.0, 10.0, 0.0, 0.0],
        "Carga Fx (KN)": [0.0, 0.0, 60.0, 0.0, 0.0], "Carga Fy (KN)": [0.0, 0.0, -80.0, 0.0, 0.0], "Carga Fz (KN)": [0.0, 0.0, 0.0, 0.0, 0.0],
        "Restringido_X": [True, True, False, True, True], "Restringido_Y": [True, True, False, True, True], "Restringido_Z": [True, True, False, True, True]
    })
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3, 4], "Nodo_Inicial": [1, 2, 4, 5], "Nodo_Final": [3, 3, 3, 3],
        "Área (m2)": [0.001]*4, "E (KN/m2)": [2e8]*4
    })

elif "Ejercicio 3" in ejercicio_seleccionado:
    st.info("📌 **Enunciado Ejercicio 3:** Armadura espacial de varios niveles con apoyos en E, F, G. Carga vertical de 3.5 Ton en el nudo C. Considere $E = 2.1 \times 10^7\text{ Ton/m}^2$ y $A = 0.15\text{ m}^2$.")
    try: st.image("ej3.jpg", caption="Esquema Referencial - Ejercicio 3", width=600)
    except: st.warning("⚠️ Sube la imagen 'ej3.jpg' a tu repositorio.")

    # Nodos aproximados basados en la geometría 3D del gráfico (E, F, G en base z=0; A, B en z=4; C, D en z=8)
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4, 5, 6, 7], # 1:E, 2:F, 3:G, 4:A, 5:B, 6:C, 7:D
        "X (m)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Y (m)": [0.0, 3.0, 6.0, 0.0, 3.0, 0.0, 3.0],
        "Z (m)": [0.0, 0.0, 0.0, 4.0, 4.0, 8.0, 8.0],
        "Carga Fx (ton)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Carga Fz (ton)": [0.0, 0.0, 0.0, 0.0, 0.0, -3.5, 0.0], # Carga de 3.5 Ton en C (Nodo 6)
        "Restringido_X": [True, True, True, False, False, False, False],
        "Restringido_Y": [True, True, True, False, False, False, False],
        "Restringido_Z": [True, True, True, False, False, False, False]
    })
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3, 4, 5, 6, 7, 8], 
        "Nodo_Inicial": [1, 1, 2, 2, 3, 4, 4, 5], 
        "Nodo_Final": [4, 5, 4, 5, 5, 6, 7, 7],
        "Área (m2)": [0.15]*8, 
        "E (ton/m2)": [2.1e7]*8
    })

else:
    st.info("📌 **Enunciado Ejercicio 4:** Cuarto sistema estructural espacial.")
    try: st.image("ej4.jpg", caption="Esquema Referencial - Ejercicio 4", width=500)
    except: pass

    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4], "X (m)": [0.0, 6.0, 3.0, 3.0], "Y (m)": [0.0, 0.0, 5.0, 2.5], "Z (m)": [0.0, 0.0, 0.0, 9.0],
        "Carga Fx (KN)": [0.0, 0.0, 0.0, 40.0], "Carga Fy (KN)": [0.0, 0.0, 0.0, 20.0], "Carga Fz (KN)": [0.0, 0.0, 0.0, -75.0],
        "Restringido_X": [True, True, True, False], "Restringido_Y": [True, True, True, False], "Restringido_Z": [True, True, True, False]
    })
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3], "Nodo_Inicial": [1, 2, 3], "Nodo_Final": [4, 4, 4],
        "Área (m2)": [0.0015]*3, "E (KN/m2)": [2e8]*3
    })

col_nodos, col_barras = st.columns(2)
with col_nodos:
    st.subheader("📍 Coordenadas y Cargas (3D)")
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key=f"nodos_{ejercicio_seleccionado}", use_container_width=True)
with col_barras:
    st.subheader("🔗 Conectividad de Barras (3D)")
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key=f"barras_{ejercicio_seleccionado}", use_container_width=True)

# --- VISTA PREVIA 3D ---
st.subheader("👁️ Vista Previa 3D de la Estructura")
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

# --- MOTOR MATRICIAL 3D ---
if st.button("🚀 INICIAR CÁLCULO MATRICIAL 3D"):
    try:
        nodos_clean = nodos_df.dropna(subset=["Nodo", "X (m)", "Y (m)", "Z (m)"])
        barras_clean = barras_df.dropna(subset=["Nodo_Inicial", "Nodo_Final"])
        
        n_nodos = len(nodos_clean)
        n_gdl = 3 * n_nodos
        
        nodo_idx = {int(row["Nodo"]): i for i, row in nodos_clean.iterrows()}
        F = np.zeros(n_gdl)
        gdl_restringidos = []
        
        for i, row in nodos_clean.iterrows():
            idx = nodo_idx[row["Nodo"]]
            fx_col = [c for c in nodos_clean.columns if "Fx" in c][0]
            fy_col = [c for c in nodos_clean.columns if "Fy" in c][0]
            fz_col = [c for c in nodos_clean.columns if "Fz" in c][0]
            
            F[3*idx]     = float(row[fx_col]) if not pd.isna(row[fx_col]) else 0.0
            F[3*idx + 1] = float(row[fy_col]) if not pd.isna(row[fy_col]) else 0.0
            F[3*idx + 2] = float(row[fz_col]) if not pd.isna(row[fz_col]) else 0.0
            
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
            
            e_col = [c for c in barras_clean.columns if "E (" in c][0]
            EA_L = (barra["Área (m2)"] * barra[e_col]) / L
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
            N = np.round((barra["Área (m2)"] * barra[e_col] / L) * delta_L, 4)
            fuerzas_axiales.append(N)
            estados.append("Tensión (Tracción)" if N > 0 else ("Compresión" if N < 0 else "Nulo"))

        st.balloons()
        st.success("✅ ¡Cálculo de la armadura espacial completado con éxito!")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📉 Desplazamientos y Reacciones", "🧮 Matriz de Rigidez (K)", "🔗 Fuerzas Axiales", "🎨 Gráfico 3D de Esfuerzos"])
        
        with tab1:
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.write("**Desplazamientos Nodales 3D (m)**")
                desp_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Dx": [f"{x:.6f}" for x in U[0::3]], "Dy": [f"{x:.6f}" for x in U[1::3]], "Dz": [f"{x:.6f}" for x in U[2::3]]})
                st.dataframe(desp_df, hide_index=True, use_container_width=True)
            with res_col2:
                st.write("**Reacciones en Apoyos 3D**")
                reac_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Rx": np.round(R[0::3], 3), "Ry": np.round(R[1::3], 3), "Rz": np.round(R[2::3], 3)})
                reac_df = reac_df[(nodos_clean["Restringido_X"].values) | (nodos_clean["Restringido_Y"].values) | (nodos_clean["Restringido_Z"].values)]
                st.dataframe(reac_df, hide_index=True, use_container_width=True)

        with tab2:
            st.write("**Matriz de Rigidez Global del Sistema 3D (K)**")
            gdl_labels = [f"N{int(n)}-{e}" for n in nodos_clean["Nodo"] for e in ['X', 'Y', 'Z']]
            K_df = pd.DataFrame(K, columns=gdl_labels, index=gdl_labels)
            st.dataframe(K_df.style.format("{:.2f}"), use_container_width=True)

        with tab3:
            st.write("**Fuerzas Internas en los Elementos**")
            fuerzas_df = pd.DataFrame({"Barra": barras_clean["Barra"].astype(int), "Nodo Inicial": barras_clean["Nodo_Inicial"].astype(int), "Nodo Final": barras_clean["Nodo_Final"].astype(int), "Fuerza Axial": fuerzas_axiales, "Estado": estados})
            st.dataframe(fuerzas_df, hide_index=True, use_container_width=True)

        with tab4:
            st.write("**Visualización Tridimensional de Esfuerzos y Reacciones en Apoyos**")
            fig2 = plt.figure(figsize=(10, 6))
            ax2 = fig2.add_subplot(projection='3d')
            fig2.patch.set_facecolor('#f0f2f6')
            
            for idx, barra in barras_clean.iterrows():
                n1 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
                n2 = nodos_clean[nodos_clean["Nodo"] == barra["Nodo_Final"]].iloc[0]
                N = fuerzas_axiales[idx]
                color = '#3498db' if N > 0 else ('#e74c3c' if N < 0 else '#95a5a6')
                etiqueta = f"{abs(N):.2f} (T)" if N > 0 else (f"{abs(N):.2f} (C)" if N < 0 else "0.00")
                ax2.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], [n1["Z (m)"], n2["Z (m)"]], color=color, lw=4)
                ax2.text(np.mean([n1["X (m)"], n2["X (m)"]]), np.mean([n1["Y (m)"], n2["Y (m)"]]), np.mean([n1["Z (m)"], n2["Z (m)"]]), etiqueta, color='black', fontsize=9, fontweight='bold')
            
            ax2.scatter(nodos_clean["X (m)"], nodos_clean["Y (m)"], nodos_clean["Z (m)"], c='black', s=50)

            for idx, row in nodos_clean.iterrows():
                n_idx = nodo_idx[int(row["Nodo"])]
                rx = R[3*n_idx]
                ry = R[3*n_idx+1]
                rz = R[3*n_idx+2]
                x, y, z = row["X (m)"], row["Y (m)"], row["Z (m)"]
                
                if row["Restringido_X"] or row["Restringido_Y"] or row["Restringido_Z"]:
                    texto_reac = f"N{int(row['Nodo'])} Reacc:\nRx:{rx:.2f}\nRy:{ry:.2f}\nRz:{rz:.2f}"
                    ax2.text(x, y, z - 0.3, texto_reac, color='#8e44ad', fontsize=8, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8, edgecolor='#8e44ad', boxstyle='round,pad=0.3'))

            blue_patch, red_patch, gray_patch = mpatches.Patch(color='#3498db', label='Tensión (+)'), mpatches.Patch(color='#e74c3c', label='Compresión (-)'), mpatches.Patch(color='#95a5a6', label='Nulo (0)')
            ax2.legend(handles=[blue_patch, red_patch, gray_patch], loc='upper right')
            ax2.set_xlabel('X (m)')
            ax2.set_ylabel('Y (m)')
            ax2.set_zlabel('Z (m)')
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ Error en el cálculo matricial. Verifica la geometría y los datos. Detalle: {e}")
