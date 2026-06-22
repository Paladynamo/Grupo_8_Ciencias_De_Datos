# Grupo 8 - Ciencias de Datos

Evaluacion Parcial N3 - Programacion para la Ciencia de Datos (SCY1101).

Proyecto grupal end-to-end con integracion de datos, pipeline ETL, API REST, dashboard interactivo, pruebas automatizadas, Docker y evidencia de trabajo colaborativo en Git.

El dashboard esta organizado en tres modulos independientes orientados a una presentacion docente/evaluadora:

- Pokemon competitivo.
- Terremotos en Chile.
- Mercado de cartas Yu-Gi-Oh.

## Fuentes de datos

- Pokemon competitivo: `giorgiocarbone/complete-competitive-pokmon-datasets-may-2022`
- Terremotos en Chile: `nicolasgonzalezmunoz/earthquakes-on-chile`
- Cartas Yu-Gi-Oh!: `hammadus/yugioh-full-card-database-index-august-1st-2025`

## Estructura

```text
api/                API REST con FastAPI
dashboard/          Dashboard Streamlit + Plotly
docker/             Dockerfile del proyecto
docs/               Documentacion tecnica, arquitectura y despliegue
etl/                Extraccion, transformacion, validacion y carga
scripts/            Entradas auxiliares de ejecucion
tests/              Pruebas automatizadas
data/raw/           Datos originales descargados localmente
data/processed/     Datos procesados en Parquet
```

Los datos no se suben al repositorio. Se regeneran desde KaggleHub con los comandos de ETL.

## Revision con Docker

Este es el flujo recomendado para que el docente revise el proyecto sin instalar dependencias Python manualmente.

### Requisitos

- Docker Desktop instalado y en ejecucion.
- Conexion a internet para descargar datasets.
- Puertos libres: `8000` para API y `8501` para dashboard.

### 1. Construir imagen

```bash
docker compose build
```

### 2. Descargar datasets

```bash
docker compose run --rm etl-download
```

Este paso descarga las tres fuentes desde KaggleHub y copia los archivos a `data/raw`.

### 3. Ejecutar pipeline ETL

```bash
docker compose run --rm etl-transform
```

Este paso normaliza columnas, aplica conversiones por modulo, valida reglas minimas de calidad y genera archivos Parquet en `data/processed`.

### 4. Ejecutar pruebas

```bash
docker compose run --rm tests
```

### 5. Levantar API y dashboard

```bash
docker compose up
```

Abrir en el navegador:

- Dashboard: <http://localhost:8501>
- API REST: <http://localhost:8000>
- Documentacion Swagger/OpenAPI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

Para detener los servicios:

```bash
docker compose down
```

## Flujo rapido para revision docente

```bash
docker compose build
docker compose run --rm etl-download
docker compose run --rm etl-transform
docker compose run --rm tests
docker compose up
```

## Instalacion local sin Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Descargar datos:

```bash
python -m etl.extract.download_kaggle
```

Ejecutar ETL:

```bash
python -m etl.transform.pipeline
```

Levantar API:

```bash
uvicorn api.main:app --reload
```

Levantar dashboard:

```bash
streamlit run dashboard/app.py
```

Ejecutar pruebas:

```bash
python -m pytest
```

## API REST

Endpoints iniciales:

- `GET /health`
- `GET /datasets`
- `GET /datasets/{dataset_name}?limit=50`

## Dashboard

Modulos disponibles:

- Pokemon competitivo: atributos, tipos, uso competitivo y combinaciones de equipo.
- Terremotos en Chile: magnitud, profundidad, evolucion temporal y distribucion geografica.
- Yu-Gi-Oh mercado: tipos de cartas, precios por rareza, lanzamientos y cartas de mayor valor.

## Documentacion adicional

- [Arquitectura](docs/arquitectura.md)
- [Documentacion de API REST](docs/api.md)
- [Guia de despliegue](docs/guia_despliegue.md)
- [Manual de usuario](docs/manual_usuario.md)
- [Preguntas y decisiones pendientes](docs/preguntas_pendientes.md)
