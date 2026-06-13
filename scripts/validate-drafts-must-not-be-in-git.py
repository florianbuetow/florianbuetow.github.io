#!/usr/bin/env python3
"""Fail if any git-tracked Markdown file has draft: true in its front matter."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import re

DRAFT_RE = re.compile(r"^draft:\s*true\s*$", re.MULTILINE)
FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def tracked_md_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.md", "**/*.md"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        Path(p)
        for p in result.stdout.splitlines()
        if p and not p.startswith("archetypes/")
    ]


def is_draft(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return False
    return bool(DRAFT_RE.search(m.group(1)))


def main() -> int:
    errors: list[str] = []
    for path in tracked_md_files():
        if is_draft(path):
            errors.append(str(path))

    for f in errors:
        print(f"ERROR: {f} is a draft document and must not be tracked by git", file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
