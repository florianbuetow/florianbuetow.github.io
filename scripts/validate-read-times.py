#!/usr/bin/env python3
"""Fail if any git-tracked published article is missing its readTime front matter field."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ANSI_RED = "\033[0;31m"
ANSI_GREEN = "\033[0;32m"
ANSI_RESET = "\033[0m"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
DRAFT_RE = re.compile(r"^draft:\s*true\s*$", re.MULTILINE)
READ_TIME_RE = re.compile(r"^readTime:", re.MULTILINE)


def tracked_md_files(dirs: list[str]) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.md", "**/*.md"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        Path(p)
        for p in result.stdout.splitlines()
        if p
        and any(p.startswith(d.rstrip("/") + "/") for d in dirs)
        and Path(p).name != "_index.md"
    ]


def parse_front_matter(text: str) -> str | None:
    m = FRONT_MATTER_RE.match(text)
    return m.group(1) if m else None


def files_to_check(args: argparse.Namespace) -> list[Path]:
    if args.file:
        paths: list[Path] = []
        for f in args.file:
            p = Path(f)
            paths.extend(sorted(p.rglob("*.md")) if p.is_dir() else [p])
        return paths
    dirs = args.dirs or args.paths
    if dirs:
        paths = []
        for d in dirs:
            p = Path(d)
            if p.is_dir():
                paths.extend(
                    f for f in sorted(p.rglob("*.md")) if f.name != "_index.md"
                )
            else:
                paths.append(p)
        return paths
    return tracked_md_files(["content"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail if any published article is missing readTime in front matter."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files to scan (legacy positional form).",
    )
    parser.add_argument(
        "--dir",
        dest="dirs",
        action="append",
        default=[],
        help="Directory to scan for articles. May be passed more than once.",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Markdown file to scan. May be passed more than once.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = files_to_check(args)

    missing: list[Path] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = parse_front_matter(text)
        if fm is None:
            continue
        if DRAFT_RE.search(fm):
            continue
        if not READ_TIME_RE.search(fm):
            missing.append(path)

    for path in missing:
        print(
            f"{ANSI_RED}ERROR: {path} is missing readTime in front matter{ANSI_RESET}",
            file=sys.stderr,
        )

    if missing:
        print(
            f"{ANSI_RED}✗ {len(missing)} published article(s) missing readTime{ANSI_RESET}",
            file=sys.stderr,
        )
        return 1

    print(f"{ANSI_GREEN}✓ all published articles have readTime{ANSI_RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
