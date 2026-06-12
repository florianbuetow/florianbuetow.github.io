#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Summarise categories and tags across blog and ticker articles as aligned ASCII tables.

Scans every published (non-draft) ``index.md`` page bundle under ``content/blog`` and
``content/ticker``, tallies the inline YAML ``categories`` and ``tags`` arrays, and renders
the counts as box-drawn tables. All tables share one global column width so the divider
lines align across the whole report.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"

BLUE = "\033[0;34m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Matches an inline YAML array field, e.g.  categories: ["A", "B"]
_ARRAY_FIELD = re.compile(r"^(?P<field>categories|tags):\s*\[(?P<body>.*)\]\s*$")
_DRAFT_TRUE = re.compile(r"^draft:\s*true\b")
_ITEM = re.compile(r"""\s*["']?(?P<value>[^,"']+?)["']?\s*$""")


def split_front_matter(text: str) -> list[str]:
    """Return the lines between the first two ``---`` fences (empty if none)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    for end, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:end]
    return []


def parse_array(body: str) -> list[str]:
    """Parse the inside of an inline YAML array into a list of values."""
    values = []
    for part in body.split(","):
        match = _ITEM.match(part)
        if match and match.group("value").strip():
            values.append(match.group("value").strip())
    return values


def iter_pages(content_subdir: Path):
    """Yield every Hugo-rendered page under a section.

    A page is either a leaf-bundle ``index.md`` or a flat ``*.md`` single page. A
    non-``index.md`` file living *inside* a bundle (e.g. an ``index.backup-*.md``) is a
    page resource, not a page, so it is skipped — as is the ``_index.md`` section list.
    """
    for path in sorted(content_subdir.rglob("*.md")):
        if path.name == "_index.md":
            continue
        if path.name == "index.md" or not (path.parent / "index.md").exists():
            yield path


def tally(content_subdir: Path) -> tuple[int, Counter, Counter]:
    """Count published articles plus their category and tag occurrences."""
    published = 0
    categories: Counter = Counter()
    tags: Counter = Counter()

    for path in iter_pages(content_subdir):
        front_matter = split_front_matter(path.read_text(encoding="utf-8"))
        if any(_DRAFT_TRUE.match(line) for line in front_matter):
            continue
        published += 1
        for line in front_matter:
            field = _ARRAY_FIELD.match(line)
            if not field:
                continue
            target = categories if field.group("field") == "categories" else tags
            target.update(parse_array(field.group("body")))

    return published, categories, tags


def ranked(counter: Counter) -> list[tuple[str, int]]:
    """Sort by count descending, then name descending (matches the legacy shell ordering)."""
    return sorted(counter.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)


def render_banner(title: str, width: int) -> list[str]:
    inner = width - 2
    return [
        f"  {BLUE}╭{'─' * inner}╮{RESET}",
        f"  {BLUE}│{RESET}{BOLD}{title.center(inner)}{RESET}{BLUE}│{RESET}",
        f"  {BLUE}╰{'─' * inner}╯{RESET}",
    ]


def render_table(header: str, rows: list[tuple[str, int]], name_w: int, count_w: int) -> list[str]:
    name_rule = "─" * (name_w + 2)
    count_rule = "─" * (count_w + 2)
    lines = [
        f"  ┌{name_rule}┬{count_rule}┐",
        f"  │ {BOLD}{header:<{name_w}}{RESET} │ {BOLD}{'Count':>{count_w}}{RESET} │",
        f"  ├{name_rule}┼{count_rule}┤",
    ]
    if rows:
        for name, count in rows:
            lines.append(f"  │ {name:<{name_w}} │ {count:>{count_w}} │")
    else:
        empty = "(none)"
        lines.append(f"  │ {DIM}{empty:<{name_w}}{RESET} │ {' ':>{count_w}} │")
    lines.append(f"  └{name_rule}┴{count_rule}┘")
    return lines


def main() -> int:
    sections = [
        ("BLOG ARTICLES", *tally(CONTENT_DIR / "blog")),
        ("TICKER NEWS", *tally(CONTENT_DIR / "ticker")),
    ]

    # One global name width and count width so every table's borders line up.
    counters: list[Counter] = []
    for section in sections:
        counters.extend(section[2:])
    all_names = ["Category", "Tag", "Count", "(none)"]
    max_count = 1
    for counter in counters:
        all_names.extend(counter)
        if counter:
            max_count = max(max_count, max(counter.values()))
    name_w = max(len(name) for name in all_names)
    count_w = max(len("Count"), len(str(max_count)))
    total_w = name_w + count_w + 7  # 2 borders of padding per column + 3 verticals

    out: list[str] = []
    for index, (title, published, categories, tags) in enumerate(sections):
        if index:
            out.append("")
        plural = "article" if published == 1 else "articles"
        out.extend(render_banner(title, total_w))
        out.append(f"  {DIM}{published} published {plural}{RESET}")
        out.append("")
        out.append(f"  {BOLD}Categories{RESET}")
        out.extend(render_table("Category", ranked(categories), name_w, count_w))
        out.append("")
        out.append(f"  {BOLD}Tags{RESET}")
        out.extend(render_table("Tag", ranked(tags), name_w, count_w))

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
