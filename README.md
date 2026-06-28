# P1Doks Local Sync

## Descripción

**P1Doks Local Sync** es una herramienta desarrollada en Python para automatizar la descarga, organización y sincronización de setups de **P1Doks** hacia la estructura local de **iRacing**.

El proyecto nace para solucionar una limitación del sincronizador oficial de P1Doks, que únicamente hace visibles los setups durante una sesión de iRacing, sin almacenarlos físicamente en el disco para poder organizarlos y reutilizarlos.

Este programa descarga automáticamente los paquetes de setups publicados en P1Doks, extrae únicamente los archivos `.sto` y los organiza siguiendo una estructura limpia y permanente dentro de la carpeta de setups de iRacing.

---

# Características

* Descarga automática de Data Packs desde la API de P1Doks.
* Filtrado por temporada y semana.
* Selección inteligente de los coches más rápidos por categoría.
* Descarga limitada configurable (por ejemplo 24 setups diarios).
* Evita descargar archivos que ya existen.
* Extracción automática únicamente de archivos `.sto`.
* Organización automática por:

  * Temporada
  * Serie
  * Circuito
* Compatible con Garage61.
* Preparado para ampliaciones futuras.

---

# Flujo de funcionamiento

El programa realiza los siguientes pasos:

1. Consulta todos los Data Packs disponibles para la temporada y semana configuradas.
2. Filtra únicamente las categorías deseadas.
3. Selecciona automáticamente los coches más rápidos según la configuración del perfil.
4. Descarga únicamente los paquetes necesarios.
5. Extrae los archivos `.sto` de cada ZIP descargado.
6. Copia los setups a la estructura local de iRacing.

---

# Estructura del proyecto

```text
P1Docks-Local-Sync
│
├── main.py                 # Punto de entrada del programa
├── downloader.py           # Descarga de Data Packs
├── extract_setups.py       # Extracción y organización de archivos .sto
├── selection.py            # Perfiles de descarga
├── selection_engine.py     # Motor de selección de setups
├── classes.py              # Clases y alias de vehículos
├── config.json             # Configuración del usuario
├── car_mapping.json        # Relación entre coches P1Doks e iRacing
│
├── downloads/              # ZIP descargados
└── extracted/              # Carpeta temporal
```

---

# Organización de los setups

Los setups se almacenan automáticamente siguiendo la estructura:

```text
Documents
└── iRacing
    └── setups
        └── <car_folder>
            └── Garage 61 - ZRT MOMO
                └── P1DOKS
                    └── 2026-S3
                        └── IMSA
                            └── Mobility Resort Motegi
                                ├── P1Doks_xxx_E.sto
                                ├── P1Doks_xxx_Q.sto
                                └── P1Doks_xxx_R.sto
```

De esta forma todos los setups quedan organizados por:

* Vehículo
* Temporada
* Serie
* Circuito

---

# Configuración inicial

Antes de ejecutar el sincronizador es necesario editar el archivo `config.json` y configurar los siguientes parámetros:

```json
{
    "bearer_token": "TU_TOKEN_DE_P1DOKS",
    "user_id": "TU_USER_ID",
    "year": 2026,
    "season": 3,
    "week": 2,
    "download_profile": "DAY1",
    "max_downloads_per_day": 24
}
```

## Parámetros

### bearer_token

Token de autenticación utilizado para acceder a la API de P1Doks.

Puede obtenerse iniciando sesión en la web de P1Doks y capturando el token Bearer desde las herramientas de desarrollo del navegador (Network → Authorization).

---

### user_id

Identificador del usuario de P1Doks.

Se utiliza durante la descarga de los Data Packs y puede obtenerse igualmente inspeccionando las peticiones realizadas por la aplicación web.

---

### year

Año de la temporada de iRacing que se desea descargar.

Ejemplo:

```json
"year": 2026
```

---

### season

Temporada de iRacing.

Valores posibles:

* 1
* 2
* 3
* 4

Ejemplo:

```json
"season": 3
```

---

### week

Semana de la temporada que se desea descargar.

Ejemplo:

```json
"week": 2
```

---

### download_profile

Perfil de descarga.

Valores disponibles:

#### DAY1

Descarga únicamente los setups prioritarios definidos en el proyecto:

* IMSA GT3
* GT Sprint GT3
* IMSA GTP
* LMP2
* Porsche Cup
* GT4
* Super Formula
* Super Formula Lights

Pensado para descargar únicamente los setups más utilizados.

---

#### DAY2

Descarga automáticamente todos los Data Packs que **no forman parte del perfil DAY1**.

No requiere configuración adicional y se calcula automáticamente en tiempo de ejecución.

---

### max_downloads_per_day

Número máximo de descargas permitidas durante una ejecución.

Por defecto:

```json
"max_downloads_per_day": 24
```

Este límite existe para evitar posibles restricciones de descarga por parte de la plataforma P1Doks.


---

# Perfiles de descarga

Los perfiles se definen en `selection.py`.

Ejemplo del perfil DAY1:

* IMSA GT3 → 6 coches
* GT Sprint GT3 → 8 coches
* IMSA GTP → 3 coches
* LMP2 → 1 coche
* Porsche Cup → 1 coche
* GT4 → 3 coches
* Super Formula → 1 coche
* Super Formula Lights → 1 coche

Esto permite priorizar las categorías más utilizadas sin necesidad de descargar todos los setups disponibles.

---

# Ejecución

Activar el entorno virtual:

```bash
venv\Scripts\activate
```

Ejecutar el sincronizador:

```bash
python main.py
```

El programa descargará automáticamente los nuevos Data Packs y los dejará organizados en la carpeta correspondiente de iRacing.

---

# Tecnologías utilizadas

* Python 3
* Requests
* ZipFile
* Pathlib
* JSON

---

# Mejoras previstas

* Descarga automática mediante login (sin Bearer Token manual).
* Actualización incremental.
* Interfaz gráfica.
* Registro de logs.
* Configuración mediante fichero YAML.
* Descarga paralela de Data Packs.
* Sincronización automática por calendario de iRacing.

---

# Autor

Proyecto desarrollado para automatizar la gestión de setups de P1Doks e integrarlos de forma local con iRacing y Garage61.

