import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

from filters import coincide_filtros, normalizar

URL = "https://pe.computrabajo.com/trabajo-de-software"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
    "Referer": "https://pe.computrabajo.com/",
}


def slug(texto: str) -> str:
    # Convierte peusto o ubicación a un segmento de URL
    texto = normalizar(texto)
    texto = re.sub(r"[^a-z0-9\s-]", "", texto)
    return re.sub(r"[\s-]+", "-", texto).strip("-")


def construir_url(puesto: str, ubicacion: str, modalidad: str) -> str:
    # Construye la URL inicial de búsqueda de Computrabajo
    puesto_slug = slug(puesto or "software")

    if puesto_slug == "software":
        url = URL
    else:
        dominio = URL.split("/trabajo-de-", 1)[0]
        url = f"{dominio}/trabajo-de-{puesto_slug}"

    if ubicacion:
        url += f"-en-{slug(ubicacion)}"

    modalidad = normalizar(modalidad)
    if modalidad in {"remoto", "teletrabajo"}:
        url += "-en-remoto"
    elif modalidad in {"hibrido", "híbrido", "presencial y remoto"}:
        url += "-hibrido"

    # La búsqueda presencial se valida con el dato de cada tarjeta
    return url


def extraer_modalidad(box) -> str:
    # Lee la modalidad mostrada en la tarjeta de resultados
    for etiqueta in box.select("span.dIB.mr10"):
        texto = normalizar(etiqueta.get_text(" ", strip=True))

        if "remoto" in texto or "teletrabajo" in texto:
            if "presencial" in texto or "hibrido" in texto:
                return "Presencial y remoto"
            return "Remoto"

    return "Presencial"


def buscar_descripcion_jsonld(dato):
    # Busca la descripción del puesto de trabajo en datos JSON-LD anidados
    if isinstance(dato, list):
        for elemento in dato:
            descripcion = buscar_descripcion_jsonld(elemento)
            if descripcion:
                return descripcion

    elif isinstance(dato, dict):
        tipo = dato.get("@type", [])
        if isinstance(tipo, str):
            tipo = [tipo]

        if "JobPosting" in tipo and dato.get("description"):
            return dato["description"]

        for valor in dato.values():
            descripcion = buscar_descripcion_jsonld(valor)
            if descripcion:
                return descripcion

    return ""


def extraer_descripcion(session: requests.Session, url: str) -> str:
    # Abre la oferta y devuelve la descripción en texto plano
    respuesta = session.get(url, headers=HEADERS, timeout=20)
    respuesta.raise_for_status()
    soup = BeautifulSoup(respuesta.text, "html.parser")

    for script in soup.select('script[type="application/ld+json"]'):
        try:
            dato = json.loads(script.string or script.get_text())
        except (json.JSONDecodeError, TypeError):
            continue

        descripcion = buscar_descripcion_jsonld(dato)
        if descripcion:
            return BeautifulSoup(descripcion, "html.parser").get_text(" ", strip=True)

    etiqueta = soup.select_one(
        '[itemprop="description"], #p_ofertas, .box_detail'
    )
    return etiqueta.get_text(" ", strip=True) if etiqueta else ""


def extraer_oferta(box, pagina_url: str) -> dict | None:
    # Lee los campos de una tarjeta de resultados
    titulo = box.select_one("h2 a.js-o-link, a.js-o-link, h2 a")
    if not titulo:
        return None

    empresa = ""
    empresa_box = box.select_one("p.dFlex.vm_fx.fs16.fc_base.mt5")
    if empresa_box:
        empresa_link = empresa_box.select_one("a.fc_base.t_ellipsis, a")
        empresa = (
            empresa_link.get_text(" ", strip=True)
            if empresa_link
            else empresa_box.get_text(" ", strip=True)
        )

    ubicacion_tag = box.select_one(
        ".fs16.fc_base.mt5:not(.dFlex) span.mr10, "
        "p.fs16.fc_base.mt5:not(.dFlex)"
    )
    href = titulo.get("href")
    if not href:
        return None

    return {
        "puesto": titulo.get_text(" ", strip=True),
        "empresa": empresa,
        "ubicacion": ubicacion_tag.get_text(" ", strip=True) if ubicacion_tag else "",
        "modalidad": extraer_modalidad(box),
        "url": urljoin(pagina_url, href),
    }


def siguiente_pagina(soup: BeautifulSoup, pagina_url: str) -> str | None:
    # Devuelve el enlace siguiente de la paginación
    for enlace in soup.select("a[href]"):
        rel = " ".join(enlace.get("rel", [])).lower()
        etiqueta = " ".join(
            [
                enlace.get_text(" ", strip=True),
                enlace.get("aria-label", ""),
                enlace.get("title", ""),
                " ".join(enlace.get("class", [])),
            ]
        )
        etiqueta = normalizar(etiqueta)

        if "next" in rel or "siguiente" in etiqueta or etiqueta.strip() in {"›", "»"}:
            return urljoin(pagina_url, enlace["href"])

    return None


def clave_oferta(url: str) -> str:
    # Quita el fragmento de una URL para evitar la duplicación de la oferta
    partes = urlsplit(url)
    return urlunsplit((partes.scheme, partes.netloc, partes.path, partes.query, ""))


def scrapear_ofertas(puesto: str, ubicacion: str, modalidad: str) -> list[dict]:
    # Recorre la búsqueda, completa detalles y devuelve ofertas coincidentes
    url_actual = construir_url(puesto, ubicacion, modalidad)
    urls_visitadas = set()
    urls_procesadas = set()
    ofertas_por_url = {}

    with requests.Session() as session:
        while url_actual and url_actual not in urls_visitadas:
            urls_visitadas.add(url_actual)

            respuesta = session.get(url_actual, headers=HEADERS, timeout=20)
            respuesta.raise_for_status()
            soup = BeautifulSoup(respuesta.text, "html.parser")

            for box in soup.select("article.box_offer, .box_offer"):
                oferta = extraer_oferta(box, respuesta.url)
                if not oferta:
                    continue

                clave = clave_oferta(oferta["url"])
                if clave in urls_procesadas:
                    continue
                urls_procesadas.add(clave)

                oferta["descripcion"] = extraer_descripcion(session, oferta["url"])

                if coincide_filtros(oferta, puesto, ubicacion, modalidad):
                    ofertas_por_url[clave] = oferta

            url_actual = siguiente_pagina(soup, respuesta.url)

    return list(ofertas_por_url.values())
