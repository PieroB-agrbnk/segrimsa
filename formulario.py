"""
SEGRIMSA - Formulario de Registro de Catequesis
Version para Streamlit Community Cloud
URL: https://segrimsa-registro.streamlit.app
"""

import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime
from database import get_connection, crear_tablas, DB_PATH

# Auto-setup
crear_tablas()

# ========================================
# CONFIG DE PAGINA
# ========================================
st.set_page_config(
    page_title="SEGRIMSA - Registro",
    page_icon="https://segrimsa.com/cdn/shop/files/logo-header.svg",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ========================================
# CSS MOBILE-FRIENDLY
# ========================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main > div {
        padding: 0.5rem 1rem;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .header-box {
        background: linear-gradient(135deg, #1B3A5C 0%, #2980B9 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    .header-box h1 { color: white; font-size: 1.5rem; margin: 0; }
    .header-box p { color: #d0e8ff; font-size: 0.9rem; margin: 5px 0 0 0; }
    
    .stTextInput input, .stSelectbox select {
        font-size: 16px !important;
        padding: 12px !important;
    }
    
    .stButton > button[kind="primary"] {
        width: 100%;
        padding: 15px !important;
        font-size: 1.1rem !important;
        border-radius: 10px !important;
    }
    
    .success-box {
        background: #d4edda;
        border: 2px solid #28a745;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    .success-box h2 { color: #155724; font-size: 1.3rem; }
    
    .section-title {
        background: #f0f4f8;
        padding: 8px 15px;
        border-radius: 8px;
        border-left: 4px solid #2980B9;
        font-weight: bold;
        margin: 15px 0 10px 0;
    }
    
    [data-testid="collapsedControl"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ========================================
# CONFIG DEL EVENTO
# ========================================
EVENTO = "Primera Comunion 2026"
SACRAMENTO = "Primera Comunion"
ANIO = 2026


# ========================================
# FUNCIONES DB
# ========================================
def guardar_registro(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registros_catequesis 
        (nombre_padre, telefono, email, nombre_nino, colegio, grado,
         tiene_hermano, hermano1_nombre, hermano1_colegio, hermano1_grado,
         hermano2_nombre, hermano2_colegio, hermano2_grado,
         evento, parroquia, sacramento, anio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["nombre_padre"], data["telefono"], data["email"],
        data["nombre_nino"], data["colegio"], data["grado"],
        data["tiene_hermano"],
        data.get("hermano1_nombre"), data.get("hermano1_colegio"), data.get("hermano1_grado"),
        data.get("hermano2_nombre"), data.get("hermano2_colegio"), data.get("hermano2_grado"),
        EVENTO, "", SACRAMENTO, ANIO,
    ))
    registro_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return registro_id


def contar_registros():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM registros_catequesis")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def obtener_registros():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT id, nombre_padre, nombre_nino, telefono, email, 
               colegio, grado, fecha_registro
        FROM registros_catequesis 
        ORDER BY id DESC
    """, conn)
    conn.close()
    return df


# ========================================
# INICIALIZAR
# ========================================
if "submitted" not in st.session_state:
    st.session_state.submitted = False


# ========================================
# HEADER
# ========================================
st.markdown("""
<div class="header-box">
    <h1>SEGRIMSA</h1>
    <p>Registro de Catequesis</p>
</div>
""", unsafe_allow_html=True)


# ========================================
# EXITO (si ya se envio)
# ========================================
if st.session_state.submitted:
    st.markdown("""
    <div class="success-box">
        <h2>Registro guardado!</h2>
        <p>Gracias por completar el formulario.<br>SEGRIMSA se comunicara con usted.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Registrar otro", type="primary"):
        st.session_state.submitted = False
        st.rerun()
    st.stop()


# ========================================
# FORMULARIO
# ========================================
with st.form("registro_catequesis", clear_on_submit=True):

    st.markdown('<div class="section-title">Datos del Padre o Madre</div>', unsafe_allow_html=True)
    
    nombre_padre = st.text_input(
        "Nombre completo del padre/madre *",
        placeholder="Ej: Maria Lopez Garcia"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        telefono = st.text_input("Telefono celular *", placeholder="987654321", max_chars=12)
    with col2:
        email = st.text_input("Correo electronico", placeholder="correo@gmail.com")

    st.markdown('<div class="section-title">Datos del Nino(a)</div>', unsafe_allow_html=True)
    
    nombre_nino = st.text_input(
        "Nombre completo del nino(a) *",
        placeholder="Ej: Jose Lopez Perez"
    )
    
    colegio = st.text_input("Colegio *", placeholder="Ej: Hans Christian Andersen")
    
    col1, col2 = st.columns(2)
    with col1:
        grado = st.selectbox("Grado *", [
            "", "1ro Primaria", "2do Primaria", "3ro Primaria", "4to Primaria",
            "5to Primaria", "6to Primaria",
            "1ro Secundaria", "2do Secundaria", "3ro Secundaria", 
            "4to Secundaria", "5to Secundaria",
        ])
    with col2:
        seccion = st.text_input("Seccion", placeholder="A, B, C...", max_chars=5)

    st.markdown('<div class="section-title">Tiene otro hijo(a) en el colegio?</div>', unsafe_allow_html=True)
    
    tiene_hermano = st.radio(
        "Otro hijo(a)?",
        ["No", "Si, 1 mas", "Si, 2 mas"],
        horizontal=True,
        label_visibility="collapsed"
    )

    hermano1_nombre = hermano1_colegio = hermano1_grado = None
    hermano2_nombre = hermano2_colegio = hermano2_grado = None

    if tiene_hermano != "No":
        st.markdown("**Hermano(a) 1:**")
        hermano1_nombre = st.text_input("Nombre del hermano(a) 1", key="h1n")
        col1, col2 = st.columns(2)
        with col1:
            hermano1_colegio = st.text_input("Colegio", key="h1c")
        with col2:
            hermano1_grado = st.text_input("Grado y seccion", key="h1g")

    if tiene_hermano == "Si, 2 mas":
        st.markdown("**Hermano(a) 2:**")
        hermano2_nombre = st.text_input("Nombre del hermano(a) 2", key="h2n")
        col1, col2 = st.columns(2)
        with col1:
            hermano2_colegio = st.text_input("Colegio", key="h2c")
        with col2:
            hermano2_grado = st.text_input("Grado y seccion", key="h2g")

    st.markdown("")
    submitted = st.form_submit_button("Enviar Registro", type="primary")

    if submitted:
        errores = []
        if not nombre_padre.strip():
            errores.append("Nombre del padre/madre")
        if not telefono.strip() or len(telefono.strip()) < 7:
            errores.append("Telefono valido")
        if not nombre_nino.strip():
            errores.append("Nombre del nino(a)")
        if not colegio.strip():
            errores.append("Colegio")
        if not grado:
            errores.append("Grado")

        if errores:
            st.error(f"Por favor complete: {', '.join(errores)}")
        else:
            grado_completo = f"{grado} {seccion}".strip()
            data = {
                "nombre_padre": nombre_padre.strip().title(),
                "telefono": telefono.strip(),
                "email": email.strip().lower() if email else "",
                "nombre_nino": nombre_nino.strip().title(),
                "colegio": colegio.strip().title(),
                "grado": grado_completo,
                "tiene_hermano": 1 if tiene_hermano != "No" else 0,
                "hermano1_nombre": (hermano1_nombre or "").strip().title() or None,
                "hermano1_colegio": (hermano1_colegio or "").strip().title() or None,
                "hermano1_grado": (hermano1_grado or "").strip() or None,
                "hermano2_nombre": (hermano2_nombre or "").strip().title() or None,
                "hermano2_colegio": (hermano2_colegio or "").strip().title() or None,
                "hermano2_grado": (hermano2_grado or "").strip() or None,
            }
            try:
                guardar_registro(data)
                st.session_state.submitted = True
                st.rerun()
            except Exception as e:
                st.error(f"Error guardando: {e}")


# ========================================
# FOOTER + ADMIN
# ========================================
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("SEGRIMSA 2026", type="secondary", use_container_width=True):
        st.session_state["show_admin_login"] = True

if st.session_state.get("show_admin_login") and not st.session_state.get("show_admin"):
    with st.expander("Acceso Administrador", expanded=True):
        admin_pass = st.text_input("Clave admin", type="password")
        if admin_pass == "segrimsa":
            st.session_state["show_admin"] = True
            st.session_state["show_admin_login"] = False
            st.rerun()
        elif admin_pass:
            st.warning("Clave incorrecta")

if st.session_state.get("show_admin"):
    st.markdown("---")
    st.markdown("### Panel de Administrador")
    
    total = contar_registros()
    st.metric("Total registros", total)
    
    df = obtener_registros()
    
    if df.empty:
        st.info("Sin registros todavia")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descargar CSV",
            csv,
            f"registros_segrimsa_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            "text/csv"
        )
        
        st.warning(
            "IMPORTANTE: Descarga el CSV regularmente. "
            "Los datos en Streamlit Cloud se reinician si la app se redespliega."
        )
    
    if st.button("Cerrar panel admin"):
        st.session_state["show_admin"] = False
        st.session_state["show_admin_login"] = False
        st.rerun()
