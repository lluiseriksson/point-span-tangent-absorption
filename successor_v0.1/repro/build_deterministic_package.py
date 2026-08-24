#!/usr/bin/env python3
"""Build the successor manifest, metadata report, and deterministic ZIP."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from pypdf import PdfReader


FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
ZIP_NAME = "point-span-tangent-absorption-successor-v0.1.zip"
EXCLUDED_NAMES = {"MANIFEST.sha256", "BUILD_REPORT.json", ZIP_NAME}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def files_under(root: Path, exclusions: set[str]) -> list[Path]:
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.name not in exclusions
            and "__pycache__" not in path.parts
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def write_build_report(root: Path) -> None:
    files = files_under(root, EXCLUDED_NAMES)
    report = {
        "package": "point-span-tangent-absorption-successor-v0.1",
        "paper_pages": len(PdfReader(str(root / "paper.pdf")).pages),
        "scope": (
            "File metadata before BUILD_REPORT.json, MANIFEST.sha256, and the "
            "ZIP itself are generated."
        ),
        "files": [
            {
                "path": path.relative_to(root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }
    (root / "BUILD_REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_manifest(root: Path) -> None:
    files = files_under(root, {"MANIFEST.sha256", ZIP_NAME})
    lines = [
        f"{sha256(path)}  {path.relative_to(root).as_posix()}" for path in files
    ]
    (root / "MANIFEST.sha256").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def write_zip(root: Path) -> Path:
    destination = root / ZIP_NAME
    files = files_under(root, {ZIP_NAME})
    with zipfile.ZipFile(
        destination,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in files:
            info = zipfile.ZipInfo(
                path.relative_to(root).as_posix(), date_time=FIXED_ZIP_TIME
            )
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    return destination


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    write_build_report(root)
    write_manifest(root)
    archive = write_zip(root)
    result = {
        "status": "PASS",
        "zip": archive.name,
        "zip_size_bytes": archive.stat().st_size,
        "zip_sha256": sha256(archive),
        "manifest_entries": len(
            (root / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
