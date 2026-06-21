#!/usr/bin/env python3
"""Compute and set the readTime front matter field as ceil(word_count / 225)."""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
from pathlib import Path

ANSI_RED = "\033[0;31m"
ANSI_GREEN = "\033[0;32m"
ANSI_BLUE = "\033[0;34m"
ANSI_RESET = "\033[0m"

WORDS_PER_MINUTE = 225

FRONT_MATTER_RE = re.compile(r"^(---\n)(.*?)(\n---)", re.DOTALL)
READ_TIME_LINE_RE = re.compile(r"^readTime:.*$", re.MULTILINE)

_FENCED_CODE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
_TILDE_CODE_RE = re.compile(r"^~~~.*?^~~~", re.MULTILINE | re.DOTALL)
_SHORTCODE_RE = re.compile(r"\{\{[<%].*?[>%]\}\}", re.DOTALL)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_FRONT_MATTER_STRIP_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


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
        if p and p.startswith("content/")
    ]


def strip_markdown(text: str) -> str:
    text = _FRONT_MATTER_STRIP_RE.sub("", text, count=1)
    text = _FENCED_CODE_RE.sub("", text)
    text = _TILDE_CODE_RE.sub("", text)
    text = _SHORTCODE_RE.sub("", text)
    text = _HTML_TAG_RE.sub("", text)
    text = _IMAGE_RE.sub("", text)
    text = _LINK_RE.sub(r"\1", text)
    return text


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", strip_markdown(text)))


def process_file(path: Path) -> bool:
    """Update readTime in front matter. Returns True if file was modified."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"{ANSI_RED}ERROR: cannot read {path}: {e}{ANSI_RESET}", file=sys.stderr)
        return False

    m = FRONT_MATTER_RE.match(text)
    if not m:
        return False

    words = count_words(text)
    minutes = math.ceil(words / WORDS_PER_MINUTE)
    new_value = f'readTime: "{minutes} min read"'

    fm_body = m.group(2)
    if READ_TIME_LINE_RE.search(fm_body):
        new_fm_body = READ_TIME_LINE_RE.sub(new_value, fm_body)
    else:
        new_fm_body = fm_body + "\n" + new_value

    if new_fm_body == fm_body:
        return False

    new_text = m.group(1) + new_fm_body + m.group(3) + text[m.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"{ANSI_BLUE}  updated: {path} ({words} words → {minutes} min read){ANSI_RESET}")
    return True


def files_to_process(args: argparse.Namespace) -> list[Path]:
    if args.file:
        paths: list[Path] = []
        for f in args.file:
            p = Path(f)
            paths.extend(sorted(p.rglob("*.md")) if p.is_dir() else [p])
        return paths
    if args.paths:
        paths = []
        for f in args.paths:
            p = Path(f)
            paths.extend(sorted(p.rglob("*.md")) if p.is_dir() else [p])
        return paths
    return tracked_md_files()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute and set readTime front matter from word count (ceil(words/225))."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to process. Defaults to git-tracked content/.",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Markdown file to process. May be passed more than once.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = files_to_process(args)

    updated = 0
    for path in files:
        if process_file(path):
            updated += 1

    if updated:
        print(f"{ANSI_GREEN}✓ updated readTime in {updated} file(s){ANSI_RESET}")
    else:
        print(f"{ANSI_GREEN}✓ all readTime values up to date{ANSI_RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
