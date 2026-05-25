#!/usr/bin/env python3
"""Check unique external links in Markdown files with curl."""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urldefrag, urlparse


ANSI_RED = "\033[0;31m"
ANSI_GREEN = "\033[0;32m"
ANSI_BLUE = "\033[0;34m"
ANSI_RESET = "\033[0m"

USER_AGENT = (
    "Mozilla/5.0 (compatible; hugo-blog-link-checker/1.0; "
    "+https://cracking-ai-engineering.com/)"
)
DEFAULT_SKIP_DOMAINS_FILE = Path("config/link-check/skip-domains.txt")

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]*)\)")
HTML_URL_RE = re.compile(r"""(?i)\b(?:href|src)=["']([^"']+)["']""")
AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
BARE_URL_RE = re.compile(r"""https?://[^\s<>"'\]\)\}]+""")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


@dataclass(frozen=True)
class LinkCheckResult:
    url: str
    ok: bool
    status: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check unique external links in Markdown files with curl."
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
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Maximum seconds per curl request. Defaults to 20.",
    )
    parser.add_argument(
        "--connect-timeout",
        type=int,
        default=8,
        help="Maximum seconds to establish a connection. Defaults to 8.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel curl checks. Defaults to 8.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Only print the unique URLs that would be checked.",
    )
    parser.add_argument(
        "--skip-domains-file",
        default=str(DEFAULT_SKIP_DOMAINS_FILE),
        help="File containing domains to skip. Defaults to config/link-check/skip-domains.txt.",
    )
    return parser.parse_args()


def markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return sorted(set(files))


def strip_trailing_markdown_punctuation(raw_url: str) -> str:
    url = raw_url.strip()
    while url and url[-1] in ".,;:!?":
        url = url[:-1]
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    while url.endswith("]") and url.count("[") < url.count("]"):
        url = url[:-1]
    return url


def markdown_destination(raw_destination: str) -> str:
    destination = raw_destination.strip()
    if destination.startswith("<") and ">" in destination:
        return destination[1 : destination.index(">")]
    return destination.split(maxsplit=1)[0] if destination else ""


def normalize_url(raw_url: str) -> str | None:
    url = strip_trailing_markdown_punctuation(html.unescape(raw_url))

    # Only absolute HTTP(S) links are external links for this checker. Everything
    # else is internal or non-checkable here: /blog/, content/..., ./image.webp,
    # #anchors, mailto:, and similar Markdown targets.
    if not url.startswith(("http://", "https://")):
        return None

    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        return None

    return urldefrag(url).url


def extract_urls_from_line(line: str) -> set[str]:
    candidates: list[str] = []

    candidates.extend(
        markdown_destination(match.group(1)) for match in MARKDOWN_LINK_RE.finditer(line)
    )
    candidates.extend(match.group(1) for match in HTML_URL_RE.finditer(line))
    candidates.extend(match.group(1) for match in AUTOLINK_RE.finditer(line))

    line_without_inline_code = INLINE_CODE_RE.sub(" ", line)
    candidates.extend(match.group(0) for match in BARE_URL_RE.finditer(line_without_inline_code))

    urls: set[str] = set()
    for candidate in candidates:
        normalized = normalize_url(candidate)
        if normalized:
            urls.add(normalized)
    return urls


def collect_links(files: list[Path]) -> dict[str, list[str]]:
    sources: dict[str, list[str]] = defaultdict(list)

    for path in files:
        in_fence = False
        fence_marker = ""
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError as exc:
            print(
                f"{ANSI_RED}✗ check-links failed: could not read {path}: {exc}{ANSI_RESET}",
                file=sys.stderr,
            )
            sys.exit(1)

        for line_number, line in enumerate(lines, start=1):
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

            for url in extract_urls_from_line(line):
                sources[url].append(f"{path}:{line_number}")

    return dict(sorted(sources.items()))


def load_skip_domains(path: Path) -> set[str]:
    if not path.exists():
        return set()

    domains: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        domain = line.split("#", 1)[0].strip().lower()
        if domain:
            domains.add(domain)
    return domains


def url_hostname(url: str) -> str:
    parsed = urlparse(url)
    return (parsed.hostname or "").lower().rstrip(".")


def should_skip_url(url: str, skip_domains: set[str]) -> bool:
    hostname = url_hostname(url)
    return any(hostname == domain or hostname.endswith(f".{domain}") for domain in skip_domains)


def curl_status(
    url: str,
    *,
    timeout: int,
    connect_timeout: int,
    method: str,
) -> tuple[int, str]:
    args = [
        "curl",
        "--location",
        "--silent",
        "--show-error",
        "--output",
        os.devnull,
        "--write-out",
        "%{http_code}",
        "--max-time",
        str(timeout),
        "--connect-timeout",
        str(connect_timeout),
        "--user-agent",
        USER_AGENT,
    ]
    if method == "HEAD":
        args.append("--head")
    elif method == "RANGE_GET":
        args.extend(["--range", "0-0"])
    else:
        raise ValueError(f"unknown curl method: {method}")

    completed = subprocess.run(
        [*args, url],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    status_text = completed.stdout.strip() or "000"
    try:
        status = int(status_text[-3:])
    except ValueError:
        status = 0
    detail = completed.stderr.strip()
    return status, detail


def check_url(url: str, timeout: int, connect_timeout: int) -> LinkCheckResult:
    status, detail = curl_status(
        url,
        timeout=timeout,
        connect_timeout=connect_timeout,
        method="HEAD",
    )
    method = "HEAD"

    if status in {403, 405, 406, 501}:
        status, detail = curl_status(
            url,
            timeout=timeout,
            connect_timeout=connect_timeout,
            method="RANGE_GET",
        )
        method = "ranged GET"

    if 200 <= status < 400:
        return LinkCheckResult(url=url, ok=True, status=str(status), detail=method)

    if status == 0:
        message = detail or "curl did not return an HTTP status"
    else:
        message = f"HTTP {status} via {method}"
    return LinkCheckResult(url=url, ok=False, status=str(status), detail=message)


def check_links(
    urls: list[str],
    *,
    timeout: int,
    connect_timeout: int,
    workers: int,
) -> list[LinkCheckResult]:
    max_workers = max(1, workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(check_url, url, timeout, connect_timeout): url for url in urls
        }
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return sorted(results, key=lambda result: result.url)


def print_failures_by_file(
    failures: list[LinkCheckResult],
    sources_by_url: dict[str, list[str]],
) -> None:
    grouped: dict[str, list[tuple[int, str, str]]] = defaultdict(list)

    for failure in failures:
        for source in sources_by_url[failure.url]:
            path, raw_line = source.rsplit(":", 1)
            try:
                line_number = int(raw_line)
            except ValueError:
                line_number = 0
            grouped[path].append((line_number, failure.url, failure.detail))

    print(f"{ANSI_RED}Broken links by markdown file:{ANSI_RESET}")
    for path in sorted(grouped):
        print(f"{ANSI_RED}  {path}{ANSI_RESET}")
        for line_number, url, detail in sorted(grouped[path]):
            location = f"line {line_number}" if line_number else "line unknown"
            print(f"    {location}: {url} ({detail})")


def print_skipped_domains(
    skipped_links: dict[str, list[str]],
    skip_domains: set[str],
) -> None:
    if not skipped_links:
        return

    print(
        f"{ANSI_BLUE}→ skipped {len(skipped_links)} URL(s) from configured "
        f"domain skiplist: {', '.join(sorted(skip_domains))}{ANSI_RESET}"
    )
    for url in sorted(skipped_links):
        print(f"  {url}")


def main() -> int:
    args = parse_args()

    if shutil.which("curl") is None:
        print(f"{ANSI_RED}✗ check-links failed: curl is not installed{ANSI_RESET}")
        return 1

    paths = args.file or args.paths or ["content"]
    files = markdown_files(paths)
    if not files:
        print(f"{ANSI_GREEN}  no markdown files found{ANSI_RESET}")
        return 0

    links = collect_links(files)
    skip_domains = load_skip_domains(Path(args.skip_domains_file))
    skipped_links = {
        url: sources for url, sources in links.items() if should_skip_url(url, skip_domains)
    }
    checkable_links = {
        url: sources for url, sources in links.items() if url not in skipped_links
    }
    urls = list(checkable_links)

    if args.list:
        for url in urls:
            print(url)
        return 0

    print(
        f"{ANSI_BLUE}→ checking {len(urls)} unique external URL(s) "
        f"from {len(files)} markdown file(s){ANSI_RESET}"
    )
    print_skipped_domains(skipped_links, skip_domains)

    if not urls:
        print(f"{ANSI_GREEN}  no external links found{ANSI_RESET}")
        return 0

    results = check_links(
        urls,
        timeout=args.timeout,
        connect_timeout=args.connect_timeout,
        workers=args.workers,
    )
    failures = [result for result in results if not result.ok]

    if failures:
        for failure in failures:
            print(f"{ANSI_RED}  ✗ {failure.url} ({failure.detail}){ANSI_RESET}")
            for source in checkable_links[failure.url]:
                print(f"    {source}")
        print(
            f"{ANSI_RED}✗ check-links failed: {len(failures)} broken link(s) "
            f"out of {len(urls)} unique URL(s){ANSI_RESET}"
        )
        print("")
        print_failures_by_file(failures, checkable_links)
        return 1

    print(f"{ANSI_GREEN}  all {len(urls)} external link target(s) reachable{ANSI_RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
