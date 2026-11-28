import argparse
import json
from pathlib import Path

from computrabajo import scrapear_ofertas

SALIDA = Path(__file__).resolve().parent / "data" / "ofertas.json"


def guardar_ofertas(ofertas: list[dict]) -> None:
    # Guarda los resultados de la búsqueda en el archivo JSON
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8") as archivo:
        json.dump(ofertas, archivo, ensure_ascii=False, indent=3)


def buscar_ofertas(
    puesto: str = "software",
    ubicacion: str = "",
    modalidad: str = "",
) -> list[dict]:
    """Busca ofertas, las guarda en JSON y devuelve la lista a quien la llamó."""
    ofertas = scrapear_ofertas(puesto or "software", ubicacion, modalidad)
    guardar_ofertas(ofertas)
    return ofertas


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Busca ofertas de Computrabajo aplicando filtros."
    )
    parser.add_argument("--puesto", default="software")
    parser.add_argument("--ubicacion", default="")
    parser.add_argument(
        "--modalidad",
        choices=["", "presencial", "remoto", "hibrido"],
        default="",
    )
    args = parser.parse_args()

    ofertas = buscar_ofertas(args.puesto, args.ubicacion, args.modalidad)

    print(f"Se guardaron {len(ofertas)} ofertas en {SALIDA}.")


if __name__ == "__main__":
    main()
