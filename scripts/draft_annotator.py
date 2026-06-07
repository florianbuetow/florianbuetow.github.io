#!/usr/bin/env python3
"""Local draft annotation helper for Hugo content.

Runs a localhost-only HTTP endpoint for draft note insertion and a CI-safe
validator for draft annotation state.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_ROOT = REPO_ROOT / "content"
DEFAULT_PORT = 8787
MAX_QUOTE_LEN = 600
MAX_NOTE_LEN = 4000


@dataclass(frozen=True)
class MarkdownFile:
    path: Path
    draft: bool
    front_matter: str
    body: str
    body_offset: int


@dataclass(frozen=True)
class BlockMatch:
    start: int
    end: int
    text: str
    source: str


class AnnotatorError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def parse_markdown(path: Path) -> MarkdownFile:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            close_end = text.find("\n", end + 4)
            if close_end == -1:
                close_end = len(text) - 1
            front_matter = text[: close_end + 1]
            body = text[close_end + 1 :]
            return MarkdownFile(
                path=path,
                draft=is_draft_front_matter(front_matter),
                front_matter=front_matter,
                body=body,
                body_offset=close_end + 1,
            )
    return MarkdownFile(path=path, draft=False, front_matter="", body=text, body_offset=0)


def is_draft_front_matter(front_matter: str) -> bool:
    for line in front_matter.splitlines():
        if re.match(r"^\s*draft\s*:\s*true\s*$", line, re.IGNORECASE):
            return True
    return False


def iter_markdown_files(content_root: Path) -> list[MarkdownFile]:
    return [
        parse_markdown(path)
        for path in sorted(content_root.rglob("*.md"))
        if path.is_file()
    ]


def find_draft_articles(content_root: Path) -> list[MarkdownFile]:
    return [doc for doc in iter_markdown_files(content_root) if doc.draft]


def safe_content_path(file_path: str, content_root: Path | None = None) -> Path:
    content_root = content_root or CONTENT_ROOT
    if not file_path or Path(file_path).is_absolute():
        raise AnnotatorError("Invalid content path.")
    target = (content_root / file_path).resolve()
    root = content_root.resolve()
    if target != root and root not in target.parents:
        raise AnnotatorError("Content path escapes content root.")
    if target.suffix != ".md":
        raise AnnotatorError("Annotations can only be written to Markdown files.")
    if not target.exists():
        raise AnnotatorError("Content file not found.", 404)
    return target


def sanitize_field(name: str, value: Any, max_len: int) -> str:
    if not isinstance(value, str):
        raise AnnotatorError(f"{name} must be text.")
    value = value.strip()
    if not value:
        raise AnnotatorError(f"{name} is required.")
    if len(value) > max_len:
        raise AnnotatorError(f"{name} is too long.")
    if "<!--" in value or "-->" in value:
        raise AnnotatorError(f"{name} cannot contain HTML comment delimiters.")
    return value


def plain_markdown_text(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"\{\{<[^>]*>\}\}", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[\^[-\w]+\]", " ", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[.)]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_~]{1,3}([^*_~]+)[*_~]{1,3}", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def normalize_anchor(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\xa0": " ",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = plain_markdown_text(text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def block_source(text: str) -> str:
    if "{{< sidenote" in text or "{{% sidenote" in text:
        return "sidenote"
    if "{{< sidequote" in text or "{{% sidequote" in text:
        return "sidequote"
    return "body"


def markdown_blocks(body: str, body_offset: int) -> list[BlockMatch]:
    blocks: list[BlockMatch] = []
    in_fence = False
    block_start: int | None = None
    pos = 0
    lines = body.splitlines(keepends=True)

    for line in lines:
        line_start = pos
        pos += len(line)
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            if block_start is not None:
                block_start = None
            continue
        if in_fence or stripped.startswith("<!-- DRAFTNOTE"):
            continue
        if stripped:
            if block_start is None:
                block_start = line_start
        elif block_start is not None:
            block_text = body[block_start:line_start].strip()
            blocks.append(
                BlockMatch(
                    body_offset + block_start,
                    body_offset + line_start,
                    block_text,
                    block_source(block_text),
                )
            )
            block_start = None

    if block_start is not None:
        block_text = body[block_start:pos].strip()
        blocks.append(BlockMatch(body_offset + block_start, body_offset + pos, block_text, block_source(block_text)))
    return blocks


def find_quote_block(doc: MarkdownFile, quote: str, source: str = "body") -> BlockMatch:
    normalized_quote = normalize_anchor(quote)
    if len(normalized_quote) < 8:
        raise AnnotatorError("Quote is too short to locate safely.")
    if source not in {"body", "sidenote", "sidequote"}:
        raise AnnotatorError("Invalid annotation source.")

    blocks = markdown_blocks(doc.body, doc.body_offset)
    if source != "body":
        blocks = [block for block in blocks if block.source == source]
    matches = [
        block
        for block in blocks
        if normalized_quote in normalize_anchor(block.text)
    ]
    if not matches:
        raise AnnotatorError("Quote was not found in the Markdown source.")
    if len(matches) > 1:
        raise AnnotatorError("Quote matches multiple places. Use a longer quote.")
    return matches[0]


def yaml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_note(quote: str, note: str, created: str | None = None) -> str:
    created = created or dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    return (
        "\n<!-- DRAFTNOTE\n"
        f"quote: {yaml_string(quote)}\n"
        f"note: {yaml_string(note)}\n"
        f"created: {yaml_string(created)}\n"
        "-->\n"
    )


def annotate_file(
    file_path: str,
    quote: str,
    note: str,
    created: str | None = None,
    source: str = "body",
) -> dict[str, Any]:
    target = safe_content_path(file_path, CONTENT_ROOT)
    clean_quote = sanitize_field("quote", quote, MAX_QUOTE_LEN)
    clean_note = sanitize_field("note", note, MAX_NOTE_LEN)
    doc = parse_markdown(target)
    if not doc.draft:
        raise AnnotatorError("Annotations are only allowed in draft articles.", 403)

    match = find_quote_block(doc, clean_quote, source)
    text = target.read_text(encoding="utf-8")
    insertion = build_note(clean_quote, clean_note, created)
    target.write_text(text[: match.end].rstrip() + insertion + text[match.end :], encoding="utf-8")
    return {"ok": True, "filePath": file_path, "source": match.source, "insertedAfter": match.text[:120]}


def validate_annotations(content_root: Path) -> int:
    docs = iter_markdown_files(content_root)
    drafts = [doc for doc in docs if doc.draft]
    published_with_notes = [
        doc.path
        for doc in docs
        if not doc.draft and "<!-- DRAFTNOTE" in doc.body
    ]

    print(f"draft-annotator: scanned {len(docs)} Markdown file(s)")
    print(f"draft-annotator: found {len(drafts)} draft Markdown file(s)")
    for doc in drafts:
        print(f"  draft: {display_path(doc.path)}")

    if published_with_notes:
        print("draft-annotator: DRAFTNOTE blocks found in published articles", file=sys.stderr)
        for path in published_with_notes:
            print(f"  {display_path(path)}", file=sys.stderr)
        return 1
    print("draft-annotator: no DRAFTNOTE blocks in published articles")
    return 0


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


class DraftAnnotationHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", self._allowed_origin())
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _allowed_origin(self) -> str:
        origin = self.headers.get("Origin", "")
        if origin.startswith("http://127.0.0.1:") or origin.startswith("http://localhost:"):
            return origin
        return "http://127.0.0.1:1313"

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", self._allowed_origin())
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/draft-annotation/health":
            self._send_json(200, {"ok": True})
            return
        self._send_json(404, {"ok": False, "error": "Not found."})

    def do_POST(self) -> None:
        if self.path == "/draft-annotation/shutdown":
            self._send_json(200, {"ok": True, "message": "Shutting down draft annotator."})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        if self.path != "/draft-annotation":
            self._send_json(404, {"ok": False, "error": "Not found."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > 16384:
                raise AnnotatorError("Request is too large.")
            payload = json.loads(self.rfile.read(size).decode("utf-8"))
            result = annotate_file(
                str(payload.get("filePath", "")),
                payload.get("quote", ""),
                payload.get("note", ""),
                source=str(payload.get("source", "body")),
            )
            self._send_json(200, result)
        except AnnotatorError as error:
            self._send_json(error.status, {"ok": False, "error": str(error)})
        except Exception as error:  # pragma: no cover - defensive server boundary.
            self._send_json(500, {"ok": False, "error": str(error)})

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"draft-annotator: {fmt % args}", file=sys.stderr)


def serve(host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), DraftAnnotationHandler)
    print(f"draft-annotator: listening on http://{host}:{port}/draft-annotation")
    try:
        server.serve_forever()
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local Hugo draft annotation helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    serve_parser = sub.add_parser("serve", help="run the local annotation endpoint")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=DEFAULT_PORT)

    validate_parser = sub.add_parser("validate", help="validate draft annotation state")
    validate_parser.add_argument("content_dir", nargs="?", default=str(CONTENT_ROOT))

    annotate_parser = sub.add_parser("annotate", help="insert one annotation")
    annotate_parser.add_argument("--file-path", required=True)
    annotate_parser.add_argument("--quote", required=True)
    annotate_parser.add_argument("--note", required=True)
    annotate_parser.add_argument("--source", choices=["body", "sidenote", "sidequote"], default="body")

    args = parser.parse_args(argv)
    if args.cmd == "serve":
        serve(args.host, args.port)
        return 0
    if args.cmd == "validate":
        return validate_annotations(Path(args.content_dir))
    if args.cmd == "annotate":
        print(json.dumps(annotate_file(args.file_path, args.quote, args.note, source=args.source), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
