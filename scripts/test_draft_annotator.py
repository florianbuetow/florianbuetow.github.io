#!/usr/bin/env python3
"""Tests for scripts/draft_annotator.py."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "draft_annotator.py"

_spec = importlib.util.spec_from_file_location("draft_annotator", SCRIPT)
assert _spec and _spec.loader
mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = mod
_spec.loader.exec_module(mod)


class DraftAnnotatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def write_doc(self, rel: str, draft: bool, body: str) -> Path:
        path = self.tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            f"title: {rel}\n"
            f"draft: {'true' if draft else 'false'}\n"
            "---\n\n"
            f"{body}\n",
            encoding="utf-8",
        )
        return path

    def test_find_draft_articles_scans_whole_tree(self):
        self.write_doc("blog/a/index.md", True, "A")
        self.write_doc("blog/b.md", False, "B")
        self.write_doc("ticker/c/index.md", True, "C")

        drafts = mod.find_draft_articles(self.tmp)

        self.assertEqual(
            [doc.path.relative_to(self.tmp).as_posix() for doc in drafts],
            ["blog/a/index.md", "ticker/c/index.md"],
        )

    def test_validate_fails_only_when_published_article_has_draftnote(self):
        self.write_doc("draft/index.md", True, "<!-- DRAFTNOTE\nnote: x\n-->")
        self.write_doc("published/index.md", False, "Clean.")

        self.assertEqual(mod.validate_annotations(self.tmp), 0)

        self.write_doc("published/index.md", False, "<!-- DRAFTNOTE\nnote: x\n-->")

        self.assertEqual(mod.validate_annotations(self.tmp), 1)

    def test_quote_matches_markdown_rendered_text(self):
        path = self.write_doc(
            "blog/post/index.md",
            True,
            "Read [the guide](https://example.com) before shipping.[^x]\n\n[^x]: source",
        )
        doc = mod.parse_markdown(path)

        match = mod.find_quote_block(doc, "the guide before shipping")

        self.assertIn("[the guide]", match.text)

    def test_quote_matches_shortcode_sidenote_body(self):
        path = self.write_doc(
            "blog/post/index.md",
            True,
            '{{< sidenote label="Note" >}}This framing technique is sometimes called persona prompting.{{< /sidenote >}}',
        )
        doc = mod.parse_markdown(path)

        match = mod.find_quote_block(doc, "This framing technique is sometimes called persona prompting.")

        self.assertIn("sidenote", match.text)

    def test_sidenote_source_disambiguates_repeated_quote(self):
        repeated = "Repeated quote appears here."
        path = self.write_doc(
            "blog/post/index.md",
            True,
            repeated
            + "\n\n"
            + f'{{{{< sidenote label="Note" >}}}}{repeated}{{{{< /sidenote >}}}}',
        )
        doc = mod.parse_markdown(path)

        with self.assertRaisesRegex(mod.AnnotatorError, "multiple"):
            mod.find_quote_block(doc, repeated)

        match = mod.find_quote_block(doc, repeated, source="sidenote")

        self.assertEqual(match.source, "sidenote")
        self.assertIn("sidenote", match.text)

    def test_annotate_can_target_ambiguous_sidenote(self):
        repeated = "Repeated quote appears here."
        path = self.write_doc(
            "blog/post/index.md",
            True,
            repeated
            + "\n\n"
            + f'{{{{< sidenote label="Note" >}}}}{repeated}{{{{< /sidenote >}}}}\n\n'
            + "Trailing paragraph.",
        )

        with mock.patch.object(mod, "CONTENT_ROOT", self.tmp):
            result = mod.annotate_file(
                "blog/post/index.md",
                repeated,
                "Sidenote only.",
                created="2026-06-07T00:00:00+00:00",
                source="sidenote",
            )

        text = path.read_text(encoding="utf-8")
        self.assertEqual(result["source"], "sidenote")
        self.assertLess(text.index("{{< sidenote"), text.index("<!-- DRAFTNOTE"))
        self.assertLess(text.index("<!-- DRAFTNOTE"), text.index("Trailing paragraph."))

    def test_ambiguous_quote_is_rejected(self):
        path = self.write_doc("blog/post/index.md", True, "Same line.\n\nSame line.")
        doc = mod.parse_markdown(path)

        with self.assertRaisesRegex(mod.AnnotatorError, "multiple"):
            mod.find_quote_block(doc, "Same line")

    def test_annotate_rejects_non_draft(self):
        self.write_doc("blog/post/index.md", False, "Target paragraph.")

        with mock.patch.object(mod, "CONTENT_ROOT", self.tmp):
            with self.assertRaisesRegex(mod.AnnotatorError, "draft"):
                mod.annotate_file("blog/post/index.md", "Target paragraph", "Needs work.")

    def test_annotate_inserts_after_matching_block(self):
        path = self.write_doc(
            "blog/post/index.md",
            True,
            "First paragraph.\n\nSecond paragraph with a target phrase.\n\nThird paragraph.",
        )

        with mock.patch.object(mod, "CONTENT_ROOT", self.tmp):
            result = mod.annotate_file(
                "blog/post/index.md",
                "target phrase",
                "Tighten this.",
                created="2026-06-07T00:00:00+00:00",
            )

        text = path.read_text(encoding="utf-8")
        self.assertTrue(result["ok"])
        self.assertIn('quote: "target phrase"', text)
        self.assertIn('note: "Tighten this."', text)
        self.assertLess(text.index("Second paragraph"), text.index("<!-- DRAFTNOTE"))
        self.assertLess(text.index("<!-- DRAFTNOTE"), text.index("Third paragraph"))

    def test_comment_delimiters_are_rejected(self):
        with self.assertRaisesRegex(mod.AnnotatorError, "comment delimiters"):
            mod.sanitize_field("note", "break --> comment", 100)

    def test_path_traversal_is_rejected(self):
        with self.assertRaisesRegex(mod.AnnotatorError, "escapes"):
            mod.safe_content_path("../outside.md", self.tmp)


if __name__ == "__main__":
    unittest.main()
