#!/usr/bin/env python3
"""Check tracked-file publication boundaries, including files staged locally."""

import hashlib
import json
import subprocess
from pathlib import Path


def main() -> None:
    names = subprocess.check_output(["git", "ls-files", "-z"]).split(b"\0")
    errors = []
    for raw in names:
        if not raw:
            continue
        name = raw.decode("utf-8")
        path = Path(name)
        if name == "data" or name.startswith("data/"):
            errors.append(f"Data is tracked: {name}")
        if path.is_file() and path.stat().st_size > 5_000_000:
            errors.append(f"Tracked file exceeds 5 MB: {name}")
    originals = json.loads(Path("validation/original-verification.json").read_text())
    for name, expected in originals.items():
        path = Path("original") / name
        if (
            hashlib.sha256(path.read_bytes()).hexdigest()
            != expected["published_sha256"]
        ):
            errors.append(f"Preserved original changed: {name}")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Tracked files: none over 5 MB; nothing under data/; original hashes match.")


if __name__ == "__main__":
    main()
