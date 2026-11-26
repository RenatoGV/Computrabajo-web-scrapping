# Buscador de empleos

Proyecto académico en Python que obtiene ofertas laborales de Computrabajo y las guarda en `data/ofertas.json` con soporte para filtros por puesto, ubicación y modalidad.

## Requisitos

- Python 3
- `requests`
- `beautifulsoup4`

## Instalación en Windows

Desde CMD, dentro de esta carpeta:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install requests beautifulsoup4
```

## Ejecución

Scraping por defecto (`software`):

```cmd
python scraper.py
```

Scraping con filtros (`--puesto`, `--ubicacion`, `--modalidad`):

```cmd
python scraper.py --puesto "python" --ubicacion "Lima" --modalidad "remoto"
python scraper.py --puesto "software" --ubicacion "Arequipa" --modalidad "hibrido"
python scraper.py --puesto "qa" --modalidad "presencial"
```

Filtrar localmente sobre `data/ofertas.json` sin volver a consultar la web:

```cmd
python scraper.py --local --puesto "qa" --ubicacion "Lima" --modalidad "presencial"
```

## Estructura de `data/ofertas.json`

Cada oferta guardada incluye:

- `puesto`: título del puesto laboral
- `empresa`: nombre de la empresa
- `ubicacion`: distrito / departamento
- `modalidad`: `Presencial`, `Remoto` o `Presencial y remoto`
- `url`: enlace directo a la oferta en Computrabajo

## Uso desde Python (para el frontend / API)

```python
from filters import cargar_ofertas, filtrar_ofertas
from scraper import scrapear_ofertas

# Opción 1: obtener ofertas filtradas directamente desde Computrabajo
ofertas = scrapear_ofertas(puesto="software", ubicacion="Lima", modalidad="remoto")

# Opción 2: filtrar ofertas ya guardadas en data/ofertas.json
todas = cargar_ofertas("data/ofertas.json")
filtradas = filtrar_ofertas(todas, puesto="qa", ubicacion="Lima", modalidad="presencial")
```
