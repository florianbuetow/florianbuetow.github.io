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

Output goes to reports/pos-tagged/<slug>.md -- never into content/, never the
source file. Default target = every draft (front matter `draft: true`) under
content/; pass a single .md path to tag just that file.

    uv run scripts/pos-tagger.py                 # all drafts
    uv run scripts/pos-tagger.py path/to/file.md # one file
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MODEL = "en_core_web_sm"
OUT_DIR = Path("reports/pos-tagged")
CONTENT_DIR = Path("content")

# A line that opens or closes a fenced code block (``` or ~~~, 3+).
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")

# Verbatim line prefix: indentation, stacked blockquote markers, and at most one
# list or heading marker. Kept as-is; only the prose after it is tagged.
LEADING_RE = re.compile(r"^(\s*(?:>\s?)*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+)?)")

# Inline spans that must NOT be fed to spaCy as prose. Order matters: code,
# shortcodes and footnote refs are matched before links so their brackets are
# not mistaken for link syntax. `image`/`link` keep their URL verbatim but their
# alt/text is recursed into as prose.
INLINE_RE = re.compile(
    r"""
      (?P<code>`[^`\n]*`)
    | (?P<shortcode>\{\{[<%].*?[%>]\}\})
    | (?P<footnote>\[\^[^\]\n]+\])
    | (?P<htmltag></?[A-Za-z][^>\n]*>)
    | (?P<autolink><https?://[^>\n]+>)
    | (?P<image>!\[(?P<alt>[^\]\n]*)\]\((?P<imgurl>[^)\n]*)\))
    | (?P<link>\[(?P<ltext>[^\]\n]*)\]\((?P<lurl>[^)\n]*)\))
    | (?P<strong>\*\*(?P<stext>[^*\n]+?)\*\*)
    | (?P<strongu>(?<!\w)__(?P<sutext>[^_\n]+?)__(?!\w))
    | (?P<em>\*(?P<etext>[^*\n]+?)\*)
    | (?P<emu>(?<!\w)_(?P<eutext>[^_\n]+?)_(?!\w))
    | (?P<url>https?://[^\s)<>{}"'`]+)
    """,
    re.VERBOSE,
)


def load_nlp():
    """Load the English spaCy model, or exit with install instructions."""
    try:
        import spacy
    except ModuleNotFoundError:  # pragma: no cover - uv run installs spacy
        sys.exit("spaCy is not installed. Run via: uv run scripts/pos-tagger.py")
    try:
        return spacy.load(MODEL)
    except OSError:
        sys.exit(
            f"spaCy English model {MODEL!r} is not installed.\n"
            f"Install it with: uv run --with spacy python -m spacy download {MODEL}"
        )


def tag_prose(text: str, nlp) -> str:
    """Replace each prose word in `text` with its POS tag.

    Punctuation, symbols and whitespace are kept verbatim (so Markdown markers
    like * [ ] survive); every other token becomes its coarse POS tag. Leading
    and trailing whitespace are preserved around the tagged core.
    """
    if not text.strip():
        return text
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    core = text.strip()

    out: list[str] = []
    for tok in nlp(core):
        if tok.pos_ in ("PUNCT", "SYM", "SPACE"):
            out.append(tok.text)
        else:
            out.append(tok.pos_)
        out.append(tok.whitespace_)  # ponytail: spaCy collapses runs of spaces to one
    return lead + "".join(out) + trail


def process_inline(text: str, nlp) -> str:
    """Tag prose in one line, leaving code/links/shortcodes/URLs verbatim."""
    out: list[str] = []
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append(tag_prose(text[pos:m.start()], nlp))
        if m.group("image") is not None:
            out.append(f"![{tag_prose(m.group('alt'), nlp)}]({m.group('imgurl')})")
        elif m.group("link") is not None:
            out.append(f"[{tag_prose(m.group('ltext'), nlp)}]({m.group('lurl')})")
        elif m.group("strong") is not None:
            out.append(f"**{tag_prose(m.group('stext'), nlp)}**")
        elif m.group("strongu") is not None:
            out.append(f"__{tag_prose(m.group('sutext'), nlp)}__")
        elif m.group("em") is not None:
            out.append(f"*{tag_prose(m.group('etext'), nlp)}*")
        elif m.group("emu") is not None:
            out.append(f"_{tag_prose(m.group('eutext'), nlp)}_")
        else:
            out.append(m.group(0))  # verbatim span
        pos = m.end()
    if pos < len(text):
        out.append(tag_prose(text[pos:], nlp))
    return "".join(out)


def split_front_matter(lines: list[str]) -> tuple[list[str], list[str]]:
    """Return (front_matter_lines, body_lines). Front matter is verbatim."""
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return lines[: i + 1], lines[i + 1:]
    return [], lines


def tag_markdown(text: str, nlp) -> str:
    """Tag an entire Markdown document, preserving all structure."""
    trailing_nl = text.endswith("\n")
    lines = text.splitlines()
    front, body = split_front_matter(lines)

    out = list(front)
    in_fence = False
    fence_char = ""
    for line in body:
        if in_fence:
            out.append(line)
            m = FENCE_RE.match(line)
            if m and m.group(2)[0] == fence_char:
                in_fence = False
            continue
        m = FENCE_RE.match(line)
        if m:
            out.append(line)
            in_fence = True
            fence_char = m.group(2)[0]
            continue
        prefix = LEADING_RE.match(line).group(0)
        out.append(prefix + process_inline(line[len(prefix):], nlp))

    result = "\n".join(out)
    return result + "\n" if trailing_nl else result


def slug_for(path: Path) -> str:
    """Page bundle (.../<slug>/index.md) -> <slug>; flat <name>.md -> <name>."""
    return path.parent.name if path.name == "index.md" else path.stem


def find_drafts() -> list[Path]:
    """Every Markdown file under content/ with front matter `draft: true`."""
    drafts = []
    for p in sorted(CONTENT_DIR.rglob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?m)^draft: true\s*$", text):
            drafts.append(p)
    return drafts


def tag_file(path: Path, nlp) -> Path:
    out_path = OUT_DIR / f"{slug_for(path)}.md"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8", errors="replace")
    out_path.write_text(tag_markdown(text, nlp), encoding="utf-8")
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

    nlp = load_nlp()
    for p in targets:
        print(f"✓ {p}  ->  {tag_file(p, nlp)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
