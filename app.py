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
    
    /* Estilos para hacer las pestañas (Tabs) más grandes, visibles y estéticas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 52px;
        background-color: rgba(30, 41, 59, 0.85);
        border-radius: 12px 12px 0px 0px;
        padding: 0 12px;
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

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
    
    # Tarjeta superior con el autor destacado
    st.markdown("""
        <div style='text-align: center; background: linear-gradient(135deg, rgba(30, 58, 138, 0.65), rgba(37, 99, 235, 0.65)); border: 1.5px solid rgba(255,255,255,0.35); padding: 12px 25px; border-radius: 35px; max-width: 650px; margin: 0 auto 25px auto; box-shadow: 0 6px 20px rgba(0,0,0,0.6);'>
            <p style='color: #ffffff; font-size: 16px; font-weight: 600; margin: 0; letter-spacing: 0.5px;'>
                👨‍💻 Creado y Desarrollado por: <span style='color: #93c5fd; font-weight: 800;'>Jara Aguila Nilo</span> • UNS
            </p>
        </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 14px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);'>Universidad Nacional del Santa • Análisis Estructural II • Desarrollado por Jara Aguila Nilo</p>", unsafe_allow_html=True)

# ==========================================
# 📊 PANTALLA DE DETALLE DEL EJERCICIO
# ==========================================
else:
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

    if "Ejercicio 1" in ejercicio_activo:
        st.markdown("""
        <div style='background-color: rgba(30, 41, 59, 0.9); padding: 20px; border-radius: 15px; border-left: 6px solid #3b82f6; margin-bottom: 25px;'>
            <h3 style='color: #60a5fa !important; margin: 0 0 10px 0; text-align: left;'>📌 Enunciado Ejercicio 1</h3>
            <p style='color: #e2e8f0; font-size: 18px; line-height: 1.5; margin: 0;'>
                Torre piramidal espacial 3D con 3 apoyos en la base y un nudo superior con carga vertical de 20 Ton.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
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

    # --- VISTA PREVIA 3D (CON ETIQUETADO DE BARRAS EN ROJO) ---
    st.subheader("👁️ Vista Previa 3D de la Estructura")
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(projection='3d')
    fig.patch.set_facecolor('#f0f2f6')

    for _, barra in barras_df.iterrows():
        try:
            n1 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Inicial"]].iloc[0]
            n2 = nodos_df[nodos_df["Nodo"] == barra["Nodo_Final"]].iloc[0]
            
            ax.plot([n1["X (m)"], n2["X (m)"]], [n1["Y (m)"], n2["Y (m)"]], [n1["Z (m)"], n2["Z (m)"]], color='#2c3e50', lw=2)
            
            mx = (n1["X (m)"] + n2["X (m)"]) / 2
            my = (n1["Y (m)"] + n2["Y (m)"]) / 2
            mz = (n1["Z (m)"] + n2["Z (m)"]) / 2
            ax.text(mx, my, mz, f"[{int(barra['Barra'])}]", color='red', fontsize=10, fontweight='bold')
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

    # --- MOTOR MATRICIAL 3D ---
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
            elementos_info = []
            matrices_locales = {}
            matrices_globales_elemento = {}
            
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
                
                # Matriz global del elemento (Ke)
                k_elemento_global = EA_L * np.block([[mat, -mat], [-mat, mat]])
                matrices_globales_elemento[int(barra["Barra"])] = k_elemento_global
                
                # Matriz local pura (en el eje de la barra x')
                k_local = np.zeros((6, 6))
                k_local[0,0] = EA_L; k_local[0,3] = -EA_L
                k_local[3,0] = -EA_L; k_local[3,3] = EA_L
                matrices_locales[int(barra["Barra"])] = k_local
                
                gdl = [3*idx1, 3*idx1+1, 3*idx1+2, 3*idx2, 3*idx2+1, 3*idx2+2]
                for i in range(6):
                    for j in range(6):
                        K[gdl[i], gdl[j]] += k_elemento_global[i, j]
                
                elementos_info.append({
                    "Barra": int(barra["Barra"]),
                    "Nodo Ini": int(barra["Nodo_Inicial"]),
                    "Nodo Fin": int(barra["Nodo_Final"]),
                    "Longitud (m)": round(L, 4),
                    "l (cos x)": round(l, 4),
                    "m (cos y)": round(m, 4),
                    "n (cos z)": round(n_dir, 4),
                    "Rigidez EA/L": round(EA_L, 2)
                })
                        
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

            # Lanza globos y cartel de éxito centrado
            st.balloons()
            st.markdown("""
                <div style='text-align: center; background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(5, 150, 105, 0.35)); border: 2px solid #10b981; padding: 22px; border-radius: 18px; margin: 30px auto; max-width: 750px; box-shadow: 0 0 25px rgba(16, 185, 129, 0.5);'>
                    <h3 style='color: #34d399 !important; margin: 0; font-size: 24px; font-weight: 800;'>🚀 ¡Cálculo de la armadura espacial completado con éxito!</h3>
                    <p style='color: #e2e8f0; font-size: 16px; margin: 8px 0 0 0;'>Análisis matricial estructural procesado correctamente.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- PESTAÑAS ORDENADAS EN FLUJO LÓGICO PROFESIONAL ---
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
                "📐 Geometría y Barras", 
                "📋 Partición de GDL", 
                "🧮 Matrices Locales (k)",
                "🌐 Matrices Globales (Ke)",
                "📑 Desglose por Elemento",
                "🧮 Matriz Global Particionada (K)", 
                "📉 Desplazamientos y Reacciones", 
                "🔗 Fuerzas Axiales", 
                "⚖️ Equilibrio Estático",
                "🎨 Gráfico 3D de Esfuerzos"
            ])
            
            with tab1:
                st.write("**📐 Propiedades Geométricas y Cosenos Directores de las Barras**")
                geom_df = pd.DataFrame(elementos_info)
                st.dataframe(geom_df, hide_index=True, use_container_width=True)

            with tab2:
                st.write("**📋 Tabla de Partición de Grados de Libertad (GDL)**")
                gdl_data = []
                for idx, row in nodos_clean.iterrows():
                    n_id = int(row["Nodo"])
                    gdl_x, gdl_y, gdl_z = 3*idx, 3*idx+1, 3*idx+2
                    gdl_data.append({
                        "Nodo": n_id,
                        "GDL X": f"{gdl_x} ({'Restringido' if row['Restringido_X'] else 'Libre'})",
                        "GDL Y": f"{gdl_y} ({'Restringido' if row['Restringido_Y'] else 'Libre'})",
                        "GDL Z": f"{gdl_z} ({'Restringido' if row['Restringido_Z'] else 'Libre'})"
                    })
                gdl_df = pd.DataFrame(gdl_data)
                st.dataframe(gdl_df, hide_index=True, use_container_width=True)
                st.info(f"💡 **Resumen Estático:** {len(gdl_libres)} GDL Libres (Submatriz K_LL) y {len(gdl_restringidos)} GDL Restringidos en apoyos.")

            with tab3:
                st.write("**🧮 Matriz de Rigidez Local ($k$) de cada Barra (6x6)**")
                local_labels = ["u1", "v1", "w1", "u2", "v2", "w2"]
                for b_id, k_mat in matrices_locales.items():
                    st.markdown(f"**Barra [{b_id}] (Eje Local)**")
                    k_df = pd.DataFrame(k_mat, columns=local_labels, index=local_labels)
                    st.dataframe(k_df.style.format("{:.2f}"), use_container_width=True)
                    st.markdown("---")

            with tab4:
                st.write("**🌐 Matriz Global de Rigidez de Cada Elemento ($Ke$)**")
                st.info("💡 Expresada con los grados de libertad globales exactos de sus nudos inicial y final.")
                for _, barra in barras_clean.iterrows():
                    b_id = int(barra["Barra"])
                    n_ini = int(barra["Nodo_Inicial"])
                    n_fin = int(barra["Nodo_Final"])
                    idx1 = nodo_idx[n_ini]
                    idx2 = nodo_idx[n_fin]
                    gdl_elem = [3*idx1, 3*idx1+1, 3*idx1+2, 3*idx2, 3*idx2+1, 3*idx2+2]
                    
                    st.markdown(f"**Elemento [{b_id}] (Nodos N{n_ini} $\\to$ N{n_fin})**")
                    ke_mat = matrices_globales_elemento[b_id]
                    ke_df = pd.DataFrame(ke_mat, columns=gdl_elem, index=gdl_elem)
                    st.dataframe(ke_df.style.format("{:.2f}"), use_container_width=True)
                    st.markdown("---")

            with tab5:
                st.write("**📑 Memoria Detallada y Ángulos por Elemento**")
                for _, barra in barras_clean.iterrows():
                    b_id = int(barra["Barra"])
                    n_ini = int(barra["Nodo_Inicial"])
                    n_fin = int(barra["Nodo_Final"])
                    
                    st.markdown(f"### 🔹 Elemento {b_id} (Nodos {n_ini} $\\to$ {n_fin})")
                    n1 = nodos_clean[nodos_clean["Nodo"] == n_ini].iloc[0]
                    n2 = nodos_clean[nodos_clean["Nodo"] == n_fin].iloc[0]
                    dx = n2["X (m)"] - n1["X (m)"]
                    dy = n2["Y (m)"] - n1["Y (m)"]
                    dz = n2["Z (m)"] - n1["Z (m)"]
                    L = np.sqrt(dx**2 + dy**2 + dz**2)
                    l, m, n_dir = dx/L, dy/L, dz/L
                    
                    ang_x = np.degrees(np.arccos(np.clip(l, -1.0, 1.0)))
                    ang_y = np.degrees(np.arccos(np.clip(m, -1.0, 1.0)))
                    ang_z = np.degrees(np.arccos(np.clip(n_dir, -1.0, 1.0)))
                    
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        st.markdown(f"""
                        * **Longitud ($L$):** {L:.4f} m
                        * **Cosenos y Ángulos Directores:**
                          * $l = {l:.4f}$ ($\\alpha = {ang_x:.2f}^\\circ$)
                          * $m = {m:.4f}$ ($\\beta = {ang_y:.2f}^\\circ$)
                          * $n = {n_dir:.4f}$ ($\\gamma = {ang_z:.2f}^\\circ$)
                        """)
                    with col_e2:
                        e_col = [c for c in barras_clean.columns if "E (" in c][0]
                        ea_l = (barra["Área (m2)"] * barra[e_col]) / L
                        st.markdown(f"""
                        * **Área ($A$):** {barra['Área (m2)']} m²
                        * **Rigidez Axial ($EA/L$):** {ea_l:.2f}
                        """)
                    st.markdown("---")

            with tab6:
                st.write("**🧮 Matriz Global del Sistema Particionada ($K_{LL}, K_{LR}, K_{RL}, K_{RR}$)**")
                st.markdown("""
                <div style='display: flex; gap: 15px; margin-bottom: 15px; font-size: 14px;'>
                    <span style='background: rgba(37, 99, 235, 0.3); border: 1px solid #3b82f6; padding: 4px 10px; border-radius: 6px;'>🟦 <b>K_LL</b> (Libres - Libres)</span>
                    <span style='background: rgba(217, 119, 6, 0.3); border: 1px solid #f59e0b; padding: 4px 10px; border-radius: 6px;'>🟧 <b>K_LR / K_RL</b> (Acoplamiento)</span>
                    <span style='background: rgba(109, 40, 217, 0.3); border: 1px solid #8b5cf6; padding: 4px 10px; border-radius: 6px;'>🟪 <b>K_RR</b> (Restringidos - Restringidos)</span>
                </div>
                """, unsafe_allow_html=True)
                
                gdl_ordenados = gdl_libres + gdl_restringidos
                K_ordenada = K[np.ix_(gdl_ordenados, gdl_ordenados)]
                n_free = len(gdl_libres)
                
                gdl_labels_ordenados = [
                    f"GDL {i} (L)" if i in gdl_libres else f"GDL {i} (R)"
                    for i in gdl_ordenados
                ]
                K_ord_df = pd.DataFrame(K_ordenada, columns=gdl_labels_ordenados, index=gdl_labels_ordenados)
                
                def style_partitions(x):
                    df_styles = pd.DataFrame('', index=x.index, columns=x.columns)
                    for r in range(len(x)):
                        for c in range(len(x.columns)):
                            if r < n_free and c < n_free:
                                df_styles.iloc[r, c] = 'background-color: rgba(37, 99, 235, 0.22); color: #93c5fd; font-weight: bold;'
                            elif r < n_free and c >= n_free:
                                df_styles.iloc[r, c] = 'background-color: rgba(217, 119, 6, 0.22); color: #fde68a;'
                            elif r >= n_free and c < n_free:
                                df_styles.iloc[r, c] = 'background-color: rgba(217, 119, 6, 0.22); color: #fde68a;'
                            else:
                                df_styles.iloc[r, c] = 'background-color: rgba(109, 40, 217, 0.22); color: #c4b5fd;'
                    return df_styles

                st.dataframe(K_ord_df.style.apply(style_partitions, axis=None).format("{:.2f}"), use_container_width=True)

            with tab7:
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

            with tab8:
                st.write("**Fuerzas Internas en los Elementos**")
                fuerzas_df = pd.DataFrame({"Barra": barras_clean["Barra"].astype(int), "Nodo Inicial": barras_clean["Nodo_Inicial"].astype(int), "Nodo Final": barras_clean["Nodo_Final"].astype(int), "Fuerza Axial": fuerzas_axiales, "Estado": estados})
                st.dataframe(fuerzas_df, hide_index=True, use_container_width=True)

            with tab9:
                st.write("**⚖️ Comprobación de Equilibrio Estático ($\sum F = 0$)**")
                ext_fx, ext_fy, ext_fz = np.sum(F[0::3]), np.sum(F[1::3]), np.sum(F[2::3])
                reac_rx, reac_ry, reac_rz = np.sum(R[0::3]), np.sum(R[1::3]), np.sum(R[2::3])
                
                eq_df = pd.DataFrame({
                    "Eje Coordenado": ["Eje X", "Eje Y", "Eje Z"],
                    "Fuerzas Externas Totales ($\sum F_{ext}$)": [ext_fx, ext_fy, ext_fz],
                    "Reacciones Totales ($\sum R$)": [reac_rx, reac_ry, reac_rz],
                    "Suma Global ($\sum F_{ext} + \sum R$)": [ext_fx + reac_rx, ext_fy + reac_ry, ext_fz + reac_rz]
                })
                numeric_cols_eq = [
                    "Fuerzas Externas Totales ($\sum F_{ext}$)",
                    "Reacciones Totales ($\sum R$)",
                    "Suma Global ($\sum F_{ext} + \sum R$)"
                ]
                st.dataframe(eq_df.style.format("{:.4f}", subset=numeric_cols_eq), hide_index=True, use_container_width=True)
                st.success("✅ ¡El sistema se encuentra en perfecto equilibrio estático ($\sum F \approx 0$)!")

            with tab10:
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
