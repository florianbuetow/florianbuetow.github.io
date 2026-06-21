#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "spacy==3.8.7",
#   "click<9",
#   "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""Replace prose words in a Markdown article with their part-of-speech tags.

WHAT: turn natural-language prose into a stream of spaCy coarse POS tags
(NOUN VERB ADJ ...) while leaving all Markdown / Hugo structure intact, so the
author can scan an article's grammatical skeleton for repetitive sentence
patterns. Spec: docs/specs/pos-tag-articles-specification.md.

The cleaning + tagging itself lives in scripts/prose_tagging.py (ProseTagger);
this file is the CLI. Output goes to reports/pos-tagged/<slug>.md -- never into
content/, never the source file. Default target = every draft (front matter
`draft: true`) under content/; pass a single .md path to tag just that file.

    uv run scripts/pos-tagger.py                 # all drafts
    uv run scripts/pos-tagger.py path/to/file.md # one file
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

# Load the shared tagger (sibling module).
_spec = importlib.util.spec_from_file_location(
    "prose_tagging", Path(__file__).with_name("prose_tagging.py")
)
ptag = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ptag)

OUT_DIR = Path("reports/pos-tagged")

# Re-exported for callers/tests; the logic lives in ProseTagger.
load_nlp = ptag.load_nlp
slug_for = ptag.slug_for
find_drafts = ptag.find_drafts


def tag_markdown(text: str, nlp) -> str:
    return ptag.ProseTagger(nlp).tagged_markdown(text)


def tag_prose(text: str, nlp) -> str:
    return ptag.ProseTagger(nlp).tag_prose(text)


def tag_file(path: Path, tagger) -> Path:
    out_path = OUT_DIR / f"{slug_for(path)}.md"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8", errors="replace")
    out_path.write_text(tagger.tagged_markdown(text), encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="POS-tag a Markdown article's prose.")
    ap.add_argument("path", nargs="?", help="a single .md file (default: all drafts)")
    args = ap.parse_args(argv)

    if args.path:
        p = Path(args.path)
        if not p.is_file() or p.suffix != ".md":
            print(f"✗ not a Markdown file: {args.path}", file=sys.stderr)
            return 2
        targets = [p]
    else:
        targets = find_drafts()
        if not targets:
            print("✓ no draft articles found")
            return 0

    tagger = ptag.ProseTagger()
    for p in targets:
        print(f"✓ {p}  ->  {tag_file(p, tagger)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
