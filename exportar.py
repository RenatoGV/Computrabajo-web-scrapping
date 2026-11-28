import csv
from io import StringIO

CAMPOS_CSV = [
    "puesto",
    "empresa",
    "ubicacion",
    "modalidad",
    "url",
]


def generar_csv(ofertas: list[dict]) -> str:
    """Convierte una lista de ofertas a CSV compatible con Excel."""
    salida = StringIO(newline="")
    escritor = csv.DictWriter(
        salida,
        fieldnames=CAMPOS_CSV,
        delimiter=";",
        extrasaction="ignore",
    )
    escritor.writeheader()
    escritor.writerows(ofertas)
    return "\ufeff" + salida.getvalue()
