#!/usr/bin/env python3
"""List Git-tracked Markdown files, optionally restricted to drafts."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

DRAFT_RE = re.compile(r"^draft: true", re.MULTILINE)


class GitTrackedFiles:
    """Select Markdown files exclusively from Git's tracked-file set."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def filter(self, paths: list[Path]) -> list[Path]:
        tracked = set(self._git_ls_files())
        return [path for path in paths if path in tracked]

    def markdown_under(self, pathspec: str, *, drafts_only: bool) -> list[Path]:
        tracked = self._git_ls_files(pathspec)
        markdown = [path for path in tracked if path.suffix == ".md"]
        if not drafts_only:
            return markdown
        return [path for path in markdown if self._is_draft(path)]

    def _git_ls_files(self, pathspec: Optional[str] = None) -> list[Path]:
        command = ["git", "ls-files", "-z"]
        if pathspec is not None:
            command.extend(["--", pathspec])
        result = subprocess.run(
            command,
            cwd=self.root,
            capture_output=True,
            check=True,
        )
        return [
            Path(raw.decode("utf-8"))
            for raw in result.stdout.split(b"\0")
            if raw
        ]

    def _is_draft(self, relative_path: Path) -> bool:
        try:
            text = (self.root / relative_path).read_text(encoding="utf-8")
        except OSError:
            return False
        return bool(DRAFT_RE.search(text))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filter-stdin", action="store_true")
    parser.add_argument("--drafts-only", action="store_true")
    parser.add_argument("path", nargs="?", default="content/")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    tracked = GitTrackedFiles(Path.cwd())
    if args.filter_stdin:
        candidates = [Path(line) for line in sys.stdin.read().splitlines() if line]
        for path in tracked.filter(candidates):
            print(path)
        return 0
    for path in tracked.markdown_under(args.path, drafts_only=args.drafts_only):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
