import argparse
import json
from pathlib import Path

from computrabajo import scrapear_ofertas

SALIDA = Path("data/ofertas.json")


def guardar_ofertas(ofertas: list[dict]) -> None:
    # Guarda los resultados de la búsqueda en el archivo JSON
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8") as archivo:
        json.dump(ofertas, archivo, ensure_ascii=False, indent=3)


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

    ofertas = scrapear_ofertas(args.puesto, args.ubicacion, args.modalidad)
    guardar_ofertas(ofertas)

    print(f"Se guardaron {len(ofertas)} ofertas en {SALIDA}.")


if __name__ == "__main__":
    main()
