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

Reuses the prose tokenising of scripts/pos-tagger.py. Drafts are tagged in
memory; this does NOT read reports/pos-tagged/ (those discard the words).
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

# Load the tagger module (hyphenated path -> importlib).
_spec = importlib.util.spec_from_file_location(
    "pos_tagger", Path(__file__).with_name("pos-tagger.py")
)
pt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pt)


def prose_inline(text: str) -> str:
    """Strip one line to bare prose: drop code/shortcodes/URLs/markdown markers,
    keep link/image/emphasis inner text. Mirrors pos-tagger's span split."""
    out: list[str] = []
    pos = 0
    for m in pt.INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append(text[pos:m.start()])
        for inner in ("alt", "ltext", "stext", "sutext", "etext", "eutext"):
            if m.groupdict().get(inner) is not None and m.group(inner) is not None:
                out.append(f" {m.group(inner)} ")
                break
        else:
            out.append(" ")  # code / shortcode / footnote / html / url -> dropped
        pos = m.end()
    if pos < len(text):
        out.append(text[pos:])
    return "".join(out)


def extract_prose(md_text: str) -> str:
    """Return a draft's prose only, with markdown/Hugo structure removed and
    paragraph breaks (blank lines) preserved for sentence segmentation."""
    lines = md_text.splitlines()
    _front, body = pt.split_front_matter(lines)
    out: list[str] = []
    in_fence = False
    fence_char = ""
    for line in body:
        if in_fence:
            m = pt.FENCE_RE.match(line)
            if m and m.group(2)[0] == fence_char:
                in_fence = False
            continue
        m = pt.FENCE_RE.match(line)
        if m:
            in_fence = True
            fence_char = m.group(2)[0]
            continue
        prefix = pt.LEADING_RE.match(line).group(0)
        rest = line[len(prefix):]
        out.append(prose_inline(rest) if rest.strip() else "")
    return "\n".join(out)


def _match_token(tok) -> str:
    """POS tag for a word/number; the literal char for punctuation/symbols."""
    return tok.text if tok.pos_ in ("PUNCT", "SYM") else tok.pos_


def pattern_for(text: str, nlp) -> list[str]:
    """The flat match-token sequence of a fingerprint expression."""
    return [_match_token(t) for t in nlp(prose_inline(text)) if not t.is_space]


def sentence_tokens(prose: str, nlp):
    """Yield (match_tokens, spacy_tokens) per sentence; lists run parallel."""
    for sent in nlp(prose).sents:
        toks = [t for t in sent if not t.is_space]
        if toks:
            yield [_match_token(t) for t in toks], toks


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


def find_passages(prose: str, fingerprints, nlp) -> list[dict]:
    """One entry per flagged span: {text, similar, pattern}. Every fingerprint
    whose matching run overlaps the same span is listed in `similar` (longest
    run defines the span and pattern), so passages matching several flagged
    examples of the same grammar are reported together, not collapsed to one."""
    passages: list[dict] = []
    for mtoks, toks in sentence_tokens(prose, nlp):
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


def build_fingerprints(nlp) -> list[dict]:
    """Tag the anti-patterns source into reports/ai-fingerprints.yaml (AC-1.2)."""
    examples = []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text:
            examples.append({"text": text, "pattern": " ".join(pattern_for(text, nlp))})
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


def check_draft(path: Path, fingerprints, nlp) -> int:
    print(f"Checking draft document: {path}")
    passages = find_passages(
        extract_prose(path.read_text(encoding="utf-8", errors="replace")), fingerprints, nlp)
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
        targets = pt.find_drafts()
        if not targets:
            print("✓ no draft articles found")
            return 0

    if not SRC.is_file():
        print(f"✗ anti-patterns source not found: {SRC}", file=sys.stderr)
        return 2

    nlp = pt.load_nlp()
    build_fingerprints(nlp)            # AC-1.2: tag source -> reports/ai-fingerprints.yaml
    fingerprints = load_fingerprints()  # AC-1.3: detector reads patterns from that file
    for i, p in enumerate(targets):
        if i:
            print()
        check_draft(p, fingerprints, nlp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
