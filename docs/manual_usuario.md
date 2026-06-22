# Manual de usuario del dashboard

## Acceso

Con Docker:

```bash
docker compose up dashboard
```

Luego abrir <http://localhost:8501>.

## Modulos

### Pokemon competitivo

Permite revisar:

- Cantidad de Pokemon registrados.
- Distribucion por tipo primario.
- Relacion entre ataque y velocidad.
- Ranking de uso competitivo.
- Combinaciones frecuentes de equipo.

### Terremotos en Chile

Permite revisar:

- Cantidad de eventos sismicos.
- Magnitud maxima.
- Profundidad media.
- Distribucion de magnitudes.
- Relacion entre profundidad y magnitud.
- Evolucion temporal y distribucion geografica.

### Yu-Gi-Oh mercado

Permite revisar:

- Cantidad de registros de mercado.
- Cartas unicas.
- Precio maximo.
- Distribucion por tipo de carta.
- Precio mediano por rareza.
- Cartas de mayor valor.

## Requisitos previos

Antes de abrir el dashboard, ejecutar:

```bash
docker compose run --rm etl-download
docker compose run --rm etl-transform
```

Si no existen datos procesados, el dashboard mostrara un mensaje solicitando ejecutar el ETL.
