import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Configuración inicial
st.set_page_config(page_title="SYNCRET - Proyectos 3D", page_icon="🏗️", layout="wide")

# --- DISEÑO VISUAL Y ESTILOS AVANZADOS ---
st.markdown("""
<style>
    /* Fondo con temática de Construcción y Análisis Estructural */
    .stApp { 
        background: linear-gradient(rgba(9, 13, 22, 0.90), rgba(20, 27, 45, 0.94)), 
                    url('https://images.unsplash.com/photo-1503387762-592deb58ef4e?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    h1, h2, h3 { color: #f7fafc !important; text-align: center; font-family: sans-serif; }
    
    /* Estilos base para los botones interactivos de cada ejercicio */
    .stButton button {
        border-radius: 18px !important;
        font-weight: bold !important;
        font-size: 22px !important;
        height: 95px !important;
        width: 100% !important;
        color: white !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        transition: all 0.35s ease-in-out;
        border: 2px solid rgba(255,255,255,0.25) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        letter-spacing: 1.2px;
    }
    
    .stButton button:hover {
        transform: translateY(-5px) scale(1.02);
        filter: brightness(1.2);
        border-color: rgba(255,255,255,0.8) !important;
        cursor: pointer;
    }

    /* Colores personalizados para cada botón de ejercicio */
    div.stButton:nth-of-type(1) > button {
        background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }
    div.stButton:nth-of-type(2) > button {
        background: linear-gradient(135deg, #047857, #10b981) !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
    }
    div.stButton:nth-of-type(3) > button {
        background: linear-gradient(135deg, #b45309, #f59e0b) !important;
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
    }
    div.stButton:nth-of-type(4) > button {
        background: linear-gradient(135deg, #6d28d9, #8b5cf6) !important;
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
    }

    /* --- ESTILO PARA EL BOTÓN DE CÁLCULO CENTRADO Y GRANDE --- */
    .centered-calc-btn {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 35px 0 25px 0;
    }
    .centered-calc-btn button {
        background: linear-gradient(135deg, #ff416c, #ff4b2b) !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        height: 75px !important;
        border-radius: 40px !important;
        width: 100% !important;
        box-shadow: 0 0 25px rgba(255, 75, 43, 0.7) !important;
        border: 2px solid #ffffff !important;
        letter-spacing: 1.5px;
    }

    /* --- ESTILO PARA EL BOTÓN VOLVER CENTRADO Y GRANDE --- */
    .centered-back-btn {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .centered-back-btn button {
        background: linear-gradient(135deg, #475569, #1e293b) !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        height: 60px !important;
        border-radius: 30px !important;
        width: 100% !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE ESTADO PARA LA NAVEGACIÓN ---
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "menu"

if "ejercicio_seleccionado" not in st.session_state:
    st.session_state.ejercicio_seleccionado = "Ejercicio 1"

# ==========================================
# 🏠 PANTALLA PRINCIPAL (MENÚ DE INICIO EN COLUMNA CENTRADA)
# ==========================================
if st.session_state.pagina_actual == "menu":
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 38px; font-weight: 700; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>
                📊 Sistematización del método de Rigidez
            </h1>
            <p style='color: #cbd5e1; font-size: 20px; font-weight: 400; margin-top: 0; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);'>
                Procedimiento para Armaduras en 3D
            </p>
            <p style='color: #ffffff; font-size: 17px; margin-top: 15px; margin-bottom: 30px; font-weight: 600;'>
                🎯 Selecciona el Sistema Estructural a Evaluar
            </p>
        </div>
    """, unsafe_allow_html=True)

    _, col_centro, _ = st.columns([1.2, 1.6, 1.2])

    with col_centro:
        if st.button("🔷 EJERCICIO 1", use_container_width=True):
            st.session_state.ejercicio_seleccionado = "Ejercicio 1"
            st.session_state.pagina_actual = "detalle"
            st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("🟢 EJERCICIO 2", use_container_width=True):
            st.session_state.ejercicio_seleccionado = "Ejercicio 2"
            st.session_state.pagina_actual = "detalle"
            st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("🔶 EJERCICIO 3", use_container_width=True):
            st.session_state.ejercicio_seleccionado = "Ejercicio 3"
            st.session_state.pagina_actual = "detalle"
            st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("🟣 EJERCICIO 4", use_container_width=True):
            st.session_state.ejercicio_seleccionado = "Ejercicio 4"
            st.session_state.pagina_actual = "detalle"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 14px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);'>Universidad Nacional del Santa • Análisis Estructural II • Desarrollado por Águila Nilo</p>", unsafe_allow_html=True)

# ==========================================
# 📊 PANTALLA DE DETALLE DEL EJERCICIO
# ==========================================
else:
    # Botón Volver al Menú Principal centrado y grande
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        st.markdown('<div class="centered-back-btn">', unsafe_allow_html=True)
        if st.button("🔙 Volver al Menú Principal", use_container_width=True):
            st.session_state.pagina_actual = "menu"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    ejercicio_activo = st.session_state.ejercicio_seleccionado
    st.title(f"🏗 SYNCRET: {ejercicio_activo}")
    st.markdown("---")

    # Enunciados estilizados con letras grandes
    if "Ejercicio 1" in ejercicio_activo:
        st.markdown("""
        <div style='background-color: rgba(30, 41, 59, 0.9); padding: 20px; border-radius: 15px; border-left: 6px solid #3b82f6; margin-bottom: 25px;'>
            <h3 style='color: #60a5fa !important; margin: 0 0 10px 0; text-align: left;'>📌 Enunciado Ejercicio 1</h3>
            <p style='color: #e2e8f0; font-size: 18px; line-height: 1.5; margin: 0;'>
                Torre piramidal espacial 3D con 3 apoyos en la base y un nudo superior con carga vertical de 20 Ton.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Imagen centrada para Ejercicio 1
        img_c1, img_c2, img_c3 = st.columns([1, 1.5, 1])
        with img_c2:
            try: st.image("ej1.jpg", caption="Esquema Referencial - Ejercicio 1", use_container_width=True)
            except: st.warning("⚠️ Sube la imagen 'ej1.jpg' a tu repositorio de GitHub.")

        nodos_default = pd.DataFrame({
            "Nodo": [1, 2, 3, 4], "X (m)": [0.0, 2.0, 1.0, 0.8], "Y (m)": [0.0, 0.0, 1.6, 1.0], "Z (m)": [0.0, 0.0, 0.0, 2.5],
            "Carga Fx (ton)": [0.0, 0.0, 0.0, 0.0], "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0], "Carga Fz (ton)": [0.0, 0.0, 0.0, -20.0],
            "Restringido_X": [True, True, True, False], "Restringido_Y": [True, True, True, False], "Restringido_Z": [True, True, True, False]
        })
        barras_default = pd.DataFrame({
            "Barra": [1, 2, 3, 4, 5, 6], "Nodo_Inicial": [1, 2, 1, 2, 3, 1], "Nodo_Final": [4, 4, 2, 3, 4, 3],
            "Área (m2)": [0.01]*6, "E (ton/m2)": [2e7]*6
        })

    elif "Ejercicio 2" in ejercicio_activo:
        st.markdown("""
        <div style='background-color: rgba(30, 41, 59, 0.9); padding: 20px; border-radius: 15px; border-left: 6px solid #10b981; margin-bottom: 25px;'>
            <h3 style='color: #34d399 !important; margin: 0 0 10px 0; text-align: left;'>📌 Enunciado Ejercicio 2</h3>
            <p style='color: #e2e8f0; font-size: 18px; line-height: 1.5; margin: 0;'>
                Armadura espacial 3D con 4 apoyos en la base, altura de 10.00m y cargas de 60 KN y 80 KN.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Imagen centrada para Ejercicio 2
        img_c1, img_c2, img_c3 = st.columns([1, 1.5, 1])
        with img_c2:
            try: st.image("ej2.jpg", caption="Esquema Referencial - Ejercicio 2", use_container_width=True)
            except: st.warning("⚠️ Sube la imagen 'ej2.jpg' a tu repositorio de GitHub.")
        
        nodos_default = pd.DataFrame({
            "Nodo": [1, 2, 3, 4, 5], "X (m)": [-4.0, 4.0, 0.0, 4.0, -4.0], "Y (m)": [-3.0, -3.0, 0.0, 3.0, 3.0], "Z (m)": [0.0, 0.0, 10.0, 0.0, 0.0],
            "Carga Fx (KN)": [0.0, 0.0, 60.0, 0.0, 0.0], "Carga Fy (KN)": [0.0, 0.0, -80.0, 0.0, 0.0], "Carga Fz (KN)": [0.0, 0.0, 0.0, 0.0, 0.0],
            "Restringido_X": [True, True, False, True, True], "Restringido_Y": [True, True, False, True, True], "Restringido_Z": [True, True, False, True, True]
        })
        barras_default = pd.DataFrame({
            "Barra": [1, 2, 3, 4], "Nodo_Inicial": [1, 2, 4, 5], "Nodo_Final": [3, 3, 3, 3],
            "Área (m2)": [0.001]*4, "E (KN/m2)": [2e8]*4
        })

    elif "Ejercicio 3" in ejercicio_activo:
        st.markdown("""
        <div style='background-color: rgba(30, 41, 59, 0.9); padding: 20px; border-radius: 15px; border-left: 6px solid #f59e0b; margin-bottom: 25px;'>
            <h3 style='color: #fbbf24 !important; margin: 0 0 10px 0; text-align: left;'>📌 Enunciado Ejercicio 3</h3>
            <p style='color: #e2e8f0; font-size: 18px; line-height: 1.5; margin: 0;'>
                Pirámide espacial con 3 apoyos fijos en la base (A, B, C) de 4.0m x 3.0m, altura de 3.0m y una carga vertical de 18 Ton en el nudo superior D.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Imagen centrada para Ejercicio 3
        img_c1, img_c2, img_c3 = st.columns([1, 1.5, 1])
        with img_c2:
            try: st.image("ej3.jpg", caption="Esquema Referencial - Ejercicio 3", use_container_width=True)
            except: st.warning("⚠️ Sube la imagen 'ej3.jpg' a tu repositorio de GitHub.")

        nodos_default = pd.DataFrame({
            "Nodo": [1, 2, 3, 4, 5], 
            "X (m)": [0.0, 4.0, 2.0, 2.0, 2.0],
            "Y (m)": [0.0, 0.0, 3.0, 1.5, 1.5],
            "Z (m)": [0.0, 0.0, 0.0, 0.0, 3.0],
            "Carga Fx (ton)": [0.0, 0.0, 0.0, 0.0, 0.0],
            "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0, 0.0],
            "Carga Fz (ton)": [0.0, 0.0, 0.0, 0.0, -18.0],
            "Restringido_X": [True, True, True, False, False],
            "Restringido_Y": [True, True, True, False, False],
            "Restringido_Z": [True, True, True, False, False]
        })
        barras_default = pd.DataFrame({
            "Barra": [1, 2, 3, 4, 5, 6, 7, 8], 
            "Nodo_Inicial": [1, 2, 1, 2, 3, 1, 2, 3], 
            "Nodo_Final":   [2, 3, 4, 4, 4, 5, 5, 5],
            "Área (m2)":    [0.01]*8, 
            "E (ton/m2)":   [2e7]*8
        })

    else: # Ejercicio 4
        st.markdown("""
        <div style='background-color: rgba(30, 41, 59, 0.9); padding: 20px; border-radius: 15px; border-left: 6px solid #8b5cf6; margin-bottom: 25px;'>
            <h3 style='color: #a78bfa !important; margin: 0 0 10px 0; text-align: left;'>📌 Enunciado Ejercicio 4</h3>
            <p style='color: #e2e8f0; font-size: 18px; line-height: 1.5; margin: 0;'>
                Torre piramidal espacial con 4 apoyos en la base de 5.0m x 3.0m, altura de 3.5m y carga vertical de 14 Tn en el nudo superior D.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Imagen centrada para Ejercicio 4
        img_c1, img_c2, img_c3 = st.columns([1, 1.5, 1])
        with img_c2:
            try: st.image("ej4.jpg", caption="Esquema Referencial - Ejercicio 4", use_container_width=True)
            except: st.warning("⚠️ Sube la imagen 'ej4.jpg' a tu repositorio de GitHub.")

        nodos_default = pd.DataFrame({
            "Nodo": [1, 2, 3, 4, 5, 6], 
            "X (m)": [0.0, 5.0, 5.0, 0.0, 2.5, 0.0],
            "Y (m)": [0.0, 0.0, 3.0, 3.0, 1.5, 0.0],
            "Z (m)": [0.0, 0.0, 0.0, 0.0, 0.0, 3.5],
            "Carga Fx (ton)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Carga Fy (ton)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Carga Fz (ton)": [0.0, 0.0, 0.0, 0.0, 0.0, -14.0],
            "Restringido_X": [True, True, True, True, False, False],
            "Restringido_Y": [True, True, True, True, False, False],
            "Restringido_Z": [True, True, True, True, False, False]
        })
        barras_default = pd.DataFrame({
            "Barra": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 
            "Nodo_Inicial": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 5], 
            "Nodo_Final":   [2, 3, 4, 1, 5, 5, 5, 5, 6, 6, 6, 6, 6],
            "Área (m2)":    [0.01]*13, 
            "E (ton/m2)":   [2e7]*13
        })

    col_nodos, col_barras = st.columns(2)
    with col_nodos:
        st.subheader("📍 Coordenadas y Cargas (3D)")
        nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key=f"nodos_{ejercicio_activo}", use_container_width=True)
    with col_barras:
        st.subheader("🔗 Conectividad de Barras (3D)")
        barras_df = st.data_editor(barras_default, num_rows="dynamic", key=f"barras_{ejercicio_activo}", use_container_width=True)

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

    ax.set_xlabel('X (m)', labelpad=12)
    ax.set_ylabel('Y (m)', labelpad=12)
    ax.set_zlabel('Z (m)', labelpad=12)
    ax.margins(0.1)
    st.pyplot(fig)
    st.markdown("---")

    # --- MOTOR MATRICIAL 3D (BOTÓN DE CÁLCULO CENTRADO Y GRANDE) ---
    col_esp1, col_calc, col_esp2 = st.columns([1, 2.5, 1])
    with col_calc:
        st.markdown('<div class="centered-calc-btn">', unsafe_allow_html=True)
        iniciar_calculo = st.button("🚀 INICIAR CÁLCULO MATRICIAL 3D", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if iniciar_calculo:
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
                
                F[3*idx]   = float(row[fx_col]) if not pd.isna(row[fx_col]) else 0.0
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
            
            U_libres = np.linalg.pinv(K_libres).dot(F_libres)
            
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

            # Lanza globos de celebración y muestra cartel centrado en pantalla
            st.balloons()
            st.markdown("""
                <div style='text-align: center; background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(5, 150, 105, 0.35)); border: 2px solid #10b981; padding: 22px; border-radius: 18px; margin: 30px auto; max-width: 750px; box-shadow: 0 0 25px rgba(16, 185, 129, 0.5);'>
                    <h3 style='color: #34d399 !important; margin: 0; font-size: 24px; font-weight: 800;'>🚀 ¡Cálculo de la armadura espacial completado con éxito!</h3>
                    <p style='color: #e2e8f0; font-size: 16px; margin: 8px 0 0 0;'>Análisis matricial estructural procesado correctamente.</p>
                </div>
            """, unsafe_allow_html=True)
            
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
                        ax2.text(x, y, z - 0.5, texto_reac, color='#8e44ad', fontsize=8, fontweight='bold', bbox=dict(facecolor='white', alpha=0.9, edgecolor='#8e44ad', boxstyle='round,pad=0.3'))

                blue_patch, red_patch, gray_patch = mpatches.Patch(color='#3498db', label='Tensión (+)'), mpatches.Patch(color='#e74c3c', label='Compresión (-)'), mpatches.Patch(color='#95a5a6', label='Nulo (0)')
                ax2.legend(handles=[blue_patch, red_patch, gray_patch], loc='upper right')
                
                ax2.set_xlabel('X (m)', labelpad=12)
                ax2.set_ylabel('Y (m)', labelpad=12)
                ax2.set_zlabel('Z (m)', labelpad=12)
                st.pyplot(fig2)

        except Exception as e:
            st.error(f"❌ Error en el cálculo matricial. Verifica la geometría y los datos. Detalle: {e}")
