# Arquitectura del proyecto

## Componentes

- `etl/`: descarga, transformacion, validacion y escritura de datos procesados.
- `api/`: servicio REST con FastAPI para consultar datasets procesados.
- `dashboard/`: dashboard interactivo con Streamlit y Plotly.
- `tests/`: pruebas automatizadas de transformaciones y validaciones.
- `docker/`: imagen base para ejecutar API y dashboard en contenedores.
- `data/raw/`: datos originales descargados desde KaggleHub.
- `data/processed/`: salidas curadas del pipeline ETL.

## Flujo

1. `etl.extract.download_kaggle` descarga las tres fuentes configuradas.
2. `etl.transform.pipeline` descubre archivos CSV/Excel en `data/raw`.
3. Cada archivo se normaliza, se valida y se guarda como Parquet en `data/processed`.
4. La API y el dashboard leen exclusivamente desde `data/processed`.
5. El dashboard presenta tres modulos independientes para evitar forzar una relacion artificial entre fuentes con dominios distintos.

## Decisiones de alcance

El equipo definio una separacion por modulos y una audiencia principal docente/evaluadora. Las visualizaciones priorizan trazabilidad tecnica, limpieza de datos, metricas descriptivas y facilidad para demostrar el pipeline end-to-end.
