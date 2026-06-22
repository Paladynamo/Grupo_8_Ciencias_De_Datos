# Documentacion de API REST

La API esta implementada con FastAPI y expone los datos procesados desde `data/processed`.

## Ejecucion

Con Docker:

```bash
docker compose up api
```

Local:

```bash
uvicorn api.main:app --reload
```

## URLs

- API: <http://localhost:8000>
- Swagger/OpenAPI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

## Endpoints

### `GET /health`

Verifica que el servicio este disponible.

Respuesta esperada:

```json
{"status": "ok"}
```

### `GET /datasets`

Lista los archivos Parquet procesados disponibles para consulta.

### `GET /datasets/{dataset_name}?limit=50`

Devuelve una muestra de registros del dataset solicitado.

Datasets disponibles:

- `pokemon`
- `earthquakes_chile`
- `yugioh`

Ejemplo:

```bash
curl "http://localhost:8000/datasets/pokemon?limit=10"
```
