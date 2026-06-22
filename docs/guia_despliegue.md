# Guia de despliegue y revision

## Requisitos

- Docker Desktop instalado y en ejecucion.
- Conexion a internet para descargar datasets desde KaggleHub.
- Puertos libres: `8000` para API y `8501` para dashboard.

## Ejecucion con Docker

```bash
docker compose build
docker compose run --rm etl-download
docker compose run --rm etl-transform
docker compose run --rm tests
docker compose up
```

## URLs

- Dashboard: <http://localhost:8501>
- API REST: <http://localhost:8000>
- Swagger/OpenAPI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

## Datos

Los datos originales y procesados no se suben al repositorio para evitar archivos pesados. Se regeneran con los servicios `etl-download` y `etl-transform`.

## Solucion de problemas

- Si `localhost:8501` o `localhost:8000` no abre, verificar que Docker Desktop este corriendo.
- Si un puerto esta ocupado, cambiar el mapeo en `docker-compose.yml`.
- Si el dashboard aparece sin datos, ejecutar nuevamente `docker compose run --rm etl-transform`.
