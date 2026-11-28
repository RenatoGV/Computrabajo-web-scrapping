
import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scraper import buscar_ofertas
from exportar import generar_csv


# ==========================================
# 1. CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="CompuTrabajo | Portal de Empleo",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. ESTILOS VISUALES
# ==========================================

st.markdown("""
<style>

:root {
    --azul: #1473C9;
    --azul-oscuro: #092B52;
    --azul-marino: #102D52;
    --azul-claro: #DCEBFA;
    --fondo: #F1F6FC;
    --blanco: #FFFFFF;
    --texto: #10243D;
    --secundario: #536B88;
    --borde: #BBD3ED;
}

/* Fondo principal */
.stApp {
    background: var(--fondo);
    color: var(--texto);
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1600px;
}

/* Ocultar elementos de Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ==========================================
   3. BARRA LATERAL
========================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #1266B5 0%,
        #0C4789 55%,
        #092B52 100%
    );
    border-right: 1px solid #0A376B;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.8rem;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

/* Identidad de CompuTrabajo */
.marca {
    font-size: 29px;
    font-weight: 900;
    letter-spacing: -1px;
    color: #FFFFFF;
    white-space: nowrap;
}

.marca-subtitulo {
    color: #A9D9FF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-left: 5px;
    margin-top: 5px;
    margin-bottom: 25px;
}

.empty-state {
    background: #FFFFFF;
    border: 1px solid #BBD3ED;
    border-radius: 16px;
    padding: 48px 24px;
    margin: 24px 0;
    text-align: center;
    box-shadow: 0 4px 14px rgba(16,45,82,0.06);
}

.empty-state-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.empty-state-title {
    color: #10243D;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 8px;
}

.empty-state-copy {
    color: #536B88;
    font-size: 15px;
}

/* Campos de búsqueda */
[data-testid="stSidebar"] input {
    background: #FFFFFF !important;
    color: #0D1F35 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] input::placeholder {
    color: #596B80 !important;
    opacity: 1;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #0D1F35 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #0D1F35 !important;
}

/* Botón aplicar filtros */
[data-testid="stSidebar"] .stFormSubmitButton button {
    background: #082F5B !important;
    color: #FFFFFF !important;
    border: 1px solid #65B9FF !important;
    border-radius: 8px !important;
    font-weight: 750 !important;
    min-height: 45px;
}

[data-testid="stSidebar"] .stFormSubmitButton button:hover {
    background: #1473C9 !important;
    border-color: #FFFFFF !important;
}


/* ==========================================
   4. ENCABEZADO PRINCIPAL
========================================== */

.hero-titulo {
    font-size: 36px;
    font-weight: 900;
    color: #102D52;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.hero-linea {
    width: 75px;
    height: 6px;
    background: #16A6E8;
    border-radius: 10px;
    margin-top: 8px;
    margin-bottom: 12px;
}

.hero-descripcion {
    font-size: 16px;
    color: #536B88;
}


/* ==========================================
   5. ESTADÍSTICAS
========================================== */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #BBD3ED;
    border-radius: 13px;
    padding: 18px;
    box-shadow: 0 4px 12px rgba(16,45,82,0.07);
}

[data-testid="stMetricLabel"] {
    color: #536B88;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #102D52;
    font-weight: 850;
}


/* ==========================================
   6. TARJETAS DE OFERTAS
========================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #BBD3ED;
    border-radius: 13px;
    box-shadow: 0 4px 12px rgba(16,45,82,0.07);
}

/* Etiqueta de oferta */
.etiqueta {
    display: inline-block;
    background: #D9EEFF;
    color: #0759A5;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 850;
    margin-bottom: 7px;
}

/* Título de cada oferta */
.titulo-oferta {
    color: #102D52;
    font-size: 21px;
    font-weight: 850;
    line-height: 1.3;
    margin-bottom: 12px;
}

/* Información de empresa y ubicación */
.dato-oferta {
    color: #405873;
    font-size: 14px;
    margin-top: 7px;
}


/* ==========================================
   7. BOTONES
========================================== */

/* Botones principales */
.stButton > button {
    background: #126CC0;
    color: #FFFFFF !important;
    border: 1px solid #126CC0;
    border-radius: 8px;
    font-weight: 750;
    min-height: 40px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #084F94;
    border-color: #084F94;
    color: #FFFFFF !important;
}

/* Descargar CSV: texto legible en los estados habilitado y deshabilitado */
[data-testid="stDownloadButton"] button {
    background: #126CC0 !important;
    color: #FFFFFF !important;
    border: 1px solid #126CC0 !important;
    border-radius: 8px !important;
    font-weight: 750 !important;
    min-height: 40px;
}

[data-testid="stDownloadButton"] button * {
    color: #FFFFFF !important;
}

[data-testid="stDownloadButton"] button:hover:not(:disabled) {
    background: #084F94 !important;
    border-color: #084F94 !important;
}

[data-testid="stDownloadButton"] button:disabled {
    background: #DCE4EE !important;
    color: #34465C !important;
    border-color: #AEBCCC !important;
    opacity: 1 !important;
    cursor: not-allowed;
}

[data-testid="stDownloadButton"] button:disabled * {
    color: #34465C !important;
}

/* Enlaces externos */
.stLinkButton > a {
    background: #FFFFFF;
    color: #0759A5 !important;
    border: 1.5px solid #1473C9;
    border-radius: 8px;
    font-weight: 750;
    min-height: 40px;
    transition: 0.2s;
}

.stLinkButton > a:hover {
    background: #E2F0FF;
    color: #084F94 !important;
}


/* ==========================================
   8. SEPARADORES Y PIE DE PÁGINA
========================================== */

hr {
    border-color: #C5D8EC;
}

.pie-pagina {
    color: #6B7F98;
    font-size: 12px;
    text-align: center;
    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 9. CONFIGURAR DEPARTAMENTOS Y NORMALIZACIÓN
# ==========================================

DEPARTAMENTOS_PERU = [
    "Amazonas",
    "Áncash",
    "Apurímac",
    "Arequipa",
    "Ayacucho",
    "Cajamarca",
    "Callao",
    "Cusco",
    "Huancavelica",
    "Huánuco",
    "Ica",
    "Junín",
    "La Libertad",
    "Lambayeque",
    "Lima",
    "Loreto",
    "Madre de Dios",
    "Moquegua",
    "Pasco",
    "Piura",
    "Puno",
    "San Martín",
    "Tacna",
    "Tumbes",
    "Ucayali",
]


# ==========================================
# 10. ESTADO DE LA APLICACIÓN
# ==========================================

if "oferta_seleccionada" not in st.session_state:
    st.session_state.oferta_seleccionada = None

if "ofertas" not in st.session_state:
    st.session_state.ofertas = []

if "busqueda_realizada" not in st.session_state:
    st.session_state.busqueda_realizada = False

if "error_busqueda" not in st.session_state:
    st.session_state.error_busqueda = None

if "filtros_aplicados" not in st.session_state:
    st.session_state.filtros_aplicados = {
        "palabra": "",
        "ubicacion": "Todos",
        "modalidad": "Todas"
    }

st.session_state.filtros_aplicados.setdefault("modalidad", "Todas")
st.session_state.filtros_aplicados.pop("empresa", None)
if st.session_state.filtros_aplicados.get("ubicacion") == "Todas":
    st.session_state.filtros_aplicados["ubicacion"] = "Todos"


# ==========================================
# 11. BARRA LATERAL Y FILTROS
# ==========================================

st.sidebar.markdown("""
<div class="marca">💼 CompuTrabajo</div>
<div class="marca-subtitulo">PORTAL DE EMPLEO</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.subheader("⚙️ Filtros de búsqueda")


# Formulario de filtros

with st.sidebar.form("form_filtros"):

    palabra = st.text_input(
        "Puesto o palabra clave",
        placeholder="Ejemplo: Java, analista..."
    )

    ubicacion = st.selectbox(
        "Departamento",
        ["Todos"] + DEPARTAMENTOS_PERU
    )

    modalidad = st.selectbox(
        "Modalidad",
        ["Todas", "Presencial", "Remoto", "Híbrido"]
    )

    buscar = st.form_submit_button(
        "🔎 Buscar ofertas",
        use_container_width=True
    )

    if buscar:

        st.session_state.filtros_aplicados = {
            "palabra": palabra,
            "ubicacion": ubicacion,
            "modalidad": modalidad
        }
        st.session_state.oferta_seleccionada = None
        st.session_state.busqueda_realizada = True
        st.session_state.error_busqueda = None

if buscar:
    filtros = st.session_state.filtros_aplicados
    ubicacion_busqueda = "" if filtros["ubicacion"] == "Todos" else filtros["ubicacion"]
    modalidad_busqueda = "" if filtros["modalidad"] == "Todas" else filtros["modalidad"]
    if modalidad_busqueda == "Híbrido":
        modalidad_busqueda = "hibrido"

    try:
        with st.spinner("Buscando ofertas en Computrabajo..."):
            st.session_state.ofertas = buscar_ofertas(
                puesto=filtros["palabra"] or "software",
                ubicacion=ubicacion_busqueda,
                modalidad=modalidad_busqueda,
            )
    except Exception as error:
        st.session_state.ofertas = []
        st.session_state.error_busqueda = str(error)


# ==========================================
# 12. OBTENER RESULTADOS
# ==========================================

ofertas = st.session_state.ofertas
resultados = list(ofertas)

# ==========================================
# 13. ENCABEZADO PRINCIPAL
# ==========================================

st.markdown("""
<div class="hero-titulo">
    Encuentra tu próxima oportunidad
</div>

<div class="hero-linea"></div>

<div class="hero-descripcion">
    Explora ofertas laborales del sector tecnológico y de software.
</div>
""", unsafe_allow_html=True)

st.write("")


# ==========================================
# 14. ESTADÍSTICAS
# ==========================================

total_resultados = len(resultados)

total_empresas = len(set(
    x.get("empresa", "").strip()
    for x in ofertas
    if x.get("empresa", "").strip()
))

total_modalidades = len(set(
    x.get("modalidad", "").strip()
    for x in ofertas
    if x.get("modalidad", "").strip()
))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💼 Ofertas encontradas",
        total_resultados
    )

with col2:
    st.metric(
        "🏢 Empresas encontradas",
        total_empresas
    )

with col3:
    st.metric(
        "🏠 Modalidades encontradas",
        total_modalidades
    )


st.write("")
st.divider()


# ==========================================
# 15. LISTADO DE OFERTAS
# ==========================================

col_titulo, col_exportar = st.columns([4, 1])
with col_titulo:
    st.subheader("💼 Ofertas laborales disponibles")
    st.caption(f"Se encontraron {total_resultados} oportunidades.")

with col_exportar:
    st.download_button(
        "⬇️ Exportar CSV",
        data=generar_csv(resultados),
        file_name="ofertas.csv",
        mime="text/csv",
        disabled=not st.session_state.busqueda_realizada,
        use_container_width=True,
        key="exportar_ofertas_csv",
    )


if st.session_state.error_busqueda:
    st.error(f"No se pudo completar la búsqueda: {st.session_state.error_busqueda}")

if not st.session_state.busqueda_realizada:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🔎</div>
        <div class="empty-state-title">Encuentra ofertas para ti</div>
        <div class="empty-state-copy">
            Elige puesto, departamento y modalidad; luego pulsa “Buscar ofertas”.
        </div>
    </div>
    """, unsafe_allow_html=True)

elif resultados:

    for i, oferta in enumerate(resultados):

        puesto = oferta.get("puesto", "Sin título")
        empresa = oferta.get("empresa", "No especificada")
        ubicacion = oferta.get("ubicacion", "No especificada")
        url = oferta.get("url", "")

        # Tarjeta de oferta

        with st.container(border=True):

            st.markdown(
                '<div class="etiqueta">OFERTA LABORAL</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="titulo-oferta">{puesto}</div>',
                unsafe_allow_html=True
            )

            col_info1, col_info2 = st.columns(2)

            with col_info1:

                st.markdown(
                    f'<div class="dato-oferta">'
                    f'🏢 <b>Empresa:</b> {empresa}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with col_info2:

                st.markdown(
                    f'<div class="dato-oferta">'
                    f'📍 <b>Ubicación:</b> {ubicacion}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            b1, b2, espacio = st.columns([1, 1.7, 5])

            seleccionada = (
                st.session_state.oferta_seleccionada == i
            )

            with b1:

                if st.button(
                    "👁 Ver detalles" if not seleccionada else "Cerrar detalles",
                    key=f"detalle_{i}"
                ):

                    if seleccionada:
                        st.session_state.oferta_seleccionada = None
                    else:
                        st.session_state.oferta_seleccionada = i

                    st.rerun()

            with b2:

                if url:

                    st.link_button(
                        "↗ Ver publicación original",
                        url,
                        key=f"url_{i}"
                    )

            # Detalle debajo de la oferta seleccionada

            if st.session_state.oferta_seleccionada == i:

                st.divider()

                st.markdown("### 🔎 Detalle de la oferta")

                st.write("**Puesto:**", puesto)

                st.write("**Empresa:**", empresa)

                st.write("**Ubicación:**", ubicacion)
                st.write("**Modalidad:**", oferta.get("modalidad", "No especificada"))

                descripcion = oferta.get("descripcion", "").strip()
                if descripcion:
                    st.write("**Descripción:**", descripcion)

                if url:

                    st.link_button(
                        "Acceder a la oferta en CompuTrabajo ↗",
                        url,
                        key=f"detalle_url_{i}"
                    )

elif not st.session_state.error_busqueda:

    st.warning(
        "No se encontraron ofertas que coincidan con los filtros."
    )


# ==========================================
# 16. PIE DE PÁGINA
# ==========================================

st.divider()

st.markdown("""
<div class="pie-pagina">
    CompuTrabajo | Proyecto académico de Lenguajes de Programación
</div>
""", unsafe_allow_html=True)
