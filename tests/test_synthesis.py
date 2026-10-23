"""Findings synthesis: synthetic helpers, committed citations, optional rebuild."""

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "synthesis"
spec = importlib.util.spec_from_file_location("synthesis_build", HERE / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
RELEASES = [
    ROOT / "data/prompt-labels-v1",
    ROOT / "data/prompt-labels-v2",
    ROOT / "data/study-07-v1",
]


def test_zero_denominator_is_unavailable_not_zero():
    row = build.share_summary("m", "image", None, 3, [1, 0, 5], [2, 0, 0], "")
    assert row["measured_films"] == 1
    assert row["equal_film_mean"] == 0.5
    assert row["pooled_share"] == 0.5
    empty = build.share_summary("m", "image", None, 1, [0], [0], "")
    assert empty["equal_film_mean"] is None
    assert empty["pooled_share"] is None


def test_share_table_weights_films_equally_and_counts_ties():
    counts = pd.DataFrame(
        {
            "film_id": ["a", "a", "b", "b"],
            "stage": ["s"] * 4,
            "model_identifier": ["x", "y", "x", "y"],
            "jobs": [9, 1, 1, 1],
        }
    )
    table = build.share_table(counts, "stage", "model_identifier", 2)
    table = table.set_index("model_identifier")
    assert table.loc["x", "equal_film_mean"] == pytest.approx((0.9 + 0.5) / 2)
    assert table.loc["x", "pooled_share"] == pytest.approx(10 / 12)
    assert table.loc["x", "top_films"] == 2
    assert table.loc["y", "top_films"] == 1


def test_pairs_compare_within_films_that_have_the_given_trait():
    first = np.array([[2, 1], [1, 1]], dtype=float)
    second = np.array([[0, 0], [0, 3]], dtype=float)
    rows = build.pair_rows([(first, 4.0), (second, 3.0)], ["a", "b"], "image", False)
    given_a = next(r for r in rows if r["given"] == "a")
    assert given_a["films_with_given"] == 1
    assert given_a["mean_share_given"] == 0.5
    assert given_a["mean_share_same_films"] == 0.25
    given_b = next(r for r in rows if r["given"] == "b")
    assert given_b["films_with_given"] == 2
    assert given_b["mean_share_given"] == 0.5


def test_release_verification_rejects_changed_assets(tmp_path):
    (tmp_path / "asset.bin").write_bytes(b"synthetic")
    value = hashlib.sha256(b"synthetic").hexdigest()
    (tmp_path / "SHA256SUMS").write_text(f"{value}  asset.bin\n")
    build.verify_release(tmp_path, expected_assets={"asset.bin": value})
    with pytest.raises(ValueError):
        build.verify_release(tmp_path, expected_manifest="0" * 64)
    (tmp_path / "asset.bin").write_bytes(b"changed")
    with pytest.raises(ValueError):
        build.verify_release(tmp_path)


def test_citations_use_literal_selectors_and_reject_disagreement(tmp_path):
    (tmp_path / "x.csv").write_text("metric,task,value\nm,image,0.25\nm,video,\\N\n")
    number = {
        "id": "c1",
        "label": "synthetic",
        "file": "synthesis/outputs/x.csv",
        "where": {"metric": "m", "task": "image"},
        "column": "value",
        "value": 0.25,
        "round": 4,
        "format": "pct",
    }
    counted = dict(number, id="c2", where={"metric": "m"}, aggregate="count")
    counted.update(value=2, round=0, format="int")
    points = {"points": [{"id": "P", "numbers": [number, counted]}]}
    table = build.citations(points, tmp_path)
    assert table.display.tolist() == ["25.00%", "2"]
    number["value"] = 0.3
    with pytest.raises(ValueError):
        build.citations(points, tmp_path)
    number.update(value=0.25, where={"metric": "m"})
    with pytest.raises(ValueError):
        build.citations(points, tmp_path)
    with pytest.raises(ValueError):
        build.fill("{{missing}}", {})


def test_committed_outputs_and_inputs_match_manifest():
    manifest = json.loads((HERE / "outputs/reproduction.json").read_text())
    assert set(manifest["outputs"]) == {
        p.name for p in build.listed(HERE / "outputs")
    } - {"reproduction.json"}
    for name, expected in manifest["outputs"].items():
        path = HERE / "outputs" / name
        assert build.digest(path) == expected, name
        assert path.stat().st_size < 1_000_000
    for name, expected in manifest["inputs"].items():
        assert build.digest(ROOT / name) == expected, name


def test_committed_citations_register_and_readme_reproduce(tmp_path):
    points = json.loads((HERE / "points.json").read_text())
    build.check_points(points)
    table = build.citations(points, HERE / "outputs")
    build.write(table, tmp_path / "citations.csv")
    build.write(build.point_register(points, table), tmp_path / "points.csv")
    for name in ["citations.csv", "points.csv"]:
        committed = (HERE / "outputs" / name).read_bytes()
        assert (tmp_path / name).read_bytes() == committed, name
    text = build.readme(points, build.read_strings(HERE / "outputs/citations.csv"))
    assert text == (HERE / "README.md").read_text()
    assert "{{" not in text


def test_outputs_hold_no_long_texts_emails_or_local_paths():
    files = [*build.listed(HERE / "outputs"), *HERE.glob("*.md"), HERE / "points.json"]
    email = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
    local = [str(Path.home()), str(ROOT)]
    for path in files:
        text = path.read_text()
        assert not email.search(text), path.name
        assert not any(prefix in text for prefix in local), path.name
        if path.suffix == ".csv":
            cells = build.read_strings(path).to_numpy().ravel()
            assert max(len(c) for c in cells) < 1000, path.name


def test_build_reproduces_committed_outputs(tmp_path):
    """Runs after downloading the three releases; CI without them skips."""
    if not all((p / "SHA256SUMS").is_file() for p in RELEASES):
        pytest.skip("Download prompt-labels-v1, -v2 and study-07-v1 into data/")
    subprocess.run(
        [
            sys.executable,
            str(HERE / "build.py"),
            "--v1",
            str(RELEASES[0]),
            "--v2",
            str(RELEASES[1]),
            "--study07",
            str(RELEASES[2]),
            "--output",
            str(tmp_path),
            "--check",
        ],
        cwd=ROOT,
        check=True,
    )
