#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "spacy==3.8.7",
#   "click<9",
#   "pyyaml",
#   "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""Flag draft passages whose grammar matches AI-voice anti-patterns.

WHAT: tag each draft's prose with parts of speech (keeping punctuation), then
report any draft sentence that shares a contiguous run of >= K match-tokens with
one of the flagged fingerprint expressions. Advisory, stdout only.
Spec: docs/specs/ai-fingerprint-detect-specification.md.

    uv run scripts/fingerprint-detector.py                 # all drafts
    uv run scripts/fingerprint-detector.py path/to/file.md # one file

Cleaning + tagging is done by ProseTagger (scripts/prose_tagging.py). Drafts are
tagged in memory; this does NOT read reports/pos-tagged/ (those discard words).
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import yaml

# K: a draft sentence is flagged when it shares a contiguous run of at least this
# many match-tokens with a fingerprint. Doubles as the minimum fingerprint length
# (shorter fingerprints can never reach a run of K). Calibrated ~6; tune here.
K = 6

SRC = Path("docs/specs/pos-tag-ai-fingerprints.txt")
FP_OUT = Path("reports/ai-fingerprints.yaml")

# Load the shared tagger (sibling module).
_spec = importlib.util.spec_from_file_location(
    "prose_tagging", Path(__file__).with_name("prose_tagging.py")
)
ptag = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ptag)


def longest_common_run(a: list[str], b: list[str]) -> tuple[int, int]:
    """Longest contiguous common run between a and b. Returns (length, start_in_a)."""
    best, a_start = 0, 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, a_start = cur[j], i - cur[j]
        prev = cur
    return best, a_start


def _span_words(toks) -> str:
    """The original words of a token span, taken from the source text so that
    whitespace dropped between filtered tokens (e.g. a hard line break) cannot
    jam words together. Newlines/space runs are normalised to single spaces."""
    text = toks[0].doc.text[toks[0].idx: toks[-1].idx + len(toks[-1].text)]
    return " ".join(text.split())


def find_passages(md_text: str, fingerprints, tagger) -> list[dict]:
    """One entry per flagged span: {text, similar, pattern}. Every fingerprint
    whose matching run overlaps the same span is listed in `similar` (longest
    run defines the span and pattern), so passages matching several flagged
    examples of the same grammar are reported together, not collapsed to one."""
    passages: list[dict] = []
    for mtoks, toks in tagger.prose_sentences(md_text):
        cands = []
        for fp in fingerprints:
            length, start = longest_common_run(mtoks, fp["pattern"])
            if length >= K:
                cands.append((length, start, fp))
        cands.sort(key=lambda c: -c[0])  # longest defines the span; others attach to it
        groups: list[tuple[int, int, dict]] = []
        for length, start, fp in cands:
            end = start + length
            hit = next((g for g in groups if not (end <= g[0] or start >= g[1])), None)
            if hit is None:
                groups.append((start, end, {
                    "text": _span_words(toks[start:end]),
                    "similar": [fp["text"]],
                    "pattern": " ".join(mtoks[start:end]),
                }))
            elif fp["text"] not in hit[2]["similar"]:
                hit[2]["similar"].append(fp["text"])
        passages.extend(b for _s, _e, b in sorted(groups, key=lambda g: g[0]))
    return passages


def build_fingerprints(tagger) -> list[dict]:
    """Tag the anti-patterns source into reports/ai-fingerprints.yaml (AC-1.2)."""
    examples = []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text:
            examples.append({"text": text, "pattern": " ".join(tagger.pattern(text))})
    FP_OUT.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# AI-voice fingerprints: POS + punctuation patterns built from\n"
        f"# {SRC} by scripts/fingerprint-detector.py (regenerated each run).\n"
        "# pattern = match-token sequence (POS tags for words; punctuation kept).\n"
    )
    body = yaml.safe_dump(
        {"fingerprints": examples}, sort_keys=False, allow_unicode=True, width=10_000
    )
    FP_OUT.write_text(header + body, encoding="utf-8")
    return examples


def load_fingerprints() -> list[dict]:
    """Read reports/ai-fingerprints.yaml back into {text, pattern-list} (AC-1.3)."""
    data = yaml.safe_load(FP_OUT.read_text(encoding="utf-8"))["fingerprints"]
    return [{"text": e["text"], "pattern": e["pattern"].split()} for e in data]


def check_draft(path: Path, fingerprints, tagger) -> int:
    print(f"Checking draft document: {path}")
    md = path.read_text(encoding="utf-8", errors="replace")
    passages = find_passages(md, fingerprints, tagger)
    for b in passages:
        print(f"DETECTED IN TEXT: {b['text']}")
        for similar in b["similar"]:
            print(f"SIMILAR AI-VOICE: {similar}")
        print(f"PATTERN         : {b['pattern']}")
        print()
    n = len(passages)
    print("No suspicious text found" if n == 0
          else f"Found {n} passages that potentially sound AI generated")
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Detect AI-voice fingerprints in drafts.")
    ap.add_argument("path", nargs="?", help="a single .md file (default: all drafts)")
    args = ap.parse_args(argv)

    if args.path:
        p = Path(args.path)
        if not p.is_file() or p.suffix != ".md":
            print(f"✗ not a Markdown file: {args.path}", file=sys.stderr)
            return 2
        targets = [p]
    else:
        targets = ptag.find_drafts()
        if not targets:
            print("✓ no draft articles found")
            return 0

    if not SRC.is_file():
        print(f"✗ anti-patterns source not found: {SRC}", file=sys.stderr)
        return 2

    tagger = ptag.ProseTagger()
    build_fingerprints(tagger)          # AC-1.2: tag source -> reports/ai-fingerprints.yaml
    fingerprints = load_fingerprints()  # AC-1.3: detector reads patterns from that file
    for i, p in enumerate(targets):
        if i:
            print()
        check_draft(p, fingerprints, tagger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
