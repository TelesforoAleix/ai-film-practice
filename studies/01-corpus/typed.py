"Optional typed views beside the immutable string views, driven by the dictionary."

import csv
from pathlib import Path


def add_typed_views(connection, dictionary_path: Path):
    """Add typed_<table>; raw string views remain unchanged.

    Each field gains __empty and __invalid flags. Raw nulls remain unavailable.
    Empty scalar values are null in the typed projection, with an empty flag;
    VARCHAR retains empty text. Invalid JSON is never repaired.
    """
    tables = {}
    with dictionary_path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            tables.setdefault(row["table"], []).append(row)
    for table, rows in tables.items():
        expressions = []
        for row in rows:
            name, typ = row["column"], row["derived_type"]
            if (
                not name.replace("_", "").isalnum()
                or not table.replace("_", "").isalnum()
            ):
                raise ValueError("Unsafe identifier")
            if typ not in {
                "VARCHAR",
                "BIGINT",
                "DOUBLE",
                "BOOLEAN",
                "TIMESTAMPTZ",
                "JSON",
            }:
                raise ValueError("Unsupported derived type")
            col = f'"{name}"'
            cast = f"try_cast(nullif({col}, '') AS {typ})"
            # VARCHAR preserves empty text; a flag still makes it explicit.
            if typ == "VARCHAR":
                cast = col
            expressions.extend(
                [
                    f"{cast} AS {col}",
                    f"({col} = '') AS \"{name}__empty\"",
                    f"({col} IS NOT NULL AND {col} <> '' AND {cast} IS NULL) "
                    f'AS "{name}__invalid"',
                ]
            )
        connection.execute(
            f'CREATE OR REPLACE TEMP VIEW "typed_{table}" AS SELECT '
            + ",".join(expressions)
            + f' FROM "{table}"'
        )
