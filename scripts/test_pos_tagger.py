#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "spacy==3.8.7",
#   "click<9",
#   "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""Tests for scripts/pos-tagger.py.

Run with:

    uv run scripts/test_pos_tagger.py        # or: just pytest-pos-tag

The tagger lives at a hyphenated path (not importable normally), so it is
loaded via importlib. The model is loaded once for the whole suite. Tests focus
on the hard core of the feature: which Markdown / Hugo constructs are preserved
verbatim vs. have their prose replaced by POS tags.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "pos_tagger", Path(__file__).with_name("pos-tagger.py")
)
assert _spec and _spec.loader
pt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pt)


class TaggerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nlp = pt.load_nlp()

    def md(self, text: str) -> str:
        return pt.tag_markdown(text, self.nlp)

    # --- prose tagging -------------------------------------------------------

    def test_words_become_pos_tags(self):
        # "Cats" -> NOUN, "run" -> VERB; the original words are gone.
        out = pt.tag_prose("Cats run", self.nlp)
        self.assertEqual(out, "NOUN VERB")

    def test_punctuation_kept_verbatim(self):
        out = pt.tag_prose("Cats, dogs!", self.nlp)
        self.assertIn(",", out)
        self.assertIn("!", out)
        self.assertNotIn("Cats", out)

    def test_numbers_tagged_num(self):
        self.assertIn("NUM", pt.tag_prose("I have 3 cats", self.nlp))

    # --- verbatim constructs -------------------------------------------------

    def test_front_matter_verbatim(self):
        src = "---\ntitle: Hello\ndraft: true\n---\nCats run today.\n"
        out = self.md(src)
        self.assertTrue(out.startswith("---\ntitle: Hello\ndraft: true\n---\n"))
        self.assertNotIn("Cats", out)

    def test_fenced_code_verbatim(self):
        src = "Text here.\n```python\ncats = run_fast()\n```\nMore text.\n"
        out = self.md(src)
        self.assertIn("cats = run_fast()", out)
        self.assertIn("```python", out)
        self.assertNotIn("Text here.", out)  # prose around the fence is tagged

    def test_inline_code_verbatim(self):
        out = self.md("Call `cats_method()` now.\n")
        self.assertIn("`cats_method()`", out)
        self.assertNotIn("now.", out)

    def test_link_url_kept_text_tagged(self):
        out = self.md("See [the docs](https://example.com/page) now.\n")
        self.assertIn("](https://example.com/page)", out)
        self.assertNotIn("[the docs]", out)  # link text was tagged

    def test_image_url_kept_alt_tagged(self):
        out = self.md("![a happy cat](/img/cat.png)\n")
        self.assertIn("](/img/cat.png)", out)
        self.assertTrue(out.startswith("!["))
        self.assertNotIn("happy", out)

    def test_emphasis_markers_preserved(self):
        out = self.md("This is **bold** and *very* _italic_ text.\n").strip()
        self.assertIn("**", out)            # strong markers survive
        self.assertIn("_", out)             # underscore-italic markers survive
        self.assertTrue(out.count("*") >= 4)  # **...** plus *...*
        for word in ("bold", "very", "italic"):
            self.assertNotIn(word, out)     # emphasised words were tagged

    def test_footnote_ref_verbatim(self):
        out = self.md("This matters[^1] greatly.\n")
        self.assertIn("[^1]", out)

    def test_self_closing_shortcode_verbatim(self):
        out = self.md('{{< audio src="x.mp3" >}}\n')
        self.assertEqual(out, '{{< audio src="x.mp3" >}}\n')

    # --- marker preserved, prose tagged --------------------------------------

    def test_heading_marker_preserved(self):
        out = self.md("## Happy Cats\n")
        self.assertTrue(out.startswith("## "))
        self.assertNotIn("Happy", out)

    def test_blockquote_marker_preserved(self):
        out = self.md("> Cats run fast.\n")
        self.assertTrue(out.startswith("> "))
        self.assertNotIn("Cats", out)

    def test_list_markers_preserved(self):
        self.assertTrue(self.md("- Cats run\n").startswith("- "))
        self.assertTrue(self.md("1. Cats run\n").startswith("1. "))

    def test_shortcode_tags_verbatim_body_tagged(self):
        out = self.md("{{% citenote %}}cats run wild{{% /citenote %}}\n")
        self.assertIn("{{% citenote %}}", out)
        self.assertIn("{{% /citenote %}}", out)
        self.assertNotIn("cats run wild", out)

    def test_bare_url_does_not_eat_following_markup(self):
        # Regression: a bare URL must stop at </a> and not swallow the closing
        # shortcode's {{< delimiter.
        src = '{{< sidenote >}}<a href="x">https://ex.com/p</a>{{< /sidenote >}}\n'
        out = self.md(src)
        self.assertIn("{{< sidenote >}}", out)
        self.assertIn("{{< /sidenote >}}", out)
        self.assertIn("https://ex.com/p", out)
        self.assertNotIn("X", out)  # /sidenote must not leak through to spaCy

    def test_block_shortcode_body_prose_tagged(self):
        src = '{{< sidenote "Term" >}}\nCats run wild.\n{{< /sidenote >}}\n'
        out = self.md(src)
        self.assertIn('{{< sidenote "Term" >}}', out)
        self.assertIn("{{< /sidenote >}}", out)
        self.assertNotIn("Cats run wild", out)

    # --- naming --------------------------------------------------------------

    def test_slug_bundle_vs_flat(self):
        self.assertEqual(pt.slug_for(Path("content/blog/my-post/index.md")), "my-post")
        self.assertEqual(pt.slug_for(Path("content/blog/my-post.md")), "my-post")

    def test_structure_preserved_no_reflow(self):
        # Blank lines and paragraph breaks survive untouched.
        out = self.md("First line.\n\nSecond line.\n")
        self.assertIn("\n\n", out)


if __name__ == "__main__":
    unittest.main()
