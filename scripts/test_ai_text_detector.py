#!/usr/bin/env python3
"""Tests for scripts/ai-text-detector.py.

Stdlib unittest only -- no third-party dependency. Run with:

    python3 scripts/test_ai_text_detector.py        # or: just ai-text-detect-test

The detector lives at a hyphenated path (not importable normally), so it is
loaded via importlib. Suite-level tests use the real config/ai-tells/*.txt
lists so the tests track the data the CI actually ships.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "ai-text-detector.py"
CFG = REPO_ROOT / "config" / "ai-tells"

_spec = importlib.util.spec_from_file_location("ai_text_detector", SCRIPT)
assert _spec and _spec.loader
mod = importlib.util.module_from_spec(_spec)
# Register before exec so dataclasses can resolve field types under py3.9.
sys.modules[_spec.name] = mod
_spec.loader.exec_module(mod)

REGISTRY = mod.build_registry(CFG)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def make_doc(text: str):
    return mod.Document(Path("test.md"), text)


def findings(text: str, checks=None) -> list:
    return mod.scan_document(make_doc(text), checks or REGISTRY, set())


def categories(text: str) -> set[str]:
    return {f.category for f in findings(text)}


def check_ids(text: str) -> set[str]:
    return {f.check_id for f in findings(text)}


# --------------------------------------------------------------------------
# Document model
# --------------------------------------------------------------------------

class TestDocument(unittest.TestCase):
    def test_front_matter_is_not_scanned(self):
        text = "---\ntitle: We delve into things\ndraft: true\n---\n\nClean body.\n"
        self.assertNotIn("cliches", categories(text))

    def test_fenced_code_is_not_scanned(self):
        text = "Real text.\n\n```\nlet's delve into the tapestry\n```\n"
        self.assertEqual(findings(text), [])

    def test_inline_code_is_masked_but_surrounding_text_is_not(self):
        flagged = findings("Please delve into the docs.")
        self.assertTrue(any(f.check_id == "cliches.lexical" for f in flagged))
        self.assertEqual(findings("Use the `delve` flag here."), [])

    def test_link_url_is_masked(self):
        # "delve" living only inside a URL must not be flagged.
        self.assertEqual(findings("See [the guide](https://x.com/delve-deep)."), [])

    def test_headings_parsed(self):
        doc = make_doc("# Title One\n\nbody\n\n## Sub Heading\n")
        self.assertEqual([(h.level, h.text) for h in doc.headings],
                         [(1, "Title One"), (2, "Sub Heading")])

    def test_paragraphs_split_on_blank_lines(self):
        doc = make_doc("First para.\n\nSecond para line one.\nstill second.\n")
        self.assertEqual(len(doc.paragraphs), 2)
        self.assertEqual(doc.paragraphs[0].start_line, 1)


# --------------------------------------------------------------------------
# Phrase compilation / config loading
# --------------------------------------------------------------------------

class TestPhraseMatching(unittest.TestCase):
    def test_case_insensitive(self):
        self.assertTrue(mod.compile_phrase("delve").search("We DELVE in"))

    def test_word_boundaries(self):
        rx = mod.compile_phrase("delve")
        self.assertIsNone(rx.search("delved"))
        self.assertIsNone(rx.search("bedelve"))

    def test_curly_apostrophe_and_flexible_whitespace(self):
        rx = mod.compile_phrase("it's worth noting")
        self.assertTrue(rx.search("it’s worth noting"))
        self.assertTrue(rx.search("it's   worth\tnoting"))

    def test_trailing_punctuation_phrase(self):
        self.assertTrue(mod.compile_phrase("the catch?").search("The catch?"))

    def test_load_entries_parses_suggestion_and_skips_comments(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
            fh.write("# comment\n\nutilize => use\nplainword\n")
            path = Path(fh.name)
        try:
            entries = mod.load_entries(path)
            phrases = {p: s for _, p, s in entries}
            self.assertEqual(phrases, {"utilize": "use", "plainword": ""})
        finally:
            path.unlink()


class TestPhraseListCheck(unittest.TestCase):
    def test_uses_suggestion_as_message(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
            fh.write("foo => bar\n")
            path = Path(fh.name)
        try:
            check = mod.PhraseListCheck("t.x", "test", mod.WARN, path, "fallback")
            fs = list(check.run(make_doc("we foo things")))
            self.assertEqual(len(fs), 1)
            self.assertEqual(fs[0].message, "bar")
            self.assertEqual(fs[0].severity, mod.WARN)
            self.assertEqual(fs[0].line, 1)
        finally:
            path.unlink()


# --------------------------------------------------------------------------
# Each "giveaway" suite fires
# --------------------------------------------------------------------------

class TestSuitesFire(unittest.TestCase):
    CASES = {
        "cliches": "Let's delve into the details today.",
        "contrast-framing": "It's not just a linter, it's a revolution.",
        "rule-of-three": "It is efficient, effective, and reliable here.",
        "cringe-questions": "We shipped it. The catch? It broke.",
        "ing-verbs": "We did it, highlighting the key benefits clearly.",
        "glazing": "It's worth noting that the parser is fast.",
        "formal-words": "We utilize the cache to speed reads.",
        "symbolic": "This signifies a deeper change in the team.",
        "fabricated-names": "As Sarah Chen discovered last year.",
        "summary-endings": "To summarize, the parser is fast.",
        "despite-challenges": "Despite these challenges, we shipped on time.",
        "puffery": "Our groundbreaking, revolutionary engine ships today.",
        "vague-attributions": "Studies show that caching helps a lot.",
        "hedging": "Arguably, the parser is generally speaking fast.",
        "transition-overuse": "Moreover, the cache helps reads.",
        "emoji": "We shipped it today \U0001F680 finally.",
    }

    def test_each_suite_fires(self):
        for category, text in self.CASES.items():
            with self.subTest(category=category):
                self.assertIn(category, categories(text))

    def test_clean_prose_is_silent(self):
        clean = (
            "I rewrote the parser last week. It was slower than expected, "
            "so I profiled it and found a quadratic loop in the tokenizer."
        )
        self.assertEqual(findings(clean), [])


# --------------------------------------------------------------------------
# Split suites -- every word-list giveaway has >= 2 named checks
# --------------------------------------------------------------------------

class TestSplitSuites(unittest.TestCase):
    def test_cliches_split(self):
        self.assertIn("cliches.lexical", check_ids("Let's delve into it."))
        self.assertIn("cliches.phrase", check_ids("We embark on a journey now."))

    def test_glazing_split(self):
        self.assertIn("glazing.openers", check_ids("It's worth noting the cache helps."))
        self.assertIn("glazing.qualifiers", check_ids("Needless to say, it works."))

    def test_formal_words_split(self):
        self.assertIn("formal-words.verbs", check_ids("We utilize a cache."))
        self.assertIn("formal-words.quantifiers", check_ids("A plethora of options exist."))

    def test_symbolic_split(self):
        self.assertIn("symbolic.verbs", check_ids("It signifies a change."))
        self.assertIn("symbolic.phrases", check_ids("It serves as a reminder to us."))

    def test_puffery_split(self):
        self.assertIn("puffery.adjectives", check_ids("A groundbreaking result here."))
        self.assertIn("puffery.compounds", check_ids("A world-class system here."))

    def test_vague_attributions_split(self):
        self.assertIn("vague-attributions.research", check_ids("Studies show it helps."))
        self.assertIn("vague-attributions.consensus", check_ids("Experts agree it helps."))

    def test_hedging_split(self):
        self.assertIn("hedging.adverbs", check_ids("Arguably the best option here."))
        self.assertIn("hedging.phrases", check_ids("To some extent it works here."))

    def test_despite_challenges_split(self):
        self.assertIn("despite-challenges.list",
                      check_ids("Despite these challenges, we shipped."))
        self.assertIn("despite-challenges.rosy-future",
                      check_ids("The future is bright for the team."))

    def test_fabricated_names_intro(self):
        self.assertIn("fabricated-names.intro",
                      check_ids("Imagine a developer named Mia at work."))

    def test_emoji_density(self):
        self.assertIn(
            "emoji.density",
            check_ids("Wow \U0001F680 so \U0001F525 cool \U0001F4A1 indeed."),
        )

    def test_gerund_heading(self):
        self.assertIn("headings.gerund-opener",
                      check_ids("## Understanding the parser\n\nbody\n"))

    def test_paragraph_uniformity(self):
        para = (" ".join(["alpha"] * 30)) + "."
        self.assertIn("natural-flow.paragraph-uniformity",
                      check_ids("\n\n".join([para] * 4)))


# --------------------------------------------------------------------------
# Severity classification (the false-positive guardrail)
# --------------------------------------------------------------------------

class TestSeverity(unittest.TestCase):
    def _sev(self, text, check_id):
        for f in findings(text):
            if f.check_id == check_id:
                return f.severity
        return None

    def test_antithesis_contrast_is_error(self):
        self.assertEqual(
            self._sev("It's not just fast, it's instant.", "contrast.not-x-its-y"),
            mod.ERROR,
        )

    def test_not_only_but_is_only_warning(self):
        # Legitimate human construction -> must never fail the build.
        sev = self._sev("It is not only fast but cheap to run.", "contrast.not-only-but")
        self.assertEqual(sev, mod.WARN)

    def test_formal_words_are_warnings(self):
        self.assertEqual(self._sev("We utilize a cache.", "formal-words.verbs"), mod.WARN)


# --------------------------------------------------------------------------
# Allowlist
# --------------------------------------------------------------------------

class TestAllowlist(unittest.TestCase):
    def test_allowlist_suppresses_matching_finding(self):
        text = "As Sarah Chen noted in her talk."
        without = mod.scan_document(make_doc(text), REGISTRY, set())
        with_allow = mod.scan_document(make_doc(text), REGISTRY, {"sarah chen"})
        self.assertTrue(any(f.check_id == "fabricated-names.list" for f in without))
        self.assertFalse(any(f.check_id == "fabricated-names.list" for f in with_allow))


# --------------------------------------------------------------------------
# Structural checks
# --------------------------------------------------------------------------

class TestStructuralChecks(unittest.TestCase):
    def test_tricolon(self):
        self.assertIn(
            "rule-of-three.tricolon",
            check_ids("It will save time, reduce costs, and increase revenue today."),
        )

    def test_cringe_short_fragment(self):
        self.assertIn("cringe-questions.short-fragment",
                      check_ids("It works. The gotcha? Latency."))

    def test_ing_after_comma_is_stronger_signal(self):
        ids = check_ids("We shipped it, leveraging the new cache.")
        self.assertIn("ing-verbs.after-comma", ids)

    def test_title_case_heading(self):
        self.assertIn("headings.title-case",
                      check_ids("## The Best Way To Write Code\n\nbody\n"))

    def test_sentence_case_heading_is_clean(self):
        self.assertNotIn("headings.title-case",
                         check_ids("## Why I left my last job\n\nbody\n"))

    def test_summary_heading(self):
        self.assertIn("summary-endings.heading", check_ids("## Conclusion\n\nbody\n"))

    def test_transition_density(self):
        text = ("However, it works. Moreover, it scales. Furthermore, it is cheap. "
                "Additionally, it is fast.")
        self.assertIn("transition-overuse.density", check_ids(text))

    def test_real_emoji_is_flagged(self):
        self.assertIn("emoji", categories("We shipped it \U0001F680 today."))
        self.assertIn("emoji", categories("Done ✅ and dusted."))

    def test_arrows_are_not_emoji(self):
        # "->" is technical notation in this blog, not an emoji explosion.
        self.assertNotIn("emoji", categories("The flow is read -> parse -> render."))
        self.assertNotIn("emoji", categories("Step A → Step B ← back."))

    def test_sentence_uniformity(self):
        # Four sentences of nearly identical length -> low burstiness.
        s = "The quick brown fox jumped over lazy dogs nearby."
        self.assertIn("natural-flow.sentence-uniformity",
                      check_ids(" ".join([s] * 4)))


# --------------------------------------------------------------------------
# File discovery
# --------------------------------------------------------------------------

class TestDiscovery(unittest.TestCase):
    def test_is_draft_and_find_drafts(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            draft = root / "a.md"
            published = root / "b.md"
            draft.write_text("---\ndraft: true\n---\nbody\n")
            published.write_text("---\ndraft: false\n---\nbody\n")
            self.assertTrue(mod.is_draft(draft))
            self.assertFalse(mod.is_draft(published))
            self.assertEqual(mod.find_drafts(root), [draft])

    def test_collect_files_expands_directories(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "x.md").write_text("body\n")
            (root / "y.md").write_text("body\n")
            collected = mod.collect_files([str(root)], [])
            self.assertEqual({p.name for p in collected}, {"x.md", "y.md"})


# --------------------------------------------------------------------------
# CLI / exit codes (integration)
# --------------------------------------------------------------------------

class TestCLI(unittest.TestCase):
    def _run(self, content, *extra):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write(content)
            path = fh.name
        try:
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--file", path, *extra],
                cwd=REPO_ROOT, capture_output=True, text=True,
            )
        finally:
            Path(path).unlink()

    def test_errors_exit_nonzero(self):
        r = self._run("It's not just fast, it's instant.\n")
        self.assertEqual(r.returncode, 1)

    def test_clean_exits_zero(self):
        r = self._run("I profiled the parser and fixed a quadratic loop.\n")
        self.assertEqual(r.returncode, 0)

    def test_warnings_pass_unless_strict(self):
        warn_only = "We utilize a cache for reads.\n"
        self.assertEqual(self._run(warn_only).returncode, 0)
        self.assertEqual(self._run(warn_only, "--strict").returncode, 1)

    def test_list_checks_runs(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--list-checks"],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("contrast-framing", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
