"""Convenience entry point for the ETL pipeline."""

from etl.transform.pipeline import run_pipeline


if __name__ == "__main__":
    run_pipeline()
