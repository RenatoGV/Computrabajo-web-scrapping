
import json
from pathlib import Path
import streamlit as st


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
    --texto: #142B4D;
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

/* Nota informativa */
.sidebar-nota {
    color: #E2EEFC;
    font-size: 12px;
    line-height: 1.6;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 13px;
    border-radius: 10px;
}

/* Campos de búsqueda */
[data-testid="stSidebar"] input {
    background: #FFFFFF !important;
    color: #142B4D !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #142B4D !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #142B4D !important;
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
# 9. CARGAR DATOS DEL JSON
# ==========================================

RUTA_JSON = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ofertas.json"
)


def cargar_ofertas():

    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        return datos if isinstance(datos, list) else []

    except FileNotFoundError:
        st.error("No se encontró data/ofertas.json.")
        return []

    except json.JSONDecodeError:
        st.error("El archivo JSON tiene un formato inválido.")
        return []

    except Exception as error:
        st.error(f"Error al cargar las ofertas: {error}")
        return []


ofertas = cargar_ofertas()


# ==========================================
# 10. ESTADO DE LA APLICACIÓN
# ==========================================

if "oferta_seleccionada" not in st.session_state:
    st.session_state.oferta_seleccionada = None

if "filtros_aplicados" not in st.session_state:
    st.session_state.filtros_aplicados = {
        "palabra": "",
        "empresa": "Todas",
        "ubicacion": "Todas",
        "orden": "Predeterminado"
    }


# ==========================================
# 11. BARRA LATERAL Y FILTROS
# ==========================================

st.sidebar.markdown("""
<div class="marca">💼 CompuTrabajo</div>
<div class="marca-subtitulo">PORTAL DE EMPLEO</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.subheader("⚙️ Filtros de búsqueda")


# Obtener empresas y ubicaciones disponibles

empresas = sorted(set(
    x.get("empresa", "").strip()
    for x in ofertas
    if x.get("empresa", "").strip()
))

ubicaciones = sorted(set(
    x.get("ubicacion", "").strip()
    for x in ofertas
    if x.get("ubicacion", "").strip()
))


# Formulario de filtros

with st.sidebar.form("form_filtros"):

    palabra = st.text_input(
        "Puesto o palabra clave",
        placeholder="Ejemplo: Java, analista..."
    )

    empresa = st.selectbox(
        "Empresa",
        ["Todas"] + empresas
    )

    ubicacion = st.selectbox(
        "Ubicación",
        ["Todas"] + ubicaciones
    )

    orden = st.selectbox(
        "Ordenar resultados",
        [
            "Predeterminado",
            "Puesto (A-Z)",
            "Empresa (A-Z)",
            "Ubicación (A-Z)"
        ]
    )

    aplicar = st.form_submit_button(
        "🔎 Aplicar filtros",
        use_container_width=True
    )

    if aplicar:

        st.session_state.filtros_aplicados = {
            "palabra": palabra,
            "empresa": empresa,
            "ubicacion": ubicacion,
            "orden": orden
        }

        st.session_state.oferta_seleccionada = None


st.sidebar.divider()

st.sidebar.markdown("""
<div class="sidebar-nota">
    ⓘ Los datos mostrados provienen del archivo
    <b>ofertas.json</b> generado por el scraper.
</div>
""", unsafe_allow_html=True)


# ==========================================
# 12. PROCESAMIENTO DE FILTROS
# ==========================================

filtros = st.session_state.filtros_aplicados

resultados = []

for oferta in ofertas:

    puesto = oferta.get("puesto", "")
    empresa_oferta = oferta.get("empresa", "")
    ubicacion_oferta = oferta.get("ubicacion", "")

    # Filtro por palabra clave
    if filtros["palabra"]:

        if filtros["palabra"].lower() not in puesto.lower():
            continue

    # Filtro por empresa
    if filtros["empresa"] != "Todas":

        if empresa_oferta != filtros["empresa"]:
            continue

    # Filtro por ubicación
    if filtros["ubicacion"] != "Todas":

        if ubicacion_oferta != filtros["ubicacion"]:
            continue

    resultados.append(oferta)


# ==========================================
# 13. ORDENAMIENTO
# ==========================================

if filtros["orden"] == "Puesto (A-Z)":

    resultados.sort(
        key=lambda x: x.get("puesto", "").lower()
    )

elif filtros["orden"] == "Empresa (A-Z)":

    resultados.sort(
        key=lambda x: x.get("empresa", "").lower()
    )

elif filtros["orden"] == "Ubicación (A-Z)":

    resultados.sort(
        key=lambda x: x.get("ubicacion", "").lower()
    )


# ==========================================
# 14. ENCABEZADO PRINCIPAL
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
# 15. ESTADÍSTICAS
# ==========================================

total_ofertas = len(ofertas)

total_resultados = len(resultados)

total_empresas = len(set(
    x.get("empresa", "").strip()
    for x in ofertas
    if x.get("empresa", "").strip()
))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💼 Ofertas registradas",
        total_ofertas
    )

with col2:
    st.metric(
        "🔎 Resultados encontrados",
        total_resultados
    )

with col3:
    st.metric(
        "🏢 Empresas registradas",
        total_empresas
    )


st.write("")
st.divider()


# ==========================================
# 16. LISTADO DE OFERTAS
# ==========================================

st.subheader("💼 Ofertas laborales disponibles")

st.caption(
    f"Se encontraron {total_resultados} oportunidades."
)


if resultados:

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

                if url:

                    st.link_button(
                        "Acceder a la oferta en CompuTrabajo ↗",
                        url,
                        key=f"detalle_url_{i}"
                    )

else:

    st.warning(
        "No se encontraron ofertas que coincidan con los filtros."
    )


# ==========================================
# 17. PIE DE PÁGINA
# ==========================================

st.divider()

st.markdown("""
<div class="pie-pagina">
    CompuTrabajo | Proyecto académico de Lenguajes de Programación
</div>
""", unsafe_allow_html=True)
