"""
SEGRIMSA - Formulario de Registro de Catequesis
Supabase + Colores SEGRIMSA + Lista colegios Lima
SIN st.form para que los radio buttons funcionen dinamicamente
"""

import streamlit as st
import requests
import re
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
# COLEGIOS DE LIMA
# ========================================
COLEGIOS_LIMA = [
    "",
    # --- Surco ---
    "Hans Christian Andersen",
    "Peruano Britanico",
    "Markham College",
    "Franco Peruano",
    "Alpamayo",
    "Santa Maria Marianistas",
    "SS.CC. Recoleta",
    "San Pedro",
    "Santa Teresita",
    "Los Alamos",
    "Maria Reina Marianistas",
    "San Jose de Monterrico",
    "Hiram Bingham",
    "Maria Reina",
    "Inmaculada Concepcion Monterrico",
    "La Casa de Carton",
    "Santisimo Nombre de Jesus",
    "Waldorf Lima",
    "Casuarinas College",
    "Sophianum",
    "Villa Caritas",
    "Villa Maria La Planicie",
    "San Ignacio de Loyola",
    "De Jesus",
    "Pamer Surco",
    "Trilce Surco",
    "Saco Oliveros Surco",
    # --- San Borja ---
    "San Ignacio de Recalde",
    "De La Inmaculada",
    "Alexander von Humboldt",
    "Salcantay",
    "San Luis Gonzaga",
    "Santa Rosa de Lima",
    # --- Miraflores ---
    "Pestalozzi",
    "San Silvestre School",
    "Reina del Mundo",
    "International Christian School",
    "Liceo Naval Almirante Guise",
    "Santa Ursula",
    "Max Uhle",
    "Raimondi",
    "Canonesas de la Cruz",
    "Maria Auxiliadora Miraflores",
    # --- San Isidro ---
    "Inmaculado Corazon",
    "San Agustin",
    "Santa Maria de la Providencia",
    # --- La Molina ---
    "Franklin Delano Roosevelt",
    "Newton College",
    "Villa Maria Academy",
    "La Molina Christian Schools",
    "Colegio de la Inmaculada",
    "SS.CC. Santa Maria",
    "Cambridge College Lima",
    "Trener",
    "Los Reyes Rojos",
    "San Jose Obrero",
    "Pamer La Molina",
    "Trilce La Molina",
    # --- Barranco ---
    "Inmaculado High School",
    "Hospicio de Barranco",
    "San Vicente de Paul Barranco",
    # --- Chorrillos ---
    "Villa Maria del Triunfo",
    "Santa Rosa de Chorrillos",
    "Militar Leoncio Prado",
    # --- Magdalena ---
    "Jose Antonio Encinas",
    "Bartolome Herrera",
    "San Felipe",
    "Maria Auxiliadora Magdalena",
    # --- San Miguel ---
    "Claretiano",
    "Cristo Salvador",
    "San Jose Hermanos Maristas",
    "Nuestra Senora de la Merced",
    "San Antonio de Padua",
    # --- Pueblo Libre ---
    "Nuestra Senora del Carmen",
    "Maria Inmaculada",
    "Concordia",
    "Rosa de Santa Maria",
    # --- Jesus Maria ---
    "Belisario Suarez",
    "San Jose de Cluny",
    "La Salle",
    "Sagrado Corazon Sophianum",
    # --- Lince ---
    "Jose Galvez",
    "San Marcos Lince",
    # --- Surquillo ---
    "Maria Auxiliadora Surquillo",
    "Enrique Meiggs",
    # --- Ate ---
    "Trilce Ate",
    "Pamer Ate",
    "La Merced de Ate",
    "Santa Maria de la Gracia",
    # --- La Victoria ---
    "Isabel la Catolica",
    "Maria Parado de Bellido",
    # --- Comas / Independencia / Los Olivos ---
    "San Felipe Neri",
    "Santo Domingo de Guzman",
    "Trilce Los Olivos",
    "Saco Oliveros Los Olivos",
    # --- San Juan de Lurigancho ---
    "Fe y Alegria 5",
    "Fe y Alegria 25",
    "Trilce SJL",
    "San Marcos SJL",
    # --- Callao / Bellavista ---
    "Parroquial de la Luz",
    "San Jose Callao",
    "America Callao",
    # --- Generales Lima ---
    "Fe y Alegria",
    "Innova Schools",
    "Colegios Pamer",
    "Colegios Trilce",
    "Saco Oliveros",
    "Maria Auxiliadora",
    "Santa Maria",
    "San Martin de Porres",
    "Sagrados Corazones",
    "San Juan Apostol",
    "San Judas Tadeo",
    "Nuestra Senora de Fatima",
    "Nuestra Senora de Guadalupe",
    "San Jose",
    "San Francisco de Asis",
    "Champagnat",
    "Divino Maestro",
    "Sagrado Corazon",
    "Cristo Rey",
    "Lord Byron",
    "Abraham Lincoln",
    "Bertolt Brecht",
    "Andre Malraux",
    "Antonio Raimondi",
    "Jean Le Boulch",
    "Nuestra Senora del Pilar",
    "San Columbano",
    "Santo Tomas de Aquino",
    "Santa Ana",
    "OTRO (escribir abajo)",
]

GRADOS = [
    "", "Kinder", "1ro Primaria", "2do Primaria", "3ro Primaria", "4to Primaria",
    "5to Primaria", "6to Primaria",
    "1ro Secundaria", "2do Secundaria", "3ro Secundaria",
    "4to Secundaria", "5to Secundaria",
]

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
# CSS
# ========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] { display: none; }
    .block-container { padding-top: 0 !important; }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .main > div {
        padding: 0;
        max-width: 520px;
        margin: 0 auto;
    }

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
    .hero h1 {
        font-family: 'Poppins', sans-serif !important;
        color: #ffffff; font-size: 2.2rem; font-weight: 700;
        letter-spacing: 1px; margin: 0; position: relative; z-index: 1;
    }
    .hero .sub {
        color: rgba(255,255,255,0.75); font-size: 0.7rem;
        letter-spacing: 3px; text-transform: uppercase;
        font-weight: 400; margin-top: 2px; position: relative; z-index: 1;
    }
    .hero-divider {
        width: 50px; height: 2px; background: rgba(255,255,255,0.35);
        margin: 16px auto 0; position: relative; z-index: 1;
    }
    .hero-title {
        color: #fff; font-size: 0.9rem; font-weight: 400;
        margin-top: 14px; position: relative; z-index: 1;
    }

    .sec {
        display: flex; align-items: center; gap: 12px;
        margin: 24px 0 14px; padding-bottom: 10px;
        border-bottom: 2px solid #3EC1D3;
    }
    .sec-dot {
        width: 30px; height: 30px; border-radius: 8px;
        background: #3EC1D3; color: white;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.8rem; font-weight: 700; flex-shrink: 0;
    }
    .sec-txt { font-size: 0.9rem; font-weight: 600; color: #2d3748; }

    .stTextInput > div > div > input {
        font-family: 'Poppins', sans-serif !important;
        font-size: 16px !important;
        padding: 13px 16px !important;
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #f7fafc !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3EC1D3 !important;
        background: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(62,193,211,0.15) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #a0aec0 !important; font-weight: 300 !important;
    }

    .stTextInput label, .stSelectbox label, .stRadio label {
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.8rem !important; font-weight: 500 !important;
        color: #4a5568 !important;
    }

    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #f7fafc !important;
    }
    .stSelectbox > div > div:focus-within {
        border-color: #3EC1D3 !important;
        box-shadow: 0 0 0 3px rgba(62,193,211,0.15) !important;
    }

    .stButton > button {
        font-family: 'Poppins', sans-serif !important;
        width: 100%; padding: 15px !important;
        font-size: 0.95rem !important; font-weight: 600 !important;
        letter-spacing: 1px !important;
        border-radius: 50px !important;
        background: #3EC1D3 !important;
        color: white !important; border: none !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        margin-top: 8px !important;
    }
    .stButton > button:hover {
        background: #35aebf !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(62,193,211,0.35) !important;
    }

    .ok-card {
        text-align: center; padding: 48px 24px; background: #ffffff;
    }
    .ok-circle {
        width: 72px; height: 72px; border-radius: 50%;
        background: #3EC1D3;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 20px; font-size: 2.2rem; color: white;
    }
    .ok-card h2 {
        font-family: 'Poppins', sans-serif !important;
        color: #2d3748; font-size: 1.4rem; font-weight: 600; margin-bottom: 8px;
    }
    .ok-card p { color: #718096; font-size: 0.88rem; line-height: 1.7; }

    .foot {
        background: #3EC1D3; text-align: center; padding: 20px 24px 16px;
    }
    .foot .brand { color: white; font-weight: 600; font-size: 0.85rem; letter-spacing: 1.5px; margin-bottom: 4px; }
    .foot p { color: rgba(255,255,255,0.7); font-size: 0.68rem; letter-spacing: 1px; margin: 0; }

    .stAlert { border-radius: 10px !important; }

    /* Hermano card */
    .hermano-card {
        background: #f0fafb;
        border: 1px solid #d4eff2;
        border-radius: 10px;
        padding: 12px 16px 4px;
        margin-bottom: 12px;
    }
    .hermano-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
    }

    /* Error inline debajo de cada campo */
    .field-error {
        color: #e53e3e;
        font-size: 0.72rem;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 8px;
        padding-left: 4px;
    }
</style>
""", unsafe_allow_html=True)


# ========================================
# FUNCIONES
# ========================================
def guardar_registro(data):
    url = f"{SUPABASE_URL}/rest/v1/registros_catequesis"
    response = requests.post(url, json=data, headers=HEADERS)
    return response.status_code in (200, 201)


def limpiar_telefono(tel):
    """Extrae solo digitos del telefono."""
    return re.sub(r'\D', '', tel)


# ========================================
# INICIALIZAR SESSION STATE
# ========================================
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "errores_campo" not in st.session_state:
    st.session_state.errores_campo = {}


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
    <div class="hero-title">Registro</div>
</div>
""", unsafe_allow_html=True)


# ========================================
# PANTALLA DE EXITO
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
        # Limpiar todo el session_state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.submitted = False
        st.session_state.errores_campo = {}
        st.rerun()
    st.markdown("""
    <div class="foot">
        <p class="brand">SEGRIMSA</p>
        <p>Creamos experiencias visuales que trascienden el tiempo</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ========================================
# HELPER: mostrar error inline
# ========================================
errores = st.session_state.errores_campo

def mostrar_error(campo):
    if campo in errores:
        st.markdown(f'<div class="field-error">⚠️ {errores[campo]}</div>', unsafe_allow_html=True)


# ========================================
# FORMULARIO (widgets libres, sin st.form)
# ========================================

# --- Seccion 1: Padre/Madre ---
st.markdown("""
<div class="sec">
    <div class="sec-dot">1</div>
    <div class="sec-txt">Datos del padre o madre</div>
</div>
""", unsafe_allow_html=True)

nombre_padre = st.text_input("Nombre completo *", placeholder="Ej: Maria Lopez Garcia", key="nombre_padre")
mostrar_error("nombre_padre")

col1, col2 = st.columns(2)
with col1:
    telefono = st.text_input("Celular (9 digitos) *", placeholder="987654321", max_chars=9, key="telefono")
    mostrar_error("telefono")
with col2:
    email = st.text_input("Correo electronico *", placeholder="correo@gmail.com", key="email")
    mostrar_error("email")

# --- Seccion 2: Nino ---
st.markdown("""
<div class="sec">
    <div class="sec-dot">2</div>
    <div class="sec-txt">Datos del niño o niña</div>
</div>
""", unsafe_allow_html=True)

nombre_nino = st.text_input("Nombre completo del nino(a) *", placeholder="Ej: Jose Lopez Perez", key="nombre_nino")
mostrar_error("nombre_nino")

colegio_sel = st.selectbox("Colegio *", COLEGIOS_LIMA, key="colegio_sel")
mostrar_error("colegio")

colegio_otro = ""
if colegio_sel == "OTRO (escribir abajo)":
    colegio_otro = st.text_input("Escriba el nombre del colegio *", placeholder="Nombre del colegio", key="colegio_otro")
    mostrar_error("colegio_otro")

col1, col2 = st.columns(2)
with col1:
    grado = st.selectbox("Grado *", GRADOS, key="grado")
    mostrar_error("grado")
with col2:
    seccion = st.text_input("Seccion", placeholder="A, B, C...", max_chars=5, key="seccion")


# --- Seccion 3: Hermanos ---
st.markdown("""
<div class="sec">
    <div class="sec-dot">3</div>
    <div class="sec-txt">Hermanos en el colegio</div>
</div>
""", unsafe_allow_html=True)

tiene_hermano = st.radio(
    "Tiene otro hijo(a) en algun colegio?",
    ["No", "Si"],
    horizontal=True,
    key="tiene_hermano",
)

# Variables por defecto
hermano1_nombre = hermano1_colegio = hermano1_grado = ""
hermano2_nombre = hermano2_colegio = hermano2_grado = ""

if tiene_hermano == "Si":
    # --- Hermano 1 ---
    st.markdown('<div class="hermano-card"><div class="hermano-title">👦 Hermano(a) 1</div>', unsafe_allow_html=True)
    hermano1_nombre = st.text_input("Nombre completo", key="h1n", placeholder="Nombre del hermano(a)")
    hermano1_colegio_sel = st.selectbox("Colegio", COLEGIOS_LIMA, key="h1c")
    if hermano1_colegio_sel == "OTRO (escribir abajo)":
        h1_colegio_otro = st.text_input("Nombre del colegio", key="h1co")
        hermano1_colegio = h1_colegio_otro
    else:
        hermano1_colegio = hermano1_colegio_sel
    col1, col2 = st.columns(2)
    with col1:
        h1_grado_sel = st.selectbox("Grado", GRADOS, key="h1g")
    with col2:
        h1_seccion = st.text_input("Seccion", key="h1s", max_chars=5, placeholder="A, B...")
    hermano1_grado = f"{h1_grado_sel} {h1_seccion}".strip()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Pregunta: otro hermano mas? ---
    tiene_hermano2 = st.radio(
        "Tiene otro hermano(a) adicional?",
        ["No", "Si"],
        horizontal=True,
        key="tiene_hermano2",
    )

    # --- Hermano 2 ---
    if tiene_hermano2 == "Si":
        st.markdown('<div class="hermano-card"><div class="hermano-title">👧 Hermano(a) 2</div>', unsafe_allow_html=True)
        hermano2_nombre = st.text_input("Nombre completo", key="h2n", placeholder="Nombre del hermano(a)")
        hermano2_colegio_sel = st.selectbox("Colegio", COLEGIOS_LIMA, key="h2c")
        if hermano2_colegio_sel == "OTRO (escribir abajo)":
            h2_colegio_otro = st.text_input("Nombre del colegio", key="h2co")
            hermano2_colegio = h2_colegio_otro
        else:
            hermano2_colegio = hermano2_colegio_sel
        col1, col2 = st.columns(2)
        with col1:
            h2_grado_sel = st.selectbox("Grado", GRADOS, key="h2g")
        with col2:
            h2_seccion = st.text_input("Seccion", key="h2s", max_chars=5, placeholder="A, B...")
        hermano2_grado = f"{h2_grado_sel} {h2_seccion}".strip()
        st.markdown('</div>', unsafe_allow_html=True)


# --- Espaciado ---
st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)


# ========================================
# BOTON ENVIAR
# ========================================
if st.button("ENVIAR REGISTRO", type="primary", use_container_width=True):
    # Determinar colegio
    colegio_final = colegio_otro.strip() if colegio_sel == "OTRO (escribir abajo)" else colegio_sel

    # --- Validacion especifica por campo ---
    nuevos_errores = {}

    # Nombre padre
    if not nombre_padre.strip():
        nuevos_errores["nombre_padre"] = "Ingrese el nombre del padre o madre"

    # Telefono
    tel_limpio = limpiar_telefono(telefono)
    if not tel_limpio:
        nuevos_errores["telefono"] = "Ingrese su numero de celular"
    elif len(tel_limpio) != 9:
        nuevos_errores["telefono"] = f"El celular debe tener 9 digitos (tiene {len(tel_limpio)})"
    elif not tel_limpio.startswith("9"):
        nuevos_errores["telefono"] = "El celular debe empezar con 9"

    # Email
    email_val = email.strip()
    if not email_val:
        nuevos_errores["email"] = "Ingrese su correo electronico"
    elif "@" not in email_val:
        nuevos_errores["email"] = "Falta el @ en el correo (ej: nombre@gmail.com)"
    elif "." not in email_val.split("@")[-1]:
        nuevos_errores["email"] = "Correo incompleto (ej: nombre@gmail.com)"

    # Nombre nino
    if not nombre_nino.strip():
        nuevos_errores["nombre_nino"] = "Ingrese el nombre del nino(a)"

    # Colegio
    if not colegio_final:
        nuevos_errores["colegio"] = "Seleccione un colegio"
    elif colegio_sel == "OTRO (escribir abajo)" and not colegio_otro.strip():
        nuevos_errores["colegio_otro"] = "Escriba el nombre del colegio"

    # Grado
    if not grado:
        nuevos_errores["grado"] = "Seleccione el grado"

    # Guardar errores y rerun para mostrar inline
    st.session_state.errores_campo = nuevos_errores

    if nuevos_errores:
        # Resumen de errores arriba
        msgs = list(nuevos_errores.values())
        st.error("Por favor corrija lo siguiente:\n" + "\n".join(f"• {m}" for m in msgs))
        st.rerun()  # Rerun para que los errores aparezcan debajo de cada campo
    else:
        # Todo OK - enviar a Supabase
        grado_completo = f"{grado} {seccion}".strip()
        data = {
            "nombre_padre": nombre_padre.strip().title(),
            "telefono": tel_limpio,
            "email": email_val.lower(),
            "nombre_nino": nombre_nino.strip().title(),
            "colegio": colegio_final.strip().title(),
            "grado": grado_completo,
            "tiene_hermano": 1 if tiene_hermano == "Si" else 0,
            "hermano1_nombre": hermano1_nombre.strip().title() if hermano1_nombre else None,
            "hermano1_colegio": hermano1_colegio.strip().title() if hermano1_colegio else None,
            "hermano1_grado": hermano1_grado if hermano1_grado else None,
            "hermano2_nombre": hermano2_nombre.strip().title() if hermano2_nombre else None,
            "hermano2_colegio": hermano2_colegio.strip().title() if hermano2_colegio else None,
            "hermano2_grado": hermano2_grado if hermano2_grado else None,
            "evento": "Primera Comunion 2026",
            "sacramento": "Primera Comunion",
            "anio": 2026,
        }

        if guardar_registro(data):
            st.session_state.submitted = True
            st.session_state.errores_campo = {}
            st.rerun()
        else:
            st.error("Error guardando el registro. Intente de nuevo.")


# Footer
st.markdown("""
<div class="foot">
    <p class="brand">SEGRIMSA</p>
    <p>Creamos experiencias visuales que trascienden el tiempo</p>
</div>
""", unsafe_allow_html=True)
