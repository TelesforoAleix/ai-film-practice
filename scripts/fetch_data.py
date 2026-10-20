#!/usr/bin/env python3
"""Download and verify the frozen release (HTTPS publicly; gh for private access)."""

import argparse
import hashlib
import os
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from film_practice import TABLES

REPOSITORY = "TelesforoAleix/ai-film-practice"
RELEASE = "data-2026-10-20"
ASSETS = frozenset(
    f"{name}{suffix}" for name in TABLES for suffix in (".parquet", ".csv.gz")
)


def read_manifest(path: Path) -> dict[str, str]:
    checksums = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        if not match:
            raise ValueError("Invalid SHA256SUMS entry")
        digest, name = match.groups()
        if name not in ASSETS or name in checksums:
            raise ValueError("Unexpected or duplicate SHA256SUMS asset")
        checksums[name] = digest
    if checksums.keys() != ASSETS:
        raise ValueError("SHA256SUMS must cover all 28 data assets exactly once")
    return checksums


def verify(folder: Path, checksums: dict[str, str]) -> None:
    for name, expected in checksums.items():
        digest = hashlib.sha256()
        with (folder / name).open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != expected:
            raise ValueError(f"Checksum mismatch: {name}")


def download_asset(name: str, destination: Path, transport: str) -> None:
    if transport == "gh":
        subprocess.run(
            [
                "gh",
                "release",
                "download",
                RELEASE,
                "--repo",
                REPOSITORY,
                "--pattern",
                name,
                "--dir",
                str(destination),
            ],
            check=True,
        )
    else:
        url = f"https://github.com/{REPOSITORY}/releases/download/{RELEASE}/{name}"
        with urllib.request.urlopen(url, timeout=120) as response:
            with (destination / name).open("wb") as out:
                while block := response.read(1024 * 1024):
                    out.write(block)


def fetch(output: Path, transport: str = "https") -> dict[str, str]:
    output.mkdir(parents=True, exist_ok=True)
    # Verify the entire download before replacing any destination files.
    with tempfile.TemporaryDirectory(prefix=".download-", dir=output) as temporary:
        staging = Path(temporary)
        download_asset("SHA256SUMS", staging, transport)
        checksums = read_manifest(staging / "SHA256SUMS")
        for name in sorted(checksums):
            download_asset(name, staging, transport)
        verify(staging, checksums)
        for name in [*sorted(checksums), "SHA256SUMS"]:
            os.replace(staging / name, output / name)
    return checksums


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data"))
    parser.add_argument("--transport", choices=("https", "gh"), default="https")
    args = parser.parse_args()
    checksums = fetch(args.output, args.transport)
    print(f"Verified all {len(checksums)} data assets against SHA256SUMS.")


if __name__ == "__main__":
    main()
