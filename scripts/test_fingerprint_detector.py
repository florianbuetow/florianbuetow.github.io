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
"""Tests for scripts/fingerprint-detector.py.

Run with:

    uv run scripts/test_fingerprint_detector.py   # or: just pytest-fingerprint-check

Loaded via importlib (hyphenated path). Model loaded once. Covers the K-gram
match (incl. punctuation), markdown/code exclusion, exact output lines, summary
strings, exit codes, and fingerprints-file generation.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

import yaml

_spec = importlib.util.spec_from_file_location(
    "fd", Path(__file__).with_name("fingerprint-detector.py")
)
fd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fd)


class FingerprintTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nlp = fd.ptag.load_nlp()
        cls.tagger = fd.ptag.ProseTagger(cls.nlp)

    # --- pure matching -------------------------------------------------------

    def test_longest_common_run(self):
        self.assertEqual(fd.longest_common_run(["A", "B", "C", "D"], ["Z", "B", "C", "D"]), (3, 1))
        self.assertEqual(fd.longest_common_run(["A", "B"], ["C", "D"]), (0, 0))

    def test_match_token_keeps_punctuation(self):
        toks = list(self.nlp("Cats, dogs."))
        by_text = {t.text: self.tagger.match_token(t) for t in toks}
        self.assertEqual(by_text[","], ",")   # punctuation kept literally
        self.assertEqual(by_text["."], ".")
        self.assertEqual(by_text["Cats"], "NOUN")  # words -> POS

    def test_pattern_includes_punctuation_tokens(self):
        pat = self.tagger.pattern("the data is mixed, but real.")
        self.assertIn(",", pat)
        self.assertIn(".", pat)

    # --- markdown / code exclusion ------------------------------------------

    def test_markdown_and_code_excluded(self):
        prose = self.tagger.extract_prose(
            "Real prose here.\n```\nsecret_code_token\n```\n"
            "See [the link words](http://example.com/x).\n"
        )
        self.assertIn("Real prose here", prose)
        self.assertIn("link words", prose)          # link text is prose
        self.assertNotIn("secret_code_token", prose)  # fenced code dropped
        self.assertNotIn("example.com", prose)        # URL dropped

    # --- K threshold ---------------------------------------------------------

    def test_short_fingerprint_never_fires(self):
        short = [{"text": "x", "pattern": ["DET", "NOUN"]}]  # len 2 < K
        self.assertEqual(fd.find_passages("The cat. The dog.", short, self.tagger), [])

    def test_kgram_match_fires(self):
        sentence = "This is the shape of the moment."
        fp = [{"text": "ORIGINAL FP", "pattern": self.tagger.pattern(sentence)}]
        passages = fd.find_passages(sentence, fp, self.tagger)
        self.assertEqual(len(passages), 1)
        self.assertEqual(passages[0]["similar"], ["ORIGINAL FP"])
        self.assertIn("shape", passages[0]["text"])  # the offending words are shown

    def test_span_words_handles_line_break(self):
        # A matched span that straddles a hard line break must not jam words.
        fp = [{"text": "FP", "pattern": self.tagger.pattern("This is the shape of the moment.")}]
        passages = fd.find_passages("This is the shape\nof the moment.", fp, self.tagger)
        self.assertEqual(len(passages), 1)
        self.assertIn("shape of", passages[0]["text"])
        self.assertNotIn("shapeof", passages[0]["text"])

    def test_multiple_examples_same_pattern_all_listed(self):
        # THE requirement: when several flagged phrases share one pattern, the
        # detected passage lists ALL of them, not just one.
        pattern = self.tagger.pattern("This is the shape of the moment.")
        fps = [{"text": "Read it as a serious signal, not a law.", "pattern": pattern},
               {"text": "And the data is mixed but real.", "pattern": pattern}]
        passages = fd.find_passages("This is the shape of the moment.", fps, self.tagger)
        self.assertEqual(len(passages), 1)                 # one detected passage
        self.assertEqual(len(passages[0]["similar"]), 2)   # BOTH examples listed
        self.assertIn("Read it as a serious signal, not a law.", passages[0]["similar"])
        self.assertIn("And the data is mixed but real.", passages[0]["similar"])

    def test_overlapping_matches_grouped_into_one_passage(self):
        full = self.tagger.pattern("This is the shape of the moment.")
        fps = [{"text": "LONG", "pattern": full},
               {"text": "SHORT", "pattern": full[:6]}]  # sub-run, overlaps LONG
        passages = fd.find_passages("This is the shape of the moment.", fps, self.tagger)
        self.assertEqual(len(passages), 1)                  # grouped, not duplicated
        self.assertIn("LONG", passages[0]["similar"])
        self.assertIn("SHORT", passages[0]["similar"])      # both listed under the span

    # --- output format -------------------------------------------------------

    def _check(self, prose: str, fingerprints):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "draft.md"
            p.write_text(prose, encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                n = fd.check_draft(p, fingerprints, self.tagger)
            return buf.getvalue(), n, p

    def test_output_format_exact(self):
        sentence = "This is the shape of the moment."
        fp = [{"text": "ORIGINAL FP", "pattern": self.tagger.pattern(sentence)}]
        out, n, p = self._check(sentence + "\n", fp)
        lines = out.split("\n")
        self.assertEqual(lines[0], f"Checking draft document: {p}")
        self.assertTrue(lines[1].startswith("DETECTED IN TEXT: "))
        self.assertEqual(lines[2], "SIMILAR AI-VOICE: ORIGINAL FP")
        self.assertTrue(lines[3].startswith("PATTERN         : "))
        self.assertEqual(lines[4], "")  # blank line after each passage
        self.assertEqual(n, 1)
        self.assertIn("Found 1 passages that potentially sound AI generated", out)

    def test_summary_no_match(self):
        out, n, _ = self._check("The cat sat on the mat.\n", [])
        self.assertEqual(n, 0)
        self.assertIn("No suspicious text found", out)
        self.assertNotIn("Potentially AI voice", out)

    # --- fingerprints file generation ---------------------------------------

    def test_fingerprints_file_generated(self):
        fps = fd.build_fingerprints(self.tagger)
        expected = sum(1 for ln in fd.SRC.read_text(encoding="utf-8").splitlines() if ln.strip())
        self.assertEqual(len(fps), expected)
        self.assertTrue(fd.FP_OUT.is_file())
        loaded = yaml.safe_load(fd.FP_OUT.read_text(encoding="utf-8"))["fingerprints"]
        self.assertEqual(len(loaded), expected)
        for e in loaded:
            self.assertIn("text", e)
            self.assertIn("pattern", e)
            self.assertTrue(e["pattern"])  # non-empty pattern string

    def test_load_fingerprints_reads_file(self):
        fd.build_fingerprints(self.tagger)
        loaded = fd.load_fingerprints()  # AC-1.3: patterns come from the yaml file
        self.assertTrue(loaded)
        self.assertIsInstance(loaded[0]["pattern"], list)  # split back into tokens
        self.assertTrue(all(isinstance(tok, str) for tok in loaded[0]["pattern"]))

    # --- exit codes ----------------------------------------------------------

    def test_bad_argument_nonzero(self):
        self.assertEqual(fd.main(["/no/such/file.md"]), 2)
        with tempfile.TemporaryDirectory() as d:
            txt = Path(d) / "notes.txt"
            txt.write_text("hi", encoding="utf-8")
            self.assertEqual(fd.main([str(txt)]), 2)

    def test_exit_zero_on_real_draft(self):
        draft = "content/blog/2026-06-04-the-bottleneck-always-moves/index.md"
        if not Path(draft).is_file():
            self.skipTest("sample draft not present")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(fd.main([draft]), 0)  # exit 0 whether or not matches found


if __name__ == "__main__":
    unittest.main()
