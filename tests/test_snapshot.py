"""Synthetic fixtures only; no archived prompts or records."""

import csv
import gzip
import hashlib
import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from film_practice import TABLES, connect
from scripts.build_parquet import EMAIL, build_table, redact, redacted_csv_gzip
from scripts.fetch_data import ASSETS, fetch, read_manifest, verify


def synthetic_email():
    # Construct a reserved-domain fixture; never persist an address in a test file/log.
    return "fixture" + chr(64) + "example.invalid"


def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(rows)


def test_strings_null_empty_multiline_json_and_long_prompts(tmp_path):
    source = tmp_path / "fixture.csv"
    address = synthetic_email()
    rows = [
        [r"\N", "", "001", 'a,"b"\nsecond line', json.dumps({"nested": "001"})],
        ["NULL", "null", "NaN", "z" * 60000, " " + address + " "],
        ["true", "1.50", "2026-10-20", "é漢字", "end"],
    ]
    columns = ["a", "b", "c", "prompt", "json"]
    write_csv(source, columns, rows)
    parquet = tmp_path / "fixture.parquet"
    result = build_table(source, parquet, batch_size=1)
    table = pq.read_table(parquet)
    assert all(field.type == pa.string() for field in table.schema)
    assert table.to_pylist() == [
        {
            name: None if value == r"\N" else redact(value)
            for name, value in zip(columns, row, strict=True)
        }
        for row in rows
    ]
    assert result["columns"]["a"]["csv_null"] == 1
    assert result["columns"]["b"]["parquet_empty"] == 1
    assert result["columns"]["json"]["email_occurrences_redacted"] == 1


def test_gzip_preserves_bytes_except_emails(tmp_path):
    source = tmp_path / "fixture.csv"
    original = ('a,b\r\n"c\n' + synthetic_email() + '",é\r\n').encode()
    source.write_bytes(original)
    gzip_path = tmp_path / "fixture.csv.gz"
    digest, counts = redacted_csv_gzip(source, gzip_path)
    expected = redact(original.decode()).encode()
    assert gzip.decompress(gzip_path.read_bytes()) == expected
    assert digest == hashlib.sha256(expected).hexdigest()
    assert counts["email"] == 1
    assert source.read_bytes() == original


def test_redaction_ignores_versions_and_handles():
    assert redact("package@13.6.33 https://site.invalid/@handle") == (
        "package@13.6.33 https://site.invalid/@handle"
    )
    assert EMAIL.fullmatch(synthetic_email())
    assert redact(synthetic_email()) == "[email removed]"


def test_path_and_phone_redaction_preserves_json_and_csv_bytes(tmp_path):
    # Generated references are synthetic, not source corpus paths or contacts.
    path = "~" + "/fixture/still.png"
    mounted = "/" + "mnt/fixture/prompt.md"
    phone = "+1" + "202" + "555" + "0123"
    payload = json.dumps({"file": path, "phone": phone, "other": mounted})
    source = tmp_path / "fixture.csv"
    write_csv(source, ["text"], [[payload]])
    result = build_table(source, tmp_path / "fixture.parquet")
    values = json.loads(pq.read_table(tmp_path / "fixture.parquet")["text"][0].as_py())
    assert values == {
        "file": "[local path removed]",
        "phone": "[phone removed]",
        "other": "[local path removed]",
    }
    assert result["columns"]["text"]["local_path_occurrences_redacted"] == 2
    assert result["columns"]["text"]["phone_occurrences_redacted"] == 1
    _, counts = redacted_csv_gzip(source, tmp_path / "fixture.csv.gz")
    assert counts["local_path"] == 2
    assert counts["phone"] == 1
    # csv.writer used CRLF; read_text normalizes it, so compare with newline=''.
    with source.open(newline="") as stream:
        expected = redact(stream.read()).encode()
    assert gzip.decompress((tmp_path / "fixture.csv.gz").read_bytes()) == expected


def test_generation_integrity_hashes_and_compound_keys(tmp_path):
    source = tmp_path / "generations.csv"
    write_csv(
        source,
        ["film_id", "generation_id", "prompt"],
        [
            ["f1", "same", r"\N"],
            ["f2", "same", ""],
            ["f2", "next", "001\ntext"],
        ],
    )
    result = build_table(source, tmp_path / "g.parquet", batch_size=1)
    metrics = result["generations"]
    assert metrics["distinct_compound_keys"] == 3
    assert metrics["nonempty_primary_prompts"] == 1
    assert metrics["explicitly_empty_primary_prompts"] == 1
    assert (
        metrics["ordered_redacted_csv_prompt_sha256"]
        == (metrics["ordered_parquet_prompt_sha256"])
    )
    write_csv(
        source,
        ["film_id", "generation_id", "prompt"],
        [
            ["f1", "same", "a"],
            ["f1", "same", "b"],
        ],
    )
    with pytest.raises(ValueError, match="Duplicate compound"):
        build_table(source, tmp_path / "duplicate.parquet")


def test_query_views_and_dataframe(tmp_path):
    root = tmp_path / "quoted'folder"
    root.mkdir()
    for name in TABLES:
        pq.write_table(
            pa.table({"film_id": ["001", None, ""]}), root / f"{name}.parquet"
        )
    with connect(root) as connection:
        assert connection.sql("SELECT count(*) FROM generations").fetchone() == (3,)
        assert (
            connection.sql("SELECT film_id FROM films").df()["film_id"].iloc[0] == "001"
        )
        assert len(connection.sql("SHOW TABLES").fetchall()) == 14
    (root / "films.parquet").unlink()
    with pytest.raises(FileNotFoundError, match="films"):
        connect(root)


def fixture_manifest(folder):
    digest = hashlib.sha256(b"synthetic").hexdigest()
    for name in ASSETS:
        (folder / name).write_bytes(b"synthetic")
    (folder / "SHA256SUMS").write_text(
        "".join(f"{digest}  {name}\n" for name in sorted(ASSETS))
    )


def test_manifest_and_tamper_detection(tmp_path):
    fixture_manifest(tmp_path)
    sums = read_manifest(tmp_path / "SHA256SUMS")
    verify(tmp_path, sums)
    (tmp_path / "films.parquet").write_bytes(b"changed")
    with pytest.raises(ValueError, match="Checksum mismatch"):
        verify(tmp_path, sums)
    for text in ["", "0" * 64 + "  ../escape\n", "bad manifest\n"]:
        (tmp_path / "SHA256SUMS").write_text(text)
        with pytest.raises(ValueError):
            read_manifest(tmp_path / "SHA256SUMS")


def test_fetch_verifies_before_replacing_destination(tmp_path, monkeypatch):
    remote = tmp_path / "remote"
    remote.mkdir()
    fixture_manifest(remote)

    def download(name, destination, transport):
        (destination / name).write_bytes((remote / name).read_bytes())

    monkeypatch.setattr("scripts.fetch_data.download_asset", download)
    destination = tmp_path / "download"
    assert len(fetch(destination)) == 28
    (destination / "films.parquet").write_bytes(b"previous")
    (remote / "films.parquet").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="Checksum mismatch"):
        fetch(destination)
    assert (destination / "films.parquet").read_bytes() == b"previous"
    assert not list(destination.glob(".download-*"))
