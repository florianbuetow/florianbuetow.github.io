#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "spacy==3.8.7",
#   "click<9",
#   "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""Shared Markdown-prose cleaning + POS tagging.

`ProseTagger` owns everything both the pos-tagger and the fingerprint detector
need: the Markdown/Hugo structure rules, prose extraction, and the spaCy
word->tag mapping. Each script is a thin CLI on top of it.

    ProseTagger(nlp).tagged_markdown(md)   # structure-preserving tag-only doc
    ProseTagger(nlp).prose_sentences(md)   # [(match_tokens, spacy_tokens)] per sentence
    ProseTagger(nlp).pattern(text)         # match-token list of a phrase
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MODEL = "en_core_web_sm"
CONTENT_DIR = Path("content")

# A line that opens or closes a fenced code block (``` or ~~~, 3+).
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")

# Verbatim line prefix: indentation, stacked blockquote markers, and at most one
# list or heading marker. Kept as-is; only the prose after it is tagged.
LEADING_RE = re.compile(r"^(\s*(?:>\s?)*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+)?)")

# Inline spans that must NOT be fed to spaCy as prose. Order matters: code,
# shortcodes and footnote refs are matched before links so their brackets are
# not mistaken for link syntax. image/link keep their URL verbatim but their
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

_INNER_GROUPS = ("alt", "ltext", "stext", "sutext", "etext", "eutext")


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


def split_front_matter(lines: list[str]) -> tuple[list[str], list[str]]:
    """Return (front_matter_lines, body_lines). Front matter is verbatim."""
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return lines[: i + 1], lines[i + 1:]
    return [], lines


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


class ProseTagger:
    """Cleans Markdown to prose and POS-tags it. Bound to one spaCy pipeline."""

    def __init__(self, nlp=None):
        self.nlp = nlp if nlp is not None else load_nlp()

    @staticmethod
    def match_token(tok) -> str:
        """POS tag for a word/number; the literal char for punctuation/symbols."""
        return tok.text if tok.pos_ in ("PUNCT", "SYM") else tok.pos_

    # --- structure-preserving rendering (pos-tagger) -------------------------

    def tag_prose(self, text: str) -> str:
        """Replace each prose word in `text` with its POS tag, keeping
        punctuation/symbols/whitespace verbatim and surrounding whitespace."""
        if not text.strip():
            return text
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        out: list[str] = []
        for tok in self.nlp(text.strip()):
            if tok.pos_ in ("PUNCT", "SYM", "SPACE"):
                out.append(tok.text)
            else:
                out.append(tok.pos_)
            out.append(tok.whitespace_)  # ponytail: spaCy collapses space runs to one
        return lead + "".join(out) + trail

    def process_inline(self, text: str) -> str:
        """Tag prose in one line, leaving code/links/shortcodes/URLs verbatim."""
        out: list[str] = []
        pos = 0
        for m in INLINE_RE.finditer(text):
            if m.start() > pos:
                out.append(self.tag_prose(text[pos:m.start()]))
            if m.group("image") is not None:
                out.append(f"![{self.tag_prose(m.group('alt'))}]({m.group('imgurl')})")
            elif m.group("link") is not None:
                out.append(f"[{self.tag_prose(m.group('ltext'))}]({m.group('lurl')})")
            elif m.group("strong") is not None:
                out.append(f"**{self.tag_prose(m.group('stext'))}**")
            elif m.group("strongu") is not None:
                out.append(f"__{self.tag_prose(m.group('sutext'))}__")
            elif m.group("em") is not None:
                out.append(f"*{self.tag_prose(m.group('etext'))}*")
            elif m.group("emu") is not None:
                out.append(f"_{self.tag_prose(m.group('eutext'))}_")
            else:
                out.append(m.group(0))  # verbatim span
            pos = m.end()
        if pos < len(text):
            out.append(self.tag_prose(text[pos:]))
        return "".join(out)

    def tagged_markdown(self, md_text: str) -> str:
        """Tag an entire Markdown document, preserving all structure."""
        trailing_nl = md_text.endswith("\n")
        lines = md_text.splitlines()
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
            out.append(prefix + self.process_inline(line[len(prefix):]))
        result = "\n".join(out)
        return result + "\n" if trailing_nl else result

    # --- bare-prose extraction (fingerprint detector) ------------------------

    @staticmethod
    def prose_inline(text: str) -> str:
        """Strip one line to bare prose: drop code/shortcodes/URLs/markdown
        markers, keep link/image/emphasis inner text."""
        out: list[str] = []
        pos = 0
        for m in INLINE_RE.finditer(text):
            if m.start() > pos:
                out.append(text[pos:m.start()])
            inner = next((m.group(g) for g in _INNER_GROUPS if m.group(g) is not None), None)
            out.append(f" {inner} " if inner is not None else " ")
            pos = m.end()
        if pos < len(text):
            out.append(text[pos:])
        return "".join(out)

    @classmethod
    def extract_prose(cls, md_text: str) -> str:
        """A document's prose only, structure removed, paragraph breaks kept."""
        lines = md_text.splitlines()
        _front, body = split_front_matter(lines)
        out: list[str] = []
        in_fence = False
        fence_char = ""
        for line in body:
            if in_fence:
                m = FENCE_RE.match(line)
                if m and m.group(2)[0] == fence_char:
                    in_fence = False
                continue
            m = FENCE_RE.match(line)
            if m:
                in_fence = True
                fence_char = m.group(2)[0]
                continue
            prefix = LEADING_RE.match(line).group(0)
            rest = line[len(prefix):]
            out.append(cls.prose_inline(rest) if rest.strip() else "")
        return "\n".join(out)

    def pattern(self, text: str) -> list[str]:
        """The flat match-token sequence of a phrase (POS + punctuation)."""
        return [self.match_token(t) for t in self.nlp(self.prose_inline(text)) if not t.is_space]

    def prose_sentences(self, md_text: str):
        """Yield (match_tokens, spacy_tokens) per sentence; lists run parallel."""
        for sent in self.nlp(self.extract_prose(md_text)).sents:
            toks = [t for t in sent if not t.is_space]
            if toks:
                yield [self.match_token(t) for t in toks], toks
