# Buscador de empleos

Proyecto académico en Python que obtiene ofertas laborales de Computrabajo y las guarda en `data/ofertas.json` con soporte para filtros por puesto, ubicación y modalidad.

## Requisitos

- Python 3.10 o superior
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

El puesto se busca en el título y la descripción; si escribes varias palabras, deben aparecer todas. La ubicación se compara con la ubicación de la oferta y la modalidad con la etiqueta de la tarjeta.

Para entender el flujo completo del scraper, sus funciones, filtros y formato de salida, consulta la [guía del scraper](docs/scraper.md).

## Estructura de `data/ofertas.json`

Cada oferta guardada incluye:

- `puesto`: título del puesto laboral
- `empresa`: nombre de la empresa
- `ubicacion`: distrito / departamento
- `modalidad`: `Presencial`, `Remoto` o `Presencial y remoto`
- `url`: enlace directo a la oferta en Computrabajo
- `descripcion`: descripción de la oferta en texto plano, cuando se puede extraer
