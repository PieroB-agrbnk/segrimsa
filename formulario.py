"""
SEGRIMSA - Formulario de Registro de Catequesis
Datos van directo a Supabase (PostgreSQL)
"""

import streamlit as st
import requests
from datetime import datetime

# ========================================
# SUPABASE CONFIG (from Streamlit secrets)
# ========================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}

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
# FUNCIONES
# ========================================
def guardar_registro(data):
    """Guarda registro en Supabase via REST API."""
    url = f"{SUPABASE_URL}/rest/v1/registros_catequesis"
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code in (200, 201):
        return True
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return False


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
# EXITO
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

    hermano1_nombre = hermano1_colegio = hermano1_grado = ""
    hermano2_nombre = hermano2_colegio = hermano2_grado = ""

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
                "hermano1_nombre": hermano1_nombre.strip().title() if hermano1_nombre else None,
                "hermano1_colegio": hermano1_colegio.strip().title() if hermano1_colegio else None,
                "hermano1_grado": hermano1_grado.strip() if hermano1_grado else None,
                "hermano2_nombre": hermano2_nombre.strip().title() if hermano2_nombre else None,
                "hermano2_colegio": hermano2_colegio.strip().title() if hermano2_colegio else None,
                "hermano2_grado": hermano2_grado.strip() if hermano2_grado else None,
                "evento": "Primera Comunion 2026",
                "sacramento": "Primera Comunion",
                "anio": 2026,
            }
            
            if guardar_registro(data):
                st.session_state.submitted = True
                st.rerun()


# ========================================
# FOOTER LIMPIO
# ========================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#999; font-size:0.75rem;'>"
    "SEGRIMSA 2026"
    "</div>",
    unsafe_allow_html=True,
)
