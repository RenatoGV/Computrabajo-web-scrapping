# Guía de `exportar.py`

`exportar.py` tiene una sola responsabilidad: convertir las ofertas de la búsqueda actual en texto CSV para que Streamlit lo entregue como archivo descargable. No consulta Computrabajo ni lee `data/ofertas.json`.

## Imports

```python
import csv
from io import StringIO
```

- `csv` es una biblioteca estándar de Python que escribe datos tabulares con reglas de CSV, incluidas las comillas necesarias cuando un valor contiene el separador.
- `StringIO` crea un archivo de texto temporal en memoria. Esto permite preparar el contenido sin crear un archivo temporal en el disco.

## Columnas

`CAMPOS_CSV` define el orden y los nombres de las columnas exportadas:

1. `puesto`
2. `empresa`
3. `ubicacion`
4. `modalidad`
5. `url`

La descripción se muestra en la aplicación y se guarda en el JSON, pero se excluye del CSV.

## `generar_csv(ofertas)`

La función recibe una lista de diccionarios, donde cada diccionario representa una oferta. Crea un `csv.DictWriter` con esas columnas y punto y coma como separador, escribe la fila de encabezados y después una fila por oferta. Si una oferta no contiene uno de los campos, esa celda queda vacía; otros campos que no están en `CAMPOS_CSV` se ignoran.

Devuelve una cadena de texto que empieza con la marca BOM de UTF-8 (`\ufeff`). Esa marca ayuda a Excel a reconocer correctamente acentos y caracteres como `ñ` al abrir el archivo.

El separador `;` se usa para que Excel con configuración regional en español distribuya los campos en columnas. Las comas dentro de un título, empresa o ubicación se conservan como parte del valor y no separan columnas.

## Cómo se conecta con el frontend

En `frontend/app.py` se importa la función:

```python
from exportar import generar_csv
```

El botón de descarga recibe `generar_csv(resultados)` como contenido, usa el nombre `ofertas.csv` y declara el tipo `text/csv`. Así se descarga directamente desde memoria, sin crear un archivo intermedio. El botón permanece deshabilitado antes de realizar la primera búsqueda.

## Cambiar el formato

- Para agregar o quitar una columna, edita `CAMPOS_CSV`.
- Para usar otro separador, cambia el argumento `delimiter` del `DictWriter`. El punto y coma está elegido para Excel en español.
- Para cambiar el nombre del archivo, edita `file_name` en el `st.download_button()` de `frontend/app.py`.
