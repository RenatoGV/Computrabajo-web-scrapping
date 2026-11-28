import re
import unicodedata

def normalizar(texto: str) -> str:
    # Normaliza mayúsculas, tildes y espacios para comparar textos
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).strip().lower()


def coincide_filtros(oferta: dict, puesto: str, ubicacion: str, modalidad: str) -> bool:
    # Comprueba los filtros contra una oferta que ya ha sido extraída
    puesto_normalizado = normalizar(puesto).split()

    texto_puesto = normalizar(oferta.get("puesto", "") + " " + oferta.get("descripcion", ""))

    lugar = normalizar(oferta.get("ubicacion", ""))
    oferta_normalizado = normalizar(oferta.get("modalidad", ""))
    busqueda_normalizada = normalizar(modalidad)

    if not all(palabra in texto_puesto for palabra in puesto_normalizado):
        return False

    if ubicacion and normalizar(ubicacion) not in lugar:
        return False

    if busqueda_normalizada in {"hibrido", "híbrido"}:
        busqueda_normalizada = "presencial y remoto"
    elif busqueda_normalizada == "teletrabajo":
        busqueda_normalizada = "remoto"

    return not busqueda_normalizada or oferta_normalizado == busqueda_normalizada
