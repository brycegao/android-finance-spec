#!/usr/bin/env python3
"""Sync root specs into the installable skill reference bundle."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "specs"
REFERENCES = ROOT / "skills" / "android-finance-spec" / "references"

FILES = [
    "finance-number-skill.md",
    "rtl-adaption.md",
    "kotlin-style.md",
]


def main() -> int:
    REFERENCES.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        source = SPECS / name
        target = REFERENCES / name
        if not source.exists():
            raise SystemExit(f"Missing spec: {source}")
        shutil.copyfile(source, target)
        print(f"synced {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
