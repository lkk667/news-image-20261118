#!/usr/bin/env python3
"""Copy the entry image to the make.fun output directory.

The entry is a single image, entry.png, stored next to this script.
Running this program copies that image to
$MAKEFUN_OUTPUT_DIR/entry.png, creating the output directory
if it does not already exist.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    if not source.is_file():
        print(f"error: entry image not found: {source}", file=sys.stderr)
        return 1
    destination = Path(out_dir) / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if sha256_file(source) != sha256_file(destination):
        print("error: copied output does not match the entry image", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
