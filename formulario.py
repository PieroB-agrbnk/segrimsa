"""
SEGRIMSA - Formulario de Registro de Catequesis
Colores y estilo basados en segrimsa.com
"""

import streamlit as st
import requests
from datetime import datetime

# ========================================
# SUPABASE CONFIG
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
# CSS - Colores SEGRIMSA
# ========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Reset Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] { display: none; }
    .block-container { padding-top: 0 !important; }

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .main > div {
        padding: 0;
        max-width: 520px;
        margin: 0 auto;
    }

    .main .block-container {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* ===== HEADER ===== */
    .hero {
        background: #3EC1D3;
        padding: 36px 24px 28px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -40%; right: -20%;
        width: 300px; height: 300px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -30%; left: -15%;
        width: 250px; height: 250px;
        background: rgba(255,255,255,0.04);
        border-radius: 50%;
    }
    .hero-logo {
        position: relative;
        z-index: 1;
    }
    .hero-logo h1 {
        font-family: 'Poppins', sans-serif !important;
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    .hero-logo .sub {
        color: rgba(255,255,255,0.75);
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 400;
        margin-top: 2px;
    }
    .hero-divider {
        width: 50px;
        height: 2px;
        background: rgba(255,255,255,0.35);
        margin: 16px auto 0;
    }
    .hero-title {
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 400;
        margin-top: 14px;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }

    /* ===== FORM BODY ===== */
    .form-wrap {
        background: #ffffff;
        padding: 4px 20px 20px;
        margin: 0;
    }

    /* Section labels */
    .sec {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 24px 0 14px;
        padding-bottom: 10px;
        border-bottom: 2px solid #3EC1D3;
    }
    .sec-dot {
        width: 30px;
        height: 30px;
        border-radius: 8px;
        background: #3EC1D3;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    .sec-txt {
        font-size: 0.9rem;
        font-weight: 600;
        color: #2d3748;
        letter-spacing: 0.3px;
    }

    /* ===== INPUT STYLING ===== */
    .stTextInput > div > div > input {
        font-family: 'Poppins', sans-serif !important;
        font-size: 16px !important;
        padding: 13px 16px !important;
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #f7fafc !important;
        color: #2d3748 !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3EC1D3 !important;
        background: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(62,193,211,0.15) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #a0aec0 !important;
        font-weight: 300 !important;
    }

    /* Labels */
    .stTextInput label, .stSelectbox label, .stRadio label {
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        color: #4a5568 !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #f7fafc !important;
    }
    .stSelectbox > div > div:focus-within {
        border-color: #3EC1D3 !important;
        box-shadow: 0 0 0 3px rgba(62,193,211,0.15) !important;
    }

    /* Radio */
    .stRadio [role="radiogroup"] {
        gap: 8px !important;
    }

    /* ===== SUBMIT BUTTON ===== */
    .stFormSubmitButton > button {
        font-family: 'Poppins', sans-serif !important;
        width: 100%;
        padding: 15px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        border-radius: 50px !important;
        background: #3EC1D3 !important;
        color: white !important;
        border: none !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        margin-top: 8px !important;
    }
    .stFormSubmitButton > button:hover {
        background: #35aebf !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(62,193,211,0.35) !important;
    }
    .stFormSubmitButton > button:active {
        transform: translateY(0) !important;
    }

    /* ===== SUCCESS ===== */
    .ok-card {
        text-align: center;
        padding: 48px 24px;
        background: #ffffff;
    }
    .ok-circle {
        width: 72px; height: 72px;
        border-radius: 50%;
        background: #3EC1D3;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 20px;
        font-size: 2.2rem;
        color: white;
    }
    .ok-card h2 {
        font-family: 'Poppins', sans-serif !important;
        color: #2d3748;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .ok-card p {
        color: #718096;
        font-size: 0.88rem;
        line-height: 1.7;
    }

    /* Otro registro button */
    .stButton > button[kind="primary"] {
        font-family: 'Poppins', sans-serif !important;
        width: 100%;
        padding: 14px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        background: #3EC1D3 !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #35aebf !important;
    }

    /* ===== FOOTER ===== */
    .foot {
        background: #3EC1D3;
        text-align: center;
        padding: 20px 24px 16px;
        margin: 0;
    }
    .foot p {
        color: rgba(255,255,255,0.7);
        font-size: 0.68rem;
        letter-spacing: 1px;
        margin: 0;
        font-weight: 400;
    }
    .foot .brand {
        color: white;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }

    /* Hide form border */
    .stForm { border: none !important; padding: 0 !important; }
    
    /* Error messages */
    .stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ========================================
# FUNCIONES
# ========================================
def guardar_registro(data):
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
<div class="hero">
    <div class="hero-logo">
        <h1>Segrimsa</h1>
        <div class="sub">FOTOGRAFIA & IMPRENTA</div>
    </div>
    <div class="hero-divider"></div>
    <div class="hero-title">Registro de Catequesis</div>
</div>
""", unsafe_allow_html=True)


# ========================================
# EXITO
# ========================================
if st.session_state.submitted:
    st.markdown("""
    <div class="ok-card">
        <div class="ok-circle">&#10003;</div>
        <h2>Registro completado</h2>
        <p>Gracias por registrar a su hijo(a).<br>
        Nos comunicaremos con usted para<br>
        coordinar los detalles del sacramento.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Registrar otro hijo(a)", type="primary"):
        st.session_state.submitted = False
        st.rerun()

    st.markdown("""
    <div class="foot">
        <p class="brand">SEGRIMSA</p>
        <p>Creamos experiencias visuales que trascienden el tiempo</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ========================================
# FORMULARIO
# ========================================
st.markdown('<div class="form-wrap">', unsafe_allow_html=True)

with st.form("registro_catequesis", clear_on_submit=True):

    # Seccion 1
    st.markdown("""
    <div class="sec">
        <div class="sec-dot">1</div>
        <div class="sec-txt">Datos del padre o madre</div>
    </div>
    """, unsafe_allow_html=True)
    
    nombre_padre = st.text_input(
        "Nombre completo *",
        placeholder="Ej: Maria Lopez Garcia"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        telefono = st.text_input("Celular *", placeholder="987 654 321", max_chars=12)
    with col2:
        email = st.text_input("Correo electronico *", placeholder="correo@gmail.com")

    # Seccion 2
    st.markdown("""
    <div class="sec">
        <div class="sec-dot">2</div>
        <div class="sec-txt">Datos del nino o nina</div>
    </div>
    """, unsafe_allow_html=True)
    
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

    # Seccion 3
    st.markdown("""
    <div class="sec">
        <div class="sec-dot">3</div>
        <div class="sec-txt">Hermanos en el colegio</div>
    </div>
    """, unsafe_allow_html=True)
    
    tiene_hermano = st.radio(
        "Tiene otro hijo(a) en algun colegio?",
        ["No", "Si, 1 mas", "Si, 2 mas"],
        horizontal=True,
    )

    hermano1_nombre = hermano1_colegio = hermano1_grado = ""
    hermano2_nombre = hermano2_colegio = hermano2_grado = ""

    grados_lista = [
        "", "1ro Primaria", "2do Primaria", "3ro Primaria", "4to Primaria",
        "5to Primaria", "6to Primaria",
        "1ro Secundaria", "2do Secundaria", "3ro Secundaria",
        "4to Secundaria", "5to Secundaria",
    ]

    if tiene_hermano != "No":
        hermano1_nombre = st.text_input("Nombre del hermano(a)", key="h1n")
        hermano1_colegio = st.text_input("Colegio", key="h1c")
        col1, col2 = st.columns(2)
        with col1:
            hermano1_grado_sel = st.selectbox("Grado", grados_lista, key="h1g")
        with col2:
            hermano1_seccion = st.text_input("Seccion", key="h1s", max_chars=5, placeholder="A, B, C...")
        hermano1_grado = f"{hermano1_grado_sel} {hermano1_seccion}".strip()

    if tiene_hermano == "Si, 2 mas":
        hermano2_nombre = st.text_input("Nombre del 2do hermano(a)", key="h2n")
        hermano2_colegio = st.text_input("Colegio", key="h2c")
        col1, col2 = st.columns(2)
        with col1:
            hermano2_grado_sel = st.selectbox("Grado", grados_lista, key="h2g")
        with col2:
            hermano2_seccion = st.text_input("Seccion", key="h2s", max_chars=5, placeholder="A, B, C...")
        hermano2_grado = f"{hermano2_grado_sel} {hermano2_seccion}".strip()

    # Submit
    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Enviar registro")

    if submitted:
        errores = []
        if not nombre_padre.strip():
            errores.append("Nombre del padre/madre")
        if not telefono.strip() or len(telefono.strip()) < 7:
            errores.append("Telefono valido")
        if not email.strip() or "@" not in email:
            errores.append("Correo electronico")
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

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="foot">
    <p class="brand">SEGRIMSA</p>
    <p>Creamos experiencias visuales que trascienden el tiempo</p>
</div>
""", unsafe_allow_html=True)
