#!/usr/bin/env python3
"""Verify the successor manifest and deterministic ZIP without extraction."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MANIFEST.sha256"
ARCHIVE = ROOT / "point-span-tangent-absorption-successor-v0.1.zip"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    failures: list[str] = []
    manifest_entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        manifest_entries[relative] = expected
        path = ROOT / PurePosixPath(relative)
        if not path.is_file():
            failures.append(f"missing payload file: {relative}")
        elif digest(path.read_bytes()) != expected:
            failures.append(f"manifest mismatch: {relative}")

    expected_names = sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path != ARCHIVE
        and "__pycache__" not in path.parts
    )
    with zipfile.ZipFile(ARCHIVE) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            failures.append("duplicate ZIP member")
        if sorted(names) != expected_names:
            failures.append("ZIP member list differs from package payload")
        for info in infos:
            relative = PurePosixPath(info.filename)
            if relative.is_absolute() or ".." in relative.parts:
                failures.append(f"unsafe ZIP path: {info.filename}")
            if info.date_time != FIXED_ZIP_TIME:
                failures.append(f"nonfixed ZIP timestamp: {info.filename}")
            current = ROOT / relative
            if current.is_file() and digest(archive.read(info)) != digest(
                current.read_bytes()
            ):
                failures.append(f"ZIP content mismatch: {info.filename}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "manifest_entries": len(manifest_entries),
        "zip_entries": len(expected_names),
        "fixed_timestamps": not any("timestamp" in item for item in failures),
        "failures": failures,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
