#!/usr/bin/env python3
"""Build the ChatGPT-uploadable random-yao skill bundle."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "chatgpt" / "random-yao"
OUTPUT = ROOT / "dist" / "random-yao-chatgpt.zip"
TOP = "random-yao"


def main() -> int:
    if not (SOURCE / "SKILL.md").is_file():
        raise SystemExit(f"missing skill manifest: {SOURCE / 'SKILL.md'}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    files = [
        path for path in SOURCE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and not path.name.endswith(".pyc")
    ]

    skill_manifests = [path for path in files if path.name.lower() == "skill.md"]
    if len(skill_manifests) != 1:
        raise SystemExit(
            f"bundle must contain exactly one SKILL.md; found {len(skill_manifests)}"
        )

    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(files):
            relative = path.relative_to(SOURCE)
            archive.write(path, Path(TOP) / relative)

    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
