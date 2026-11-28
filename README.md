# Buscador de empleos

Aplicación académica en Python que busca ofertas en Computrabajo Perú. Permite filtrar por puesto o palabras clave, departamento y modalidad. La búsqueda recorre las páginas de resultados, abre cada oferta para leer su descripción y muestra las coincidencias en una interfaz web.

El proyecto tiene dos formas de uso:

- **Interfaz web:** permite seleccionar filtros, revisar las ofertas y descargar los resultados en CSV.
- **Consola:** ejecuta una búsqueda pasando los filtros como argumentos.

En ambos casos el scraper guarda también la última búsqueda en `data/ofertas.json`. La interfaz usa directamente la lista que devuelve el scraper; no carga los resultados desde ese JSON. El archivo `data/ofertas.json` se ignora en Git porque es un resultado generado.

## Requisitos

- Python 3.10 o superior.
- `requests` para hacer solicitudes web.
- `beautifulsoup4` para leer y extraer datos del HTML.
- `streamlit` para ejecutar la interfaz web.

`argparse`, `csv`, `json`, `pathlib`, `re`, `sys`, `unicodedata`, `io` y `urllib.parse` pertenecen a la biblioteca estándar de Python; no necesitan instalarse por separado.

## Instalación en Windows

Abre CMD en la carpeta del proyecto y ejecuta:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install requests beautifulsoup4 streamlit
```

El entorno virtual `.venv` guarda las dependencias de este proyecto separadas de otros proyectos de Python.

## Ejecutar la interfaz web

Con el entorno virtual activo:

```cmd
streamlit run frontend/app.py
```

Streamlit mostrará una dirección local en la terminal y abrirá la aplicación en el navegador. En el panel lateral, escribe el puesto o las palabras clave, selecciona un departamento y una modalidad y pulsa **Buscar ofertas**. Si quieres omitir un filtro, elige **Todos** para departamento o **Todas** para modalidad. Si dejas vacío el puesto, la aplicación busca `software` por defecto.

La lista aparece en el área principal. Antes de realizar una búsqueda se muestra un mensaje inicial y el botón **Exportar CSV** está deshabilitado. Después de buscar, el botón descarga las coincidencias de esa búsqueda.

## Ejecutar desde la consola

Una búsqueda por defecto busca `software`:

```cmd
python scraper.py
```

Se pueden especificar filtros con `--puesto`, `--ubicacion` y `--modalidad`:

```cmd
python scraper.py --puesto "python" --ubicacion "Lima" --modalidad "remoto"
python scraper.py --puesto "software" --ubicacion "Arequipa" --modalidad "hibrido"
python scraper.py --puesto "qa" --modalidad "presencial"
```

En CMD escribe cada comando en una sola línea. Al terminar se imprime la cantidad de ofertas encontradas y la ruta del JSON generado.

### Cómo se aplican los filtros

- `--puesto` busca en el título **y** en la descripción de la oferta. Si contiene varias palabras, todas deben aparecer; `python django` requiere que aparezcan ambas.
- `--ubicacion` busca el texto indicado dentro de la ubicación extraída de la tarjeta. Puede omitirse.
- `--modalidad` acepta `presencial`, `remoto` o `hibrido`. Puede omitirse. La modalidad se identifica en la etiqueta de la oferta y se comprueba junto con los demás filtros.

La interfaz web ofrece los departamentos del Perú como opciones de ubicación. La consola acepta texto libre.

## Cómo funciona el proyecto

1. `frontend/app.py` o `scraper.py` recoge los filtros introducidos.
2. `scraper.py` coordina la búsqueda y llama a `computrabajo.py`.
3. `computrabajo.py` construye la URL de búsqueda, recorre las páginas, extrae las tarjetas y visita los enlaces de las ofertas para obtener la descripción.
4. `filters.py` normaliza los textos y conserva solo las ofertas que coinciden con todos los filtros.
5. El scraper devuelve la lista y guarda una copia en `data/ofertas.json`.
6. La interfaz presenta la lista en memoria; `exportar.py` puede convertirla en un CSV descargable.

La guía detallada del scraper está en [docs/scraper.md](docs/scraper.md). La interfaz y la exportación tienen sus propias guías: [docs/frontend.md](docs/frontend.md) y [docs/exportar.md](docs/exportar.md).

## Imports usados en el proyecto

En Python, una **importación** permite usar código que ya existe en otro módulo o biblioteca. Los imports del proyecto se dividen en tres grupos:

### Biblioteca estándar de Python

No hay que instalarlos con `pip`:

| Import | Archivo(s) | Para qué se usa |
| --- | --- | --- |
| `argparse` | `scraper.py` | Leer opciones como `--puesto` al ejecutar desde la consola. |
| `csv` | `exportar.py` | Escribir las ofertas en formato CSV. |
| `io.StringIO` | `exportar.py` | Crear el contenido CSV en memoria antes de descargarlo. |
| `json` | `scraper.py`, `computrabajo.py` | Guardar resultados como JSON y leer datos JSON-LD de las páginas. |
| `pathlib.Path` | `scraper.py`, `frontend/app.py` | Construir rutas de archivos y carpetas de forma portable. |
| `re` | `computrabajo.py`, `filters.py` | Buscar o reemplazar patrones en texto. |
| `sys` | `frontend/app.py` | Añadir la raíz del proyecto a las rutas donde Python busca módulos. |
| `unicodedata` | `filters.py` | Quitar tildes para comparar textos de manera consistente. |
| `urllib.parse` | `computrabajo.py` | Unir enlaces relativos con la URL de la página y normalizar URLs. |

### Dependencias instaladas con `pip`

| Import | Paquete | Para qué se usa |
| --- | --- | --- |
| `requests` | `requests` | Descargar páginas de Computrabajo y mantener una sesión HTTP. |
| `BeautifulSoup` | `beautifulsoup4` | Interpretar el HTML descargado y buscar tarjetas, enlaces y datos. |
| `streamlit as st` | `streamlit` | Crear la interfaz web, sus controles, mensajes y descarga. |

En `import streamlit as st`, `st` es un alias corto: permite escribir `st.button()` en lugar de `streamlit.button()`.

### Imports del propio proyecto

Estos importan funciones entre los archivos del repositorio:

| Import | Qué conecta |
| --- | --- |
| `from computrabajo import scrapear_ofertas` | `scraper.py` usa la extracción web implementada en `computrabajo.py`. |
| `from filters import coincide_filtros, normalizar` | `computrabajo.py` reutiliza las comparaciones y la normalización. |
| `from scraper import buscar_ofertas` | `frontend/app.py` ejecuta el scraper directamente. |
| `from exportar import generar_csv` | `frontend/app.py` prepara la descarga CSV. |

## Estructura de archivos

```text
buscador-empleos/
├── computrabajo.py       # Descarga y extracción de Computrabajo
├── filters.py            # Normalización y aplicación de filtros
├── scraper.py            # Coordinación, CLI y guardado en JSON
├── exportar.py           # Conversión de resultados a CSV
├── frontend/
│   └── app.py            # Interfaz web de Streamlit
├── docs/
│   ├── scraper.md        # Guía de scraper.py, computrabajo.py y filters.py
│   ├── frontend.md       # Guía de la interfaz web
│   └── exportar.md       # Guía del archivo CSV
└── data/
    ├── .gitkeep          # Mantiene la carpeta vacía en Git
    └── ofertas.json      # Última búsqueda; generado localmente e ignorado por Git
```

## Datos generados

Cada elemento de `data/ofertas.json` representa una oferta y puede incluir:

| Campo | Significado |
| --- | --- |
| `puesto` | Título del puesto publicado. |
| `empresa` | Empresa que publica la oferta, si aparece. |
| `ubicacion` | Ubicación mostrada en la tarjeta. |
| `modalidad` | Modalidad identificada en la tarjeta. |
| `url` | Enlace directo a la oferta. |
| `descripcion` | Descripción extraída de la página de la oferta, si se pudo obtener. |

El CSV descargable incluye `puesto`, `empresa`, `ubicacion`, `modalidad` y `url`; no incluye la descripción. Usa punto y coma para separar columnas y facilita abrirlo con Excel en español.
