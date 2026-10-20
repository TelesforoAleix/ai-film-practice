"""DuckDB views over the immutable, privacy-redacted research snapshot."""

from pathlib import Path

import duckdb

TABLES = (
    "films",
    "priority_films",
    "folders",
    "generations",
    "generation_prompts",
    "assets",
    "asset_usages",
    "asset_folders",
    "generation_folders",
    "reference_elements",
    "brief_assets",
    "model_usage",
    "extraction_log",
    "other_items",
)


def connect(data_dir: str | Path = "data") -> duckdb.DuckDBPyConnection:
    """Open an in-memory connection with one view per published table.

    All files are required. Values remain VARCHAR or NULL; typing belongs to studies.
    Use ``connection.sql(...).df()`` for pandas, and close the connection when done.
    """
    root = Path(data_dir).resolve()
    missing = [name for name in TABLES if not (root / f"{name}.parquet").is_file()]
    if missing:
        raise FileNotFoundError("Missing Parquet tables: " + ", ".join(missing))
    connection = duckdb.connect()
    try:
        for name in TABLES:
            path = str(root / f"{name}.parquet").replace("'", "''")
            connection.execute(
                f"CREATE VIEW \"{name}\" AS SELECT * FROM read_parquet('{path}')"
            )
    except Exception:
        connection.close()
        raise
    return connection
