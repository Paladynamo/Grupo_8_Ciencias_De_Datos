"""FastAPI service exposing processed project datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

from etl.config import get_settings

app = FastAPI(
    title="Grupo 8 Ciencias de Datos API",
    version="0.1.0",
    description="API REST para consultar datasets procesados del proyecto.",
)


def list_processed_files() -> list[Path]:
    """Return processed Parquet files available to the API."""

    settings = get_settings()
    return sorted(settings.processed_dir.rglob("*.parquet"))


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""

    return {"status": "ok"}


@app.get("/datasets")
def datasets() -> list[dict[str, str]]:
    """List processed datasets and files."""

    settings = get_settings()
    return [
        {
            "dataset": path.relative_to(settings.processed_dir).parts[0],
            "file": path.name,
            "relative_path": str(path.relative_to(settings.processed_dir)),
        }
        for path in list_processed_files()
    ]


@app.get("/datasets/{dataset_name}")
def dataset_preview(
    dataset_name: str,
    limit: int = Query(default=50, ge=1, le=500),
) -> list[dict[str, object]]:
    """Return a preview for all processed files belonging to one dataset."""

    settings = get_settings()
    dataset_dir = settings.processed_dir / dataset_name
    if not dataset_dir.exists():
        raise HTTPException(status_code=404, detail=f"Dataset not found: {dataset_name}")

    frames = [pd.read_parquet(path).head(limit) for path in sorted(dataset_dir.glob("*.parquet"))]
    if not frames:
        raise HTTPException(status_code=404, detail=f"No processed files for dataset: {dataset_name}")

    preview = pd.concat(frames, ignore_index=True).head(limit)
    return preview.where(pd.notnull(preview), None).to_dict(orient="records")
