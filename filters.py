import json
import re
import unicodedata
from pathlib import Path

BASE_URL = "https://pe.computrabajo.com"

MODALIDADES_VALIDAS = {
    "remoto": "remoto",
    "teletrabajo": "remoto",
    "hibrido": "presencial y remoto",
    "presencial y remoto": "presencial y remoto",
    "presencial": "presencial",
}

MODALIDAD_URL_SUFFIX = {
    "remoto": "-en-remoto",
    "presencial y remoto": "-hibrido",
}


def normalizar_texto(texto: str) -> str:
    """Convierte texto a minúsculas, sin tildes y con espacios colapsados."""
    if not texto:
        return ""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )
    return re.sub(r"\s+", " ", sin_tildes).strip().lower()


def slugificar(texto: str) -> str:
    """Convierte un texto en un slug válido para URLs de Computrabajo."""
    limpio = normalizar_texto(texto)
    limpio = re.sub(r"[^a-z0-9\s-]", "", limpio)
    return re.sub(r"[\s-]+", "-", limpio).strip("-")


def normalizar_modalidad(modalidad: str) -> str:
    """Normaliza sinónimos de modalidad a los valores estándar del scraper."""
    clave = normalizar_texto(modalidad)
    return MODALIDADES_VALIDAS.get(clave, clave)


def construir_url(puesto: str = "", ubicacion: str = "", modalidad: str = "") -> str:
    """Construye la URL de búsqueda en Computrabajo Perú según los filtros."""
    puesto_slug = slugificar(puesto)
    ubicacion_slug = slugificar(ubicacion)
    modalidad_norm = normalizar_modalidad(modalidad)

    ruta = f"/trabajo-de-{puesto_slug}" if puesto_slug else "/empleos"
    if ubicacion_slug:
        ruta += f"-en-{ubicacion_slug}"

    ruta += MODALIDAD_URL_SUFFIX.get(modalidad_norm, "")
    return f"{BASE_URL}{ruta}"


def filtrar_ofertas(
    ofertas: list[dict],
    puesto: str = "",
    ubicacion: str = "",
    modalidad: str = "",
) -> list[dict]:
    """Filtra una lista de ofertas por puesto, ubicación y modalidad."""
    tokens_puesto = normalizar_texto(puesto).split()
    ubicacion_norm = normalizar_texto(ubicacion)
    modalidad_norm = normalizar_modalidad(modalidad)

    resultado = []
    for oferta in ofertas:
        puesto_oferta = normalizar_texto(oferta.get("puesto", ""))
        ubicacion_oferta = normalizar_texto(oferta.get("ubicacion", ""))
        modalidad_oferta = normalizar_modalidad(oferta.get("modalidad", ""))

        if tokens_puesto and not all(token in puesto_oferta for token in tokens_puesto):
            continue
        if ubicacion_norm and ubicacion_norm not in ubicacion_oferta:
            continue
        if modalidad_norm and modalidad_oferta != modalidad_norm:
            continue

        resultado.append(oferta)

    return resultado


def cargar_ofertas(ruta: str = "data/ofertas.json") -> list[dict]:
    """Carga ofertas guardadas desde un archivo JSON."""
    archivo = Path(ruta)
    if not archivo.exists():
        return []
    with archivo.open("r", encoding="utf-8") as file:
        return json.load(file)
