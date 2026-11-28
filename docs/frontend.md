# Guía del frontend

Este documento explica `frontend/app.py`, la interfaz web del buscador. La aplicación está hecha con Streamlit y ejecuta el scraper cuando la persona envía el formulario.

## Ejecutar

Desde la raíz del proyecto, con las dependencias instaladas y el entorno virtual activo:

```cmd
streamlit run frontend/app.py
```

Streamlit inicia un servidor local y abre la interfaz en el navegador. Para detenerlo, pulsa `Ctrl+C` en la terminal.

## Imports

```python
import sys
from pathlib import Path
import streamlit as st
from scraper import buscar_ofertas
from exportar import generar_csv
```

- `sys` y `Path` permiten encontrar la carpeta raíz del proyecto cuando Streamlit inicia el archivo dentro de `frontend/`.
- `streamlit as st` importa las herramientas de Streamlit con el alias corto `st`.
- `buscar_ofertas` ejecuta la búsqueda web y devuelve una lista de ofertas.
- `generar_csv` convierte esa lista en texto CSV para el botón de descarga.

`ROOT_DIR` calcula la carpeta principal del proyecto. Si hace falta, se añade a `sys.path`, que es la lista de carpetas donde Python busca módulos. Así la interfaz puede importar `scraper.py` y `exportar.py`, que están un nivel por encima de `frontend/`.

## Controles de búsqueda

El formulario está en la barra lateral y tiene tres filtros:

- **Puesto o palabra clave:** texto que se envía como filtro de puesto. Puede contener un cargo, lenguaje, tecnología o varias palabras.
- **Departamento:** uno de los departamentos de Perú o `Todos` para no filtrar por ubicación.
- **Modalidad:** `Todas`, `Presencial`, `Remoto` o `Híbrido`.

El formulario solo envía los valores al pulsar **Buscar ofertas**. Antes de llamar al scraper, la interfaz convierte `Todos` y `Todas` en valores vacíos porque significan que no se aplique ese filtro. También envía una palabra por defecto (`software`) si el campo de puesto se dejó vacío.

## Flujo al buscar

1. Streamlit ejecuta de nuevo el archivo cuando se pulsa el botón del formulario.
2. `buscar_ofertas()` llama al scraper con el puesto, la ubicación y la modalidad.
3. El scraper recorre los resultados web, aplica los filtros y devuelve una lista.
4. La interfaz guarda esa lista en `st.session_state.ofertas` y muestra las tarjetas en la vista principal.

La interfaz **no lee `data/ofertas.json`**. El scraper guarda ese JSON como salida secundaria, pero la vista y el CSV usan la lista devuelta en memoria.

## Estado de la interfaz

Streamlit vuelve a ejecutar el script después de muchas interacciones. `st.session_state` mantiene valores entre esas ejecuciones:

- `ofertas`: ofertas devueltas por la última búsqueda.
- `busqueda_realizada`: indica si ya se envió una búsqueda.
- `filtros_aplicados`: filtros usados en esa búsqueda.
- `oferta_seleccionada`: tarjeta cuyos detalles se encuentran abiertos.
- `error_busqueda`: mensaje de error, si el scraper no pudo completar la búsqueda.

Si aún no se ha buscado, aparece un estado vacío con instrucciones. Si la búsqueda no devuelve coincidencias, aparece un aviso. Si ocurre una excepción, se muestra el error y se conserva una lista vacía.

## Resultados y descarga

La vista principal presenta el número de ofertas, empresas y modalidades encontradas. Cada resultado puede mostrar puesto, empresa, ubicación y modalidad. El control de detalles permite ver más información disponible y abrir la publicación original.

El botón **Exportar CSV** llama a `generar_csv(resultados)` y descarga `ofertas.csv`. Está deshabilitado hasta que `busqueda_realizada` sea verdadero. Si ya se buscó y no se encontraron ofertas, permite descargar un CSV con solo los encabezados.

La estructura y estilos visuales están definidos en el mismo archivo mediante CSS incluido con `st.markdown()`. El HTML/CSS controla la presentación; los controles y la lógica de búsqueda siguen siendo componentes de Streamlit.

## Si algo falla

- Ejecuta `streamlit run frontend/app.py` desde la raíz del repositorio para que las rutas locales sean las esperadas.
- Si no carga el módulo `scraper`, comprueba que `scraper.py` se encuentre en la raíz del proyecto.
- Si aparece un error durante la consulta, el mensaje se muestra encima de la lista; revisa la conexión y los selectores del scraper.
- Para los detalles de extracción y filtros, consulta [scraper.md](scraper.md).
- Para cambiar las columnas o el formato descargado, consulta [exportar.md](exportar.md).
