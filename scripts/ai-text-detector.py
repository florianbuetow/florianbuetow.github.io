#!/usr/bin/env python3
"""Detect AI-generated-text tells in Markdown articles.

A heuristic, deterministic linter for the article-review CI. It flags the
linguistic fingerprints of LLM-written prose -- not a forensic
"was-this-machine-written" verdict, but a "this reads like AI slop" gate.

Architecture (modular by design):

    Document      parsed once per file: front matter and code stripped,
                  inline code / link URLs masked, paragraphs + sentences +
                  headings extracted. Every check shares this view.
    Check         self-contained unit with id / category / severity and a
                  run(doc) -> findings method. Add a check = add one entry
                  to build_registry().
    suite         each "giveaway" (contrast framing, rule of three, ...) is
                  covered by a SUITE of checks grouped under one category.
    PhraseListCheck   reusable engine for every word/phrase rule; its data
                      lives in config/ai-tells/*.txt so lists can be tuned
                      without touching code.

Severity:
    ERROR   high-precision tells -> fail the build (exit 1)
    WARN    noisy / domain-sensitive tells -> reported only (exit 0)
    --strict promotes warnings to failures.

config/ai-tells/allowlist.txt suppresses known false positives, one phrase
per line (the config/harper/dictionary.txt escape-hatch pattern).

By default scans draft articles (front matter `draft: true`) under content/.
Pass file or directory paths, or --file, to scan specific files regardless
of draft status (use this to confirm a published, hand-written post stays
quiet).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Iterator


# --------------------------------------------------------------------------
# Presentation
# --------------------------------------------------------------------------

ANSI_RED = "\033[0;31m"
ANSI_YELLOW = "\033[0;33m"
ANSI_GREEN = "\033[0;32m"
ANSI_BLUE = "\033[0;34m"
ANSI_DIM = "\033[2m"
ANSI_RESET = "\033[0m"

DEFAULT_CONFIG_DIR = Path("config/ai-tells")
DEFAULT_CONTENT_DIR = Path("content")

# Straight or curly apostrophe, for phrase/regex matching.
AP = "['’]"


class Severity(Enum):
    ERROR = "error"
    WARN = "warn"

    @property
    def color(self) -> str:
        return ANSI_RED if self is Severity.ERROR else ANSI_YELLOW


ERROR = Severity.ERROR
WARN = Severity.WARN


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    col: int
    check_id: str
    category: str
    severity: Severity
    text: str
    message: str


# --------------------------------------------------------------------------
# Document model (parsed once, shared by every check)
# --------------------------------------------------------------------------

_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
_LINK_URL_RE = re.compile(r"(\]\()([^)]*)(\))")
_BARE_URL_RE = re.compile(r"https?://\S+")
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
_HEADING_RE = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_WORD_RE = re.compile(r"[^\W\d_][\w'’-]*")


def _mask(text: str) -> str:
    """Blank out code spans and URLs, preserving column positions."""

    def blank(match: re.Match) -> str:
        return " " * len(match.group(0))

    text = _INLINE_CODE_RE.sub(blank, text)
    text = _LINK_URL_RE.sub(
        lambda m: m.group(1) + " " * len(m.group(2)) + m.group(3), text
    )
    text = _BARE_URL_RE.sub(blank, text)
    return text


@dataclass(frozen=True)
class ScanLine:
    lineno: int
    raw: str
    masked: str  # code/URLs blanked; "" for front-matter and code lines


@dataclass(frozen=True)
class Heading:
    lineno: int
    level: int
    text: str


@dataclass(frozen=True)
class Paragraph:
    start_line: int
    text: str  # masked prose, joined with spaces


class Document:
    def __init__(self, path: Path, text: str) -> None:
        self.path = str(path)
        self.raw_lines = text.splitlines()
        self.scan_lines = self._build_scan_lines(self.raw_lines)
        self.headings = self._build_headings()
        self.paragraphs = self._build_paragraphs()

    @classmethod
    def from_path(cls, path: Path) -> "Document":
        return cls(path, path.read_text(encoding="utf-8", errors="replace"))

    @staticmethod
    def _build_scan_lines(raw_lines: list[str]) -> list[ScanLine]:
        scan: list[ScanLine] = []
        in_front = False
        in_fence = False
        fence_char = ""
        for i, raw in enumerate(raw_lines):
            lineno = i + 1
            stripped = raw.strip()
            if i == 0 and stripped == "---":
                in_front = True
                scan.append(ScanLine(lineno, raw, ""))
                continue
            if in_front:
                scan.append(ScanLine(lineno, raw, ""))
                if stripped == "---":
                    in_front = False
                continue
            fence = _FENCE_RE.match(raw)
            if in_fence:
                scan.append(ScanLine(lineno, raw, ""))
                if fence and fence.group(1)[0] == fence_char:
                    in_fence = False
                continue
            if fence:
                in_fence = True
                fence_char = fence.group(1)[0]
                scan.append(ScanLine(lineno, raw, ""))
                continue
            scan.append(ScanLine(lineno, raw, _mask(raw)))
        return scan

    def _build_headings(self) -> list[Heading]:
        headings: list[Heading] = []
        for sl in self.scan_lines:
            if not sl.masked.strip():
                continue
            m = _HEADING_RE.match(sl.raw)
            if m:
                headings.append(Heading(sl.lineno, len(m.group(1)), m.group(2)))
        return headings

    def _build_paragraphs(self) -> list[Paragraph]:
        paragraphs: list[Paragraph] = []
        buf: list[str] = []
        start: int | None = None
        for sl in self.scan_lines:
            is_heading = bool(_HEADING_RE.match(sl.raw)) and bool(sl.masked.strip())
            if not sl.masked.strip() or is_heading:
                if buf:
                    paragraphs.append(Paragraph(start or 1, " ".join(buf)))
                    buf, start = [], None
                continue
            if start is None:
                start = sl.lineno
            buf.append(sl.masked.strip())
        if buf:
            paragraphs.append(Paragraph(start or 1, " ".join(buf)))
        return paragraphs

    def prose_lines(self) -> Iterator[ScanLine]:
        for sl in self.scan_lines:
            if sl.masked.strip():
                yield sl


def split_sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_SPLIT_RE.split(text.strip()) if s]


def word_count(text: str) -> int:
    return len(_WORD_RE.findall(text))


# --------------------------------------------------------------------------
# Config loading
# --------------------------------------------------------------------------

def compile_phrase(phrase: str) -> re.Pattern:
    tokens = phrase.split()
    body = r"\s+".join(re.escape(t).replace("'", AP) for t in tokens)
    left = r"(?<!\w)" if phrase[:1].isalnum() else ""
    right = r"(?!\w)" if phrase[-1:].isalnum() else ""
    return re.compile(left + body + right, re.IGNORECASE)


def load_entries(path: Path) -> list[tuple[re.Pattern, str, str]]:
    """Parse a phrase-list file into (regex, phrase, suggestion) tuples."""
    entries: list[tuple[re.Pattern, str, str]] = []
    if not path.exists():
        return entries
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=>" in line:
            phrase, _, suggestion = line.partition("=>")
            phrase, suggestion = phrase.strip(), suggestion.strip()
        else:
            phrase, suggestion = line, ""
        if phrase:
            entries.append((compile_phrase(phrase), phrase, suggestion))
    return entries


def load_phrases(path: Path) -> list[str]:
    return [phrase for _, phrase, _ in load_entries(path)]


def load_allowlist(path: Path) -> set[str]:
    allow: set[str] = set()
    if not path.exists():
        return allow
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            allow.add(line.lower())
    return allow


# --------------------------------------------------------------------------
# Check framework
# --------------------------------------------------------------------------

class Check:
    """Base class. A check inspects a Document and yields Findings."""

    def __init__(
        self, check_id: str, category: str, severity: Severity, description: str
    ) -> None:
        self.id = check_id
        self.category = category
        self.severity = severity
        self.description = description

    def run(self, doc: Document) -> Iterable[Finding]:  # pragma: no cover
        raise NotImplementedError(f"{self.id}.run({doc.path!r}) is abstract")

    def finding(self, doc: Document, line: int, col: int, text: str, message: str) -> Finding:
        return Finding(
            path=doc.path,
            line=line,
            col=col,
            check_id=self.id,
            category=self.category,
            severity=self.severity,
            text=text.strip(),
            message=message,
        )


class PhraseListCheck(Check):
    """Flag every phrase from a config/ai-tells/*.txt list."""

    def __init__(
        self,
        check_id: str,
        category: str,
        severity: Severity,
        path: Path,
        message: str,
        description: str = "",
    ) -> None:
        super().__init__(check_id, category, severity, description or message)
        self.entries = load_entries(path)
        self.message = message

    def run(self, doc: Document) -> Iterator[Finding]:
        for sl in doc.prose_lines():
            for regex, _, suggestion in self.entries:
                for m in regex.finditer(sl.masked):
                    text = sl.raw[m.start():m.end()]
                    yield self.finding(
                        doc, sl.lineno, m.start() + 1, text, suggestion or self.message
                    )


class RegexCheck(Check):
    """Flag a single-line structural pattern."""

    def __init__(
        self,
        check_id: str,
        category: str,
        severity: Severity,
        pattern: str,
        message: str,
        group: int = 0,
        description: str = "",
    ) -> None:
        super().__init__(check_id, category, severity, description or message)
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.message = message
        self.group = group

    def run(self, doc: Document) -> Iterator[Finding]:
        g = self.group
        for sl in doc.prose_lines():
            for m in self.regex.finditer(sl.masked):
                text = sl.raw[m.start(g):m.end(g)]
                yield self.finding(doc, sl.lineno, m.start(g) + 1, text, self.message)


# --- Structural checks ----------------------------------------------------

_DESCRIPTOR_SUFFIX = (
    "ing", "ed", "ive", "ent", "ant", "ful", "ous", "al", "ic",
    "able", "ible", "less", "ly", "y",
)
_TRIAD_RE = re.compile(r"\b(\w{3,}), (\w{3,}),? and (\w{3,})\b")


class RuleOfThreeCheck(Check):
    """Descriptor triads: 'efficient, effective, and reliable'."""

    def __init__(self) -> None:
        super().__init__(
            "rule-of-three.descriptor-triad", "rule-of-three", WARN,
            "three parallel descriptors in a row",
        )

    def run(self, doc: Document) -> Iterator[Finding]:
        for sl in doc.prose_lines():
            for m in _TRIAD_RE.finditer(sl.masked):
                words = [m.group(1), m.group(2), m.group(3)]
                if all(w.lower().endswith(_DESCRIPTOR_SUFFIX) for w in words):
                    text = sl.raw[m.start():m.end()]
                    yield self.finding(
                        doc, sl.lineno, m.start() + 1, text,
                        "rule-of-three triad -- use sparingly",
                    )


# Pictographic emoji planes + Misc Symbols/Dingbats + regional flags. The
# arrow blocks (U+2190-21FF, U+2B00-2BFF) are deliberately excluded: "->" and
# friends are technical notation in this blog, not emoji explosions.
_EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF\U0000FE0F]"
)


class EmojiCheck(Check):
    def __init__(self) -> None:
        super().__init__("emoji.any", "emoji", WARN, "emoji in prose")

    def run(self, doc: Document) -> Iterator[Finding]:
        for sl in doc.prose_lines():
            for m in _EMOJI_RE.finditer(sl.raw):
                yield self.finding(
                    doc, sl.lineno, m.start() + 1, m.group(0),
                    "emoji -- use sparingly, if at all",
                )


_EMOJI_EXPLOSION_THRESHOLD = 3


class EmojiDensityCheck(Check):
    """Many emoji in one file -- the actual 'emoji explosion' tell."""

    def __init__(self) -> None:
        super().__init__("emoji.density", "emoji", WARN, "emoji explosion")

    def run(self, doc: Document) -> Iterator[Finding]:
        total = 0
        first: int | None = None
        for sl in doc.prose_lines():
            for _ in _EMOJI_RE.finditer(sl.raw):
                total += 1
                if first is None:
                    first = sl.lineno
        if total >= _EMOJI_EXPLOSION_THRESHOLD and first is not None:
            yield self.finding(
                doc, first, 1, f"{total} emoji",
                f"{total} emoji in this file -- emoji explosion",
            )


_TITLE_FUNCTION_WORDS = {
    "a", "an", "the", "and", "or", "but", "nor", "of", "to", "in", "on",
    "for", "with", "as", "at", "by", "from", "is", "are", "was", "were",
    "it", "its", "your", "you", "how", "why", "what", "when", "that",
    "this", "about", "into", "over", "than", "then", "so", "if", "vs",
}


class TitleCaseHeadingCheck(Check):
    """Headings should be sentence case, not Title Case."""

    def __init__(self) -> None:
        super().__init__(
            "headings.title-case", "headings", WARN, "Title Case heading",
        )

    def run(self, doc: Document) -> Iterator[Finding]:
        for h in doc.headings:
            words = _WORD_RE.findall(h.text)
            if len(words) < 2:
                continue
            rest = words[1:]
            cap_function = any(
                w[:1].isupper() and w.lower() in _TITLE_FUNCTION_WORDS for w in rest
            )
            cap_content = [
                w for w in rest if w[0].isupper() and not w.isupper() and len(w) >= 2
            ]
            if cap_function or len(cap_content) >= 2:
                yield self.finding(
                    doc, h.lineno, 1, h.text,
                    "heading looks Title Case -- prefer sentence case",
                )


# Gerund-led headings AI reaches for. Excludes plain "Building"/"Creating",
# which are common and legitimate.
_GERUND_HEADINGS = {
    "understanding", "exploring", "navigating", "unlocking", "leveraging",
    "mastering", "demystifying", "harnessing", "unleashing", "embracing",
    "rethinking", "revolutionizing", "elevating", "supercharging",
    "discovering", "uncovering",
}


class GerundHeadingCheck(Check):
    """'Understanding X', 'Navigating Y' -- a stock AI heading shape."""

    def __init__(self) -> None:
        super().__init__("headings.gerund-opener", "headings", WARN, "gerund-led heading")

    def run(self, doc: Document) -> Iterator[Finding]:
        for h in doc.headings:
            words = _WORD_RE.findall(h.text)
            if words and words[0].lower() in _GERUND_HEADINGS:
                yield self.finding(
                    doc, h.lineno, 1, h.text,
                    "gerund-led heading -- a common AI tell",
                )


_SUMMARY_HEADINGS = {
    "conclusion", "summary", "in summary", "in conclusion", "final thoughts",
    "wrapping up", "wrap up", "tldr", "tl;dr", "takeaways", "key takeaways",
    "closing thoughts", "the takeaway", "final word", "final words",
    "parting thoughts",
}


class SummaryHeadingCheck(Check):
    def __init__(self) -> None:
        super().__init__(
            "summary-endings.heading", "summary-endings", WARN,
            "formulaic wrap-up heading",
        )

    def run(self, doc: Document) -> Iterator[Finding]:
        for h in doc.headings:
            norm = h.text.strip().lower().rstrip(":")
            if norm in _SUMMARY_HEADINGS:
                yield self.finding(
                    doc, h.lineno, 1, h.text,
                    "formulaic wrap-up heading -- end on a concrete point",
                )


_TRANSITION_INITIAL = {
    "however", "moreover", "furthermore", "additionally", "therefore",
    "thus", "hence", "consequently", "meanwhile", "nevertheless",
    "nonetheless", "similarly", "ultimately", "indeed", "notably",
    "importantly", "accordingly", "subsequently",
}
_TRANSITION_DENSITY_THRESHOLD = 4


class TransitionDensityCheck(Check):
    """Too many sentences opening with a formal connector."""

    def __init__(self) -> None:
        super().__init__(
            "transition-overuse.density", "transition-overuse", WARN,
            "many sentence-initial transitions",
        )

    def run(self, doc: Document) -> Iterator[Finding]:
        count = 0
        first_line: int | None = None
        for p in doc.paragraphs:
            for sentence in split_sentences(p.text):
                words = _WORD_RE.findall(sentence)
                if words and words[0].lower() in _TRANSITION_INITIAL:
                    count += 1
                    if first_line is None:
                        first_line = p.start_line
        if count >= _TRANSITION_DENSITY_THRESHOLD and first_line is not None:
            yield self.finding(
                doc, first_line, 1, f"{count} sentence-initial transitions",
                f"{count} sentences open with a formal transition -- vary them",
            )


_UNIFORMITY_MIN_SENTENCES = 4
_UNIFORMITY_CV_THRESHOLD = 0.30
_UNIFORMITY_MIN_MEAN_WORDS = 6.0


class SentenceUniformityCheck(Check):
    """Low burstiness: human writing varies sentence length; LLMs don't."""

    def __init__(self) -> None:
        super().__init__(
            "natural-flow.sentence-uniformity", "natural-flow", WARN,
            "uniform sentence lengths (low burstiness)",
        )

    def run(self, doc: Document) -> Iterator[Finding]:
        for p in doc.paragraphs:
            lengths = [n for n in (word_count(s) for s in split_sentences(p.text)) if n]
            if len(lengths) < _UNIFORMITY_MIN_SENTENCES:
                continue
            mean = sum(lengths) / len(lengths)
            if mean < _UNIFORMITY_MIN_MEAN_WORDS:
                continue
            variance = sum((n - mean) ** 2 for n in lengths) / len(lengths)
            cv = (variance ** 0.5) / mean
            if cv < _UNIFORMITY_CV_THRESHOLD:
                yield self.finding(
                    doc, p.start_line, 1,
                    f"{len(lengths)} sentences, CV={cv:.2f}",
                    f"sentence lengths very uniform (CV={cv:.2f}) -- vary your rhythm",
                )


_PARA_UNIFORMITY_MIN_PARAS = 4
_PARA_UNIFORMITY_MIN_WORDS = 25
_PARA_UNIFORMITY_CV_THRESHOLD = 0.22


class ParagraphUniformityCheck(Check):
    """Same-sized paragraph blocks -- the LLM 'wall of even bricks' rhythm."""

    def __init__(self) -> None:
        super().__init__(
            "natural-flow.paragraph-uniformity", "natural-flow", WARN,
            "uniform paragraph lengths",
        )

    def run(self, doc: Document) -> Iterator[Finding]:
        sized = [(p.start_line, word_count(p.text)) for p in doc.paragraphs]
        sized = [(ln, n) for ln, n in sized if n >= _PARA_UNIFORMITY_MIN_WORDS]
        if len(sized) < _PARA_UNIFORMITY_MIN_PARAS:
            return
        lengths = [n for _, n in sized]
        mean = sum(lengths) / len(lengths)
        variance = sum((n - mean) ** 2 for n in lengths) / len(lengths)
        cv = (variance ** 0.5) / mean
        if cv < _PARA_UNIFORMITY_CV_THRESHOLD:
            yield self.finding(
                doc, sized[0][0], 1, f"{len(lengths)} paragraphs, CV={cv:.2f}",
                f"{len(lengths)} paragraphs of near-equal length (CV={cv:.2f}) "
                "-- vary paragraph size",
            )


# --------------------------------------------------------------------------
# Registry -- one suite of checks per "giveaway"
# --------------------------------------------------------------------------

def build_registry(cfg: Path) -> list[Check]:
    """Build the full check suite. Each "giveaway" maps to >= 2 checks."""
    checks: list[Check] = []

    # 1. LLM clichés (suite: lexical + phrase) ------------------------------
    checks += [
        PhraseListCheck(
            "cliches.lexical", "cliches", ERROR, cfg / "cliches-lexical.txt",
            "LLM lexical cliché -- rewrite it in your own words",
        ),
        PhraseListCheck(
            "cliches.phrase", "cliches", ERROR, cfg / "cliches-phrase.txt",
            "LLM cliché phrase -- rewrite it in your own words",
        ),
    ]

    # 2. Contrast-framing overload (suite of 5) -----------------------------
    checks += [
        RegexCheck(
            "contrast.not-x-its-y", "contrast-framing", ERROR,
            rf"\bit{AP}?s not (?:just|only|merely|simply|about)\b[^.?!\n]*?\bit{AP}?s\b",
            "contrast cliche -- be direct, use a concrete detail",
        ),
        # not-just / not-only ... but: a legitimate human construction too,
        # so WARN, not ERROR. The build-failing tell is the antithesis form
        # ("X isn't Y, it's Z") handled by the ERROR checks above/below.
        RegexCheck(
            "contrast.not-just-but", "contrast-framing", WARN,
            r"\bnot (?:just|merely|simply)\b[^.?!\n]*?\bbut\b",
            "not-just/but contrast -- consider being more direct",
        ),
        RegexCheck(
            "contrast.not-only-but", "contrast-framing", WARN,
            r"\bnot only\b[^.?!\n]*?\bbut\b",
            "not-only/but-also construction -- consider saying it straight",
        ),
        RegexCheck(
            "contrast.isnt-its", "contrast-framing", ERROR,
            rf"\b\w+ (?:isn{AP}?t|aren{AP}?t|is not|are not)\b[^.?!\n]*?,\s*"
            rf"(?:it{AP}?s|they{AP}?re|it is|they are)\b",
            "X-isn't-Y-it's-Z contrast -- be direct",
        ),
        RegexCheck(
            "contrast.less-more-about", "contrast-framing", ERROR,
            r"\bless about\b[^.?!\n]*?\bmore about\b",
            "less-about/more-about contrast -- be direct",
        ),
    ]

    # 3. Rule of three (suite: descriptor triad + tricolon) -----------------
    checks += [
        RuleOfThreeCheck(),
        RegexCheck(
            "rule-of-three.tricolon", "rule-of-three", WARN,
            r"\b\w+ \w+, \w+ \w+,? and \w+ \w+\b",
            "tricolon (three parallel clauses) -- AI over-uses these",
        ),
    ]

    # 4. Cringe transition questions (suite: list + short-fragment) ---------
    checks += [
        PhraseListCheck(
            "cringe-questions.list", "cringe-questions", ERROR,
            cfg / "cringe-questions.txt",
            "infomercial fragment -- cut it",
        ),
        RegexCheck(
            "cringe-questions.short-fragment", "cringe-questions", ERROR,
            r"(?:^|[.!?]\s+)((?:The|And the|But the|My|Your|Our)\s+\w+\?)",
            "rhetorical fragment -- cut the infomercial setup",
            group=1,
        ),
    ]

    # 5. Corporate -ing verbs (suite: list + after-comma) -------------------
    ing_words = load_phrases(cfg / "ing-verbs.txt")
    checks.append(
        PhraseListCheck(
            "ing-verbs.list", "ing-verbs", WARN, cfg / "ing-verbs.txt",
            "corporate -ing verb -- use a simple active verb",
        )
    )
    if ing_words:
        alternation = "|".join(re.escape(w) for w in ing_words)
        checks.append(
            RegexCheck(
                "ing-verbs.after-comma", "ing-verbs", WARN,
                rf",\s+({alternation})\b",
                "comma + corporate -ing verb -- strong AI tell",
                group=1,
            )
        )

    # 6. Vague glazing opinions (suite: openers + qualifiers) ---------------
    checks += [
        PhraseListCheck(
            "glazing.openers", "glazing", ERROR, cfg / "glazing-openers.txt",
            "throat-clearing opener -- just state your point",
        ),
        PhraseListCheck(
            "glazing.qualifiers", "glazing", ERROR, cfg / "glazing-qualifiers.txt",
            "soft-claim qualifier -- commit to the point",
        ),
    ]

    # 7. Formality-first language (suite: verbs + quantifiers) --------------
    checks += [
        PhraseListCheck(
            "formal-words.verbs", "formal-words", WARN, cfg / "formal-verbs.txt",
            "four-dollar verb -- write like you talk",
        ),
        PhraseListCheck(
            "formal-words.quantifiers", "formal-words", WARN,
            cfg / "formal-quantifiers.txt",
            "four-dollar quantifier -- write like you talk",
        ),
    ]

    # 8. Emoji explosion (suite: any + density) -----------------------------
    checks += [EmojiCheck(), EmojiDensityCheck()]

    # (9. Extra em dashes -- already banned outright by config/semgrep/no-em-dash.yml)

    # 10. Everything is "symbolic" (suite: verbs + phrases) -----------------
    checks += [
        PhraseListCheck(
            "symbolic.verbs", "symbolic", WARN, cfg / "symbolic-verbs.txt",
            "stating what it 'represents' -- say what happened",
        ),
        PhraseListCheck(
            "symbolic.phrases", "symbolic", WARN, cfg / "symbolic-phrases.txt",
            "gesturing at meaning -- say what happened",
        ),
    ]

    # 11. Fabricated example person (suite: stock-names + intro pattern) -----
    checks += [
        PhraseListCheck(
            "fabricated-names.list", "fabricated-names", ERROR,
            cfg / "fabricated-names.txt",
            "looks like a fabricated example -- use a real one",
        ),
        RegexCheck(
            "fabricated-names.intro", "fabricated-names", WARN,
            r"\b(?:a|an|our|the|this)\s+(?:developer|engineer|manager|user|"
            r"customer|founder|designer|colleague|friend|client|student|"
            r"researcher|teammate|coworker)\s+(?:named|called)\s+\w+",
            "introducing a hypothetical person -- use a real example",
        ),
    ]

    # 12. Formulaic summary endings (suite: phrases + heading) --------------
    checks += [
        PhraseListCheck(
            "summary-endings.list", "summary-endings", ERROR,
            cfg / "summary-endings.txt",
            "formulaic summary opener -- end on a concrete point",
        ),
        SummaryHeadingCheck(),
    ]

    # 13. "Despite challenges" filler (suite: concession + rosy future) -----
    checks += [
        PhraseListCheck(
            "despite-challenges.list", "despite-challenges", ERROR,
            cfg / "despite-challenges.txt",
            "formulaic 'despite challenges' concession -- be specific",
        ),
        PhraseListCheck(
            "despite-challenges.rosy-future", "despite-challenges", ERROR,
            cfg / "rosy-future.txt",
            "canned optimistic closer -- land on a concrete takeaway",
        ),
    ]

    # 14. Puffery (suite: adjectives + compounds) ---------------------------
    checks += [
        PhraseListCheck(
            "puffery.adjectives", "puffery", WARN, cfg / "puffery-adjectives.txt",
            "puffery -- back it with a concrete detail",
        ),
        PhraseListCheck(
            "puffery.compounds", "puffery", WARN, cfg / "puffery-compounds.txt",
            "brochure hype -- show the thing instead",
        ),
    ]

    # 15. Vague attributions (suite: research + consensus) ------------------
    checks += [
        PhraseListCheck(
            "vague-attributions.research", "vague-attributions", ERROR,
            cfg / "vague-research.txt",
            "unsourced research claim -- cite it or cut it",
        ),
        PhraseListCheck(
            "vague-attributions.consensus", "vague-attributions", ERROR,
            cfg / "vague-consensus.txt",
            "vague appeal to consensus -- name them or cut it",
        ),
    ]

    # 16. Hedging and disclaimers (suite: adverbs + phrases) ----------------
    checks += [
        PhraseListCheck(
            "hedging.adverbs", "hedging", WARN, cfg / "hedging-adverbs.txt",
            "hedge -- make the claim",
        ),
        PhraseListCheck(
            "hedging.phrases", "hedging", WARN, cfg / "hedging-phrases.txt",
            "hedge -- make the claim",
        ),
    ]

    # 17. Transition overuse (suite: list + density) ------------------------
    checks += [
        PhraseListCheck(
            "transition-overuse.list", "transition-overuse", WARN,
            cfg / "transition-words.txt",
            "formal transition -- vary or cut",
        ),
        TransitionDensityCheck(),
    ]

    # 18. Natural flow (suite: sentence + paragraph uniformity) -------------
    checks += [SentenceUniformityCheck(), ParagraphUniformityCheck()]

    # 19. Headings (suite: title-case + gerund-opener) ----------------------
    checks += [TitleCaseHeadingCheck(), GerundHeadingCheck()]

    return checks


# --------------------------------------------------------------------------
# File discovery
# --------------------------------------------------------------------------

_DRAFT_RE = re.compile(r"^draft:\s*true\s*$", re.MULTILINE)


def is_draft(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:4096]
    except OSError:
        return False
    return bool(_DRAFT_RE.search(head))


def find_drafts(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return [p for p in sorted(root.rglob("*.md")) if is_draft(p)]


def collect_files(paths: list[str], files: list[str]) -> list[Path]:
    explicit = files + paths
    if not explicit:
        return find_drafts(DEFAULT_CONTENT_DIR)
    collected: list[Path] = []
    seen: set[Path] = set()
    for raw in explicit:
        p = Path(raw)
        candidates: Iterable[Path]
        if p.is_dir():
            candidates = sorted(p.rglob("*.md"))
        elif p.is_file():
            candidates = [p]
        else:
            print(f"{ANSI_YELLOW}  ! not found: {p}{ANSI_RESET}", file=sys.stderr)
            continue
        for c in candidates:
            if c not in seen:
                seen.add(c)
                collected.append(c)
    return collected


# --------------------------------------------------------------------------
# Runner + reporting
# --------------------------------------------------------------------------

def scan_document(
    doc: Document, checks: list[Check], allowlist: set[str]
) -> list[Finding]:
    findings: list[Finding] = []
    for check in checks:
        for f in check.run(doc):
            if f.text.lower() in allowlist:
                continue
            findings.append(f)
    return findings


def report(findings_by_path: dict[str, list[Finding]]) -> tuple[int, int]:
    errors = warnings = 0
    for path in sorted(findings_by_path):
        fs = sorted(
            findings_by_path[path], key=lambda f: (f.line, f.col, f.severity.value)
        )
        for f in fs:
            sev = f.severity.value.upper()
            tag = f"{f.severity.color}[{sev} {f.check_id}]{ANSI_RESET}"
            msg = f"  {ANSI_DIM}-> {f.message}{ANSI_RESET}" if f.message else ""
            print(f'  {path}:{f.line}:{f.col}  {tag}  "{f.text}"{msg}')
            if f.severity is Severity.ERROR:
                errors += 1
            else:
                warnings += 1
    return errors, warnings


def print_registry(checks: list[Check]) -> None:
    by_category: dict[str, list[Check]] = {}
    for c in checks:
        by_category.setdefault(c.category, []).append(c)
    print(f"{ANSI_BLUE}AI-text detector: {len(checks)} checks "
          f"in {len(by_category)} suites{ANSI_RESET}\n")
    for category in by_category:
        print(f"{ANSI_BLUE}{category}{ANSI_RESET}")
        for c in by_category[category]:
            tag = f"{c.severity.color}{c.severity.value.upper():5}{ANSI_RESET}"
            print(f"  {tag}  {c.id}\n         {ANSI_DIM}{c.description}{ANSI_RESET}")
        print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect AI-generated-text tells in Markdown articles."
    )
    parser.add_argument(
        "paths", nargs="*",
        help="Files or directories to scan. Defaults to draft articles in content/.",
    )
    parser.add_argument(
        "--file", action="append", default=[],
        help="Markdown file to scan. May be passed more than once.",
    )
    parser.add_argument(
        "--config-dir", default=str(DEFAULT_CONFIG_DIR),
        help="Directory holding the *.txt rule lists (default: config/ai-tells).",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Fail (exit 1) on warnings as well as errors.",
    )
    parser.add_argument(
        "--list-checks", action="store_true",
        help="Print the check registry and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cfg = Path(args.config_dir)
    checks = build_registry(cfg)

    if args.list_checks:
        print_registry(checks)
        return 0

    allowlist = load_allowlist(cfg / "allowlist.txt")
    files = collect_files(args.paths, args.file)
    if not files:
        print(f"{ANSI_GREEN}  no files to scan{ANSI_RESET}")
        return 0

    findings_by_path: dict[str, list[Finding]] = {}
    for fp in files:
        findings = scan_document(Document.from_path(fp), checks, allowlist)
        if findings:
            findings_by_path[str(fp)] = findings

    errors, warnings = report(findings_by_path)

    print("")
    if errors == 0 and warnings == 0:
        print(f"{ANSI_GREEN}  no AI-text tells found in "
              f"{len(files)} file(s){ANSI_RESET}")
        return 0

    summary = f"{errors} error(s), {warnings} warning(s) across {len(findings_by_path)} file(s)"
    if errors or (args.strict and warnings):
        print(f"{ANSI_RED}  {summary}{ANSI_RESET}")
        return 1
    print(f"{ANSI_YELLOW}  {summary} (warnings only){ANSI_RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
