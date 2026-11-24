# Buscador de empleos

Proyecto académico en Python que obtiene ofertas laborales de Computrabajo y las guarda en `data/ofertas.json`.

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

```cmd
python scraper.py
```

Las ofertas se guardan en `data/ofertas.json` con estos campos: puesto, empresa, ubicación y enlace.