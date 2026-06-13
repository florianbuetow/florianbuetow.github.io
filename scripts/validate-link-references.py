#!/usr/bin/env python3
"""Validate that every link used in a Markdown file is listed in its
references section.

Some articles close with a "links section": a heading titled Links,
References, Resources, or Sources, followed by the catalogue of sources the
article cites. This checker enforces three rules on any file that has such a
heading:

  1. Exactly one links section per file.
  2. Nothing comes after it (no heading may follow the links section).
  3. Every link that appears in the body above the section is also listed
     inside the section.

A "link" is an inline Markdown link ``[text](url)`` or an HTML ``href``.
Images, bare URLs (so Markdown footnote definitions are ignored), footnote
markers, same-page anchors (``#...``, links to the current page), and the
author's LinkedIn post link are intentionally not counted. External and
same-site links (``/blog/...``) are counted.
Links inside shortcodes (sidenote/citenote) are counted, because they are
plain text in the source. Fenced code blocks and front matter are skipped.

Run with:

    uv run scripts/validate-link-references.py            # scans content/
    uv run scripts/validate-link-references.py --file path/to/index.md
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
import re
from urllib.parse import urlparse


ANSI_RED = "\033[0;31m"
ANSI_GREEN = "\033[0;32m"
ANSI_YELLOW = "\033[0;33m"
ANSI_RESET = "\033[0m"

# Headings (case-insensitive, exact title) that open a links section.
REFERENCE_TITLES = frozenset({"links", "references", "resources", "sources"})

ATX_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# Inline Markdown link, excluding images: the negative lookbehind drops the
# leading "!" of "![alt](src)" so images are never treated as links.
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]*)\)")
# HTML anchors written as raw HTML (href only; src points at images/media).
HTML_HREF_RE = re.compile(r"""(?i)\bhref\s*=\s*["']([^"']+)["']""")

FRONT_MATTER_DELIMITERS = ("---", "+++")

# Our own site (mirrors hugo.toml baseURL). An internal link may be written
# relative ("/blog/x/") in the body and absolute
# ("https://cracking-ai-engineering.com/blog/x/") in the references section;
# both name the same destination, so they must compare equal.
SITE_HOST = "cracking-ai-engineering.com"


@dataclass(frozen=True)
class Heading:
    index: int  # 0-based position in the line list (used for splitting)
    line_no: int  # 1-based line number (used for reporting)
    level: int
    title: str


@dataclass(frozen=True)
class Violation:
    kind: str  # "multiple-sections" | "heading-after-section" | "missing-link"
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that every link in a Markdown file is listed in its "
            "Links/References/Resources/Sources section."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to scan. Defaults to content/.",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Markdown file to scan. May be passed more than once.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Link extraction
# ---------------------------------------------------------------------------

def is_excluded_linkedin(url: str) -> bool:
    """The author's LinkedIn post link sits above the references heading in
    essays and inside the section in tickers. It is structural, never a cited
    source, so it is excluded everywhere. Profile links (/in/...) are kept."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    host = (parsed.hostname or "").lower()
    if not (host == "linkedin.com" or host.endswith(".linkedin.com")):
        return False
    path = parsed.path or ""
    return path.startswith("/posts/") or path.startswith("/feed/update/")


def markdown_destination(raw_destination: str) -> str:
    """Extract the URL from a Markdown link destination, dropping an optional
    title and surrounding angle brackets: `url "title"` -> `url`."""
    destination = raw_destination.strip()
    if not destination:
        return ""
    if destination.startswith("<"):
        end = destination.find(">")
        if end != -1:
            return destination[1:end].strip()
    return destination.split()[0]


def canonical_link(url: str) -> str:
    """Reduce an internal link to its path so a relative body link matches its
    absolute own-domain form in the references section. External links are
    returned unchanged."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return url
    host = (parsed.hostname or "").lower()
    if host == SITE_HOST or host == f"www.{SITE_HOST}":
        path = parsed.path or "/"
        if parsed.query:
            path = f"{path}?{parsed.query}"
        if parsed.fragment:
            path = f"{path}#{parsed.fragment}"
        return path
    return url


def _code_aware_lines(lines: list[str], start: int = 0):
    """Yield (index, line) for lines outside fenced code blocks."""
    in_fence = False
    fence_marker = ""
    for i in range(start, len(lines)):
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if in_fence and marker == fence_marker:
                in_fence = False
                fence_marker = ""
            elif not in_fence:
                in_fence = True
                fence_marker = marker
            continue
        if in_fence:
            continue
        yield i, line


def extract_links(text: str) -> list[str]:
    """Return the URLs in ``text``, deduplicated and in first-appearance order.

    Counts inline Markdown links ``[text](url)`` and HTML ``href`` values.
    Skips images, bare URLs, fenced code blocks, and the LinkedIn post link.
    """
    urls: list[str] = []
    seen: set[str] = set()

    def add(candidate: str) -> None:
        url = candidate.strip()
        # Skip same-page anchors (links to the current page) and the LinkedIn
        # post link; keep external and same-site links.
        if not url or url.startswith("#") or is_excluded_linkedin(url):
            return
        if url not in seen:
            seen.add(url)
            urls.append(url)

    for _, line in _code_aware_lines(text.split("\n")):
        for match in MARKDOWN_LINK_RE.finditer(line):
            add(markdown_destination(match.group(1)))
        for match in HTML_HREF_RE.finditer(line):
            add(match.group(1))

    return urls


# ---------------------------------------------------------------------------
# Structure analysis
# ---------------------------------------------------------------------------

def _front_matter_end(lines: list[str]) -> int:
    """Return the index of the first line after the front-matter block, or 0
    when the file has none."""
    if not lines:
        return 0
    delimiter = lines[0].strip()
    if delimiter not in FRONT_MATTER_DELIMITERS:
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == delimiter:
            return i + 1
    return 0


def is_draft(text: str) -> bool:
    """True only when front matter explicitly sets draft to true. Hugo treats a
    missing draft key as published, so absence (and no front matter) is not a
    draft."""
    lines = text.split("\n")
    if not lines:
        return False
    delimiter = lines[0].strip()
    if delimiter not in FRONT_MATTER_DELIMITERS:
        return False
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == delimiter:
            break
        if re.match(r"(?i)^draft\s*[:=]\s*true\b", stripped):
            return True
    return False


def _find_headings(lines: list[str], start: int) -> list[Heading]:
    headings: list[Heading] = []
    for i, line in _code_aware_lines(lines, start):
        match = ATX_HEADING_RE.match(line)
        if match:
            title = match.group(2).strip().rstrip("#").strip()
            headings.append(
                Heading(index=i, line_no=i + 1, level=len(match.group(1)), title=title)
            )
    return headings


def analyze_text(text: str) -> list[Violation]:
    """Return the violations for one Markdown document. Files without a links
    section return no violations (they are not subject to the check)."""
    lines = text.split("\n")
    content_start = _front_matter_end(lines)
    headings = _find_headings(lines, content_start)

    reference_headings = [h for h in headings if h.title.lower() in REFERENCE_TITLES]
    if not reference_headings:
        return []

    # Rule 1: exactly one links section. Stop here if violated.
    if len(reference_headings) > 1:
        listed = ", ".join(
            f'"{"#" * h.level} {h.title}" (line {h.line_no})' for h in reference_headings
        )
        return [
            Violation(
                "multiple-sections",
                f"multiple links sections (only one allowed): {listed}",
            )
        ]

    section = reference_headings[0]

    # Rule 2: nothing after the links section. Stop here if violated.
    trailing = [h for h in headings if h.index > section.index]
    if trailing:
        return [
            Violation(
                "heading-after-section",
                f'heading "{"#" * h.level} {h.title}" (line {h.line_no}) '
                f'appears after the "{section.title}" section (line {section.line_no})',
            )
            for h in trailing
        ]

    # Rule 3: every body link is listed in the section. Links are compared by
    # canonical form so an internal link written relative in the body matches
    # its absolute own-domain entry in the section (and vice versa).
    body_links = extract_links("\n".join(lines[content_start : section.index]))
    section_links = {
        canonical_link(url) for url in extract_links("\n".join(lines[section.index :]))
    }
    return [
        Violation(
            "missing-link",
            f'link missing from "{section.title}" section: {url}',
        )
        for url in body_links
        if canonical_link(url) not in section_links
    ]


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def _git_tracked_markdown(directory: Path) -> list[Path]:
    """List git-tracked .md files under a directory. CI must never block on a
    file that is not part of the commit, so untracked files are skipped here
    (matching the validate-md target)."""
    spec = f"{str(directory).rstrip('/')}/*.md"
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", spec],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "git ls-files failed"
        print(
            f"{ANSI_RED}✗ validate-link-references failed: {message}{ANSI_RESET}",
            file=sys.stderr,
        )
        sys.exit(1)
    return [Path(entry) for entry in result.stdout.split("\0") if entry]


def markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(_git_tracked_markdown(path))
    return sorted(set(files))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        print(
            f"{ANSI_RED}✗ validate-link-references failed: could not read "
            f"{path}: {exc}{ANSI_RESET}",
            file=sys.stderr,
        )
        sys.exit(1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    args = parse_args()

    paths = args.file or args.paths or ["content"]
    files = markdown_files(paths)
    if not files:
        print(f"{ANSI_GREEN}  no markdown files found{ANSI_RESET}")
        return 0

    # Violations in published articles are errors (they fail CI); violations in
    # drafts are warnings (shown, but never affect the exit code).
    errors: list[tuple[Path, list[Violation]]] = []
    warnings: list[tuple[Path, list[Violation]]] = []
    for path in files:
        text = read_text(path)
        violations = analyze_text(text)
        if not violations:
            continue
        (warnings if is_draft(text) else errors).append((path, violations))

    def emit(groups: list[tuple[Path, list[Violation]]], color: str, header: str) -> None:
        print(f"{color}{header}{ANSI_RESET}")
        for path, violations in groups:
            print(f"{color}  {path}{ANSI_RESET}")
            for violation in violations:
                print(f"    {violation.message}")

    if errors:
        emit(errors, ANSI_RED, "Link reference errors (published articles):")
    if warnings:
        emit(warnings, ANSI_YELLOW, "Link reference warnings (drafts, non-blocking):")

    error_count = sum(len(v) for _, v in errors)
    warning_count = sum(len(v) for _, v in warnings)
    warning_tail = (
        f"; {warning_count} warning(s) in {len(warnings)} draft(s)" if warning_count else ""
    )

    if error_count:
        print(
            f"{ANSI_RED}✗ validate-link-references failed: {error_count} error(s) "
            f"in {len(errors)} published file(s){warning_tail}{ANSI_RESET}"
        )
        return 1

    if warning_count:
        print(
            f"{ANSI_YELLOW}✓ validate-link-references passed: 0 errors"
            f"{warning_tail}{ANSI_RESET}"
        )
        return 0

    print(f"{ANSI_GREEN}  all {len(files)} markdown file(s) passed{ANSI_RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
