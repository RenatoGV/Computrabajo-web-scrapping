import argparse
import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from filters import (
    cargar_ofertas,
    construir_url,
    filtrar_ofertas,
    normalizar_modalidad,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
    "Referer": "https://pe.computrabajo.com/",
}


def extraer_modalidad(box) -> str:
    """Extrae la modalidad de trabajo de una tarjeta de oferta."""
    icono_remoto = box.select_one("span.icon.i_home_office")
    if icono_remoto and icono_remoto.parent:
        texto = icono_remoto.parent.get_text(" ", strip=True)
        if texto:
            return texto
    return "Presencial"


def extraer_oferta(box, base_url: str) -> dict:
    """Extrae los campos principales de una oferta laboral."""
    titulo = box.select_one("h2 a.js-o-link, a.js-o-link, h2 a")

    empresa_box = box.select_one("p.dFlex.vm_fx.fs16.fc_base.mt5")
    if empresa_box:
        empresa_link = empresa_box.select_one("a.fc_base.t_ellipsis, a")
        empresa = (
            empresa_link.get_text(" ", strip=True)
            if empresa_link
            else empresa_box.get_text(" ", strip=True)
        )
    else:
        empresa = ""

    ubicacion = box.select_one(
        ".fs16.fc_base.mt5:not(.dFlex) span.mr10, p.fs16.fc_base.mt5:not(.dFlex)"
    )
    enlace = titulo.get("href", "") if titulo else ""

    return {
        "puesto": titulo.get_text(" ", strip=True) if titulo else "",
        "empresa": empresa,
        "ubicacion": ubicacion.get_text(" ", strip=True) if ubicacion else "",
        "modalidad": extraer_modalidad(box),
        "url": urljoin(base_url, enlace) if enlace else "",
    }


def scrapear_ofertas(
    puesto: str = "software",
    ubicacion: str = "",
    modalidad: str = "",
    timeout: int = 20,
) -> list[dict]:
    """Consulta Computrabajo con los filtros indicados y retorna las ofertas."""
    url = construir_url(puesto=puesto, ubicacion=ubicacion, modalidad=modalidad)
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    ofertas = [
        extraer_oferta(box, url)
        for box in soup.select("article.box_offer, .box_offer")
    ]

    # Computrabajo no tiene parámetro URL para "Presencial", así que se filtra localmente.
    if normalizar_modalidad(modalidad) == "presencial":
        ofertas = filtrar_ofertas(ofertas, modalidad="presencial")

    return ofertas


def guardar_ofertas(ofertas: list[dict], ruta: str = "data/ofertas.json") -> None:
    """Guarda la lista de ofertas en un archivo JSON."""
    archivo = Path(ruta)
    archivo.parent.mkdir(parents=True, exist_ok=True)
    with archivo.open("w", encoding="utf-8") as file:
        json.dump(ofertas, file, ensure_ascii=False, indent=3)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scraper y buscador con filtros de ofertas en Computrabajo Perú."
    )
    parser.add_argument(
        "--puesto",
        default="",
        help="Palabra clave o puesto a buscar (ej: 'software', 'python', 'qa').",
    )
    parser.add_argument(
        "--ubicacion",
        default="",
        help="Departamento o ciudad (ej: 'Lima', 'Arequipa', 'La Libertad').",
    )
    parser.add_argument(
        "--modalidad",
        default="",
        help="Modalidad de trabajo: 'presencial', 'remoto' o 'hibrido'.",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Filtra sobre data/ofertas.json existente sin consultar la web.",
    )
    parser.add_argument(
        "--output",
        default="data/ofertas.json",
        help="Ruta del archivo JSON de salida (por defecto: data/ofertas.json).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.local:
        ofertas_base = cargar_ofertas(args.output)
        ofertas = filtrar_ofertas(
            ofertas_base,
            puesto=args.puesto,
            ubicacion=args.ubicacion,
            modalidad=args.modalidad,
        )
        print(f"Se encontraron {len(ofertas)} ofertas locales con los filtros aplicados.")
    else:
        puesto = args.puesto or "software"
        ofertas = scrapear_ofertas(
            puesto=puesto,
            ubicacion=args.ubicacion,
            modalidad=args.modalidad,
        )
        guardar_ofertas(ofertas, args.output)
        print(f"Se guardaron {len(ofertas)} ofertas en {args.output}.")


if __name__ == "__main__":
    main()
