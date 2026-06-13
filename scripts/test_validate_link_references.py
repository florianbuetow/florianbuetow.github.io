#!/usr/bin/env python3
"""Tests for scripts/validate-link-references.py.

Stdlib unittest only -- no third-party dependency. Run with:

    python3 scripts/test_validate_link_references.py   # or: just validate-link-references-test

The checker lives at a hyphenated path (not importable normally), so it is
loaded via importlib.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate-link-references.py"

_spec = importlib.util.spec_from_file_location("validate_link_references", SCRIPT)
assert _spec and _spec.loader
mod = importlib.util.module_from_spec(_spec)
# Register before exec so dataclasses can resolve field types under older py.
sys.modules[_spec.name] = mod
_spec.loader.exec_module(mod)


def kinds(text: str) -> list[str]:
    return [v.kind for v in mod.analyze_text(text)]


def messages(text: str) -> list[str]:
    return [v.message for v in mod.analyze_text(text)]


# --------------------------------------------------------------------------
# extract_links: the generic helper (string in -> ordered, deduped URLs out)
# --------------------------------------------------------------------------

class TestExtractLinks(unittest.TestCase):
    def test_markdown_link(self):
        self.assertEqual(mod.extract_links("see [t](https://t.example)"), ["https://t.example"])

    def test_image_excluded(self):
        self.assertEqual(mod.extract_links("![alt](https://img.example/a.png)"), [])

    def test_html_href(self):
        self.assertEqual(
            mod.extract_links('<a href="https://h.example" target="_blank">x</a>'),
            ["https://h.example"],
        )

    def test_bare_url_ignored(self):
        self.assertEqual(mod.extract_links("see https://bare.example for more"), [])

    def test_footnote_marker_not_link(self):
        self.assertEqual(mod.extract_links("A claim.[^ref]"), [])

    def test_footnote_definition_bare_url_ignored(self):
        self.assertEqual(mod.extract_links("[^ref]: Source. https://bare.example"), [])

    def test_dedup_preserves_first_appearance_order(self):
        text = "[a](https://1) [b](https://2) [c](https://1) [d](https://3)"
        self.assertEqual(mod.extract_links(text), ["https://1", "https://2", "https://3"])

    def test_linkedin_post_excluded(self):
        self.assertEqual(
            mod.extract_links("[c](https://www.linkedin.com/posts/fbuetow_abc-123)"), []
        )

    def test_linkedin_feed_excluded(self):
        self.assertEqual(
            mod.extract_links("[c](https://www.linkedin.com/feed/update/urn:li:activity:1/)"), []
        )

    def test_linkedin_profile_kept(self):
        url = "https://www.linkedin.com/in/esteevanderwalt/"
        self.assertEqual(mod.extract_links(f"[p]({url})"), [url])

    def test_links_in_shortcode_counted(self):
        text = '{{< sidenote label="x" >}}see [docs](https://d.example){{< /sidenote >}}'
        self.assertEqual(mod.extract_links(text), ["https://d.example"])

    def test_links_in_code_fence_ignored(self):
        text = "```\n[x](https://code.example)\n```\n[y](https://real.example)\n"
        self.assertEqual(mod.extract_links(text), ["https://real.example"])

    def test_markdown_title_stripped(self):
        self.assertEqual(
            mod.extract_links('[x](https://t.example "Title here")'), ["https://t.example"]
        )

    def test_angle_bracket_destination(self):
        self.assertEqual(
            mod.extract_links("[x](<https://a.example/path>)"), ["https://a.example/path"]
        )

    def test_same_page_anchor_excluded(self):
        self.assertEqual(mod.extract_links("[see](#references)"), [])

    def test_internal_site_link_kept(self):
        self.assertEqual(mod.extract_links("[other](/blog/x/)"), ["/blog/x/"])

    def test_external_link_with_fragment_kept(self):
        self.assertEqual(
            mod.extract_links("[repo](https://github.com/a/b#install)"),
            ["https://github.com/a/b#install"],
        )


# --------------------------------------------------------------------------
# analyze_text: structural rules + precedence
# --------------------------------------------------------------------------

class TestAnalyzeText(unittest.TestCase):
    def test_no_reference_section_is_skipped(self):
        text = "Body [a](https://a.example).\n\n## Some Heading\n\ntext\n"
        self.assertEqual(kinds(text), [])

    def test_clean_file_passes(self):
        text = (
            "---\ntitle: x\n---\n\n"
            'Body [t](https://t.example) and <a href="https://h.example">h</a>.\n\n'
            "## References\n\n- [t](https://t.example)\n- [h](https://h.example)\n"
        )
        self.assertEqual(kinds(text), [])

    def test_missing_link_flagged(self):
        text = (
            "Body [t](https://t.example) and [o](https://o.example).\n\n"
            "## References\n\n- [t](https://t.example)\n"
        )
        self.assertEqual(kinds(text), ["missing-link"])
        self.assertIn("https://o.example", messages(text)[0])

    def test_extra_section_links_are_allowed(self):
        text = (
            "Body [t](https://t.example).\n\n"
            "## References\n\n- [t](https://t.example)\n- [bonus](https://bonus.example)\n"
        )
        self.assertEqual(kinds(text), [])

    def test_multiple_sections_flagged(self):
        text = (
            "## Links\n\n- [a](https://a.example)\n\n"
            "## References\n\n- [a](https://a.example)\n"
        )
        self.assertEqual(kinds(text), ["multiple-sections"])

    def test_heading_after_section_flagged(self):
        text = (
            "Body [a](https://a.example).\n\n"
            "## References\n\n- [a](https://a.example)\n\n## Appendix\n\nmore\n"
        )
        self.assertEqual(kinds(text), ["heading-after-section"])

    def test_precedence_multiple_sections_wins(self):
        # Two sections AND a trailing heading AND a missing link -> only the
        # multiple-sections violation is reported.
        text = (
            "Body [missing](https://m.example).\n\n"
            "## Links\n\n## References\n\nnothing\n\n## Appendix\n"
        )
        self.assertEqual(kinds(text), ["multiple-sections"])

    def test_footnote_essay_passes(self):
        text = (
            "Claim one.[^a] Claim two.[^b]\n\n"
            "Comment on [LinkedIn](https://www.linkedin.com/posts/fbuetow_abc-123)\n\n"
            "## References\n\n"
            "[^a]: Source A. https://a.example\n"
            "[^b]: Source B. https://b.example\n"
        )
        self.assertEqual(kinds(text), [])

    def test_sources_heading_is_a_reference_section(self):
        text = (
            "Body [a](https://a.example) and [b](https://b.example).\n\n"
            "## Sources\n\n- [a](https://a.example)\n"
        )
        self.assertEqual(kinds(text), ["missing-link"])
        self.assertIn("Sources", messages(text)[0])

    def test_heading_match_is_case_insensitive(self):
        text = (
            "Body [a](https://a.example) [b](https://b.example).\n\n"
            "## rEfErEnCeS\n\n- [a](https://a.example)\n"
        )
        self.assertEqual(kinds(text), ["missing-link"])

    def test_front_matter_links_are_ignored(self):
        text = (
            '---\ntitle: t\ndescription: "[notlink](https://fm.example)"\n---\n\n'
            "Body [a](https://a.example).\n\n## References\n\n- [a](https://a.example)\n"
        )
        self.assertEqual(kinds(text), [])

    def test_internal_relative_body_link_matches_absolute_reference(self):
        # The crosspost template writes the body link relative and the matching
        # References entry absolute on our own domain. /blog/x/ and
        # https://cracking-ai-engineering.com/blog/x/ are the same destination,
        # so the relative body link must not be reported as missing.
        text = (
            "Read [interview](/blog/x/).\n\n"
            "## References\n\n"
            "- [interview](https://cracking-ai-engineering.com/blog/x/)\n"
        )
        self.assertEqual(kinds(text), [])


# --------------------------------------------------------------------------
# CLI integration (exit codes + grouped output)
# --------------------------------------------------------------------------

class TestDraftClassification(unittest.TestCase):
    def test_draft_true(self):
        self.assertTrue(mod.is_draft("---\ndraft: true\n---\n"))

    def test_draft_false(self):
        self.assertFalse(mod.is_draft("---\ndraft: false\n---\n"))

    def test_draft_missing_defaults_to_published(self):
        self.assertFalse(mod.is_draft("---\ntitle: x\n---\n"))

    def test_draft_toml_front_matter(self):
        self.assertTrue(mod.is_draft("+++\ndraft = true\n+++\n"))

    def test_no_front_matter_is_published(self):
        self.assertFalse(mod.is_draft("# Title\n\nbody\n"))


class TestCli(unittest.TestCase):
    VIOLATION = "Body [o](https://o.example).\n\n## References\n\n- nothing here\n"

    def _run_files(self, files: list[tuple[str, str]]):
        with tempfile.TemporaryDirectory() as tmp:
            args: list[str] = []
            for name, text in files:
                path = Path(tmp) / name
                path.write_text(text, encoding="utf-8")
                args += ["--file", str(path)]
            return subprocess.run(
                [sys.executable, str(SCRIPT), *args],
                capture_output=True,
                text=True,
            )

    def _run(self, text: str):
        return self._run_files([("index.md", text)])

    def test_cli_exits_zero_on_clean_file(self):
        result = self._run(
            "Body [t](https://t.example).\n\n## References\n\n- [t](https://t.example)\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cli_exits_one_and_reports_on_violation(self):
        result = self._run(self.VIOLATION)
        self.assertEqual(result.returncode, 1)
        self.assertIn("https://o.example", result.stdout)

    def test_cli_draft_violation_is_a_nonblocking_warning(self):
        result = self._run_files([("a.md", "---\ndraft: true\n---\n\n" + self.VIOLATION)])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("https://o.example", result.stdout)
        self.assertIn("warning", result.stdout.lower())

    def test_cli_published_violation_is_an_error(self):
        result = self._run_files([("a.md", "---\ndraft: false\n---\n\n" + self.VIOLATION)])
        self.assertEqual(result.returncode, 1)
        self.assertIn("https://o.example", result.stdout)

    def test_cli_mixed_published_error_dominates_exit_code(self):
        result = self._run_files(
            [
                ("pub.md", "---\ndraft: false\n---\n\n" + self.VIOLATION),
                ("drf.md", "---\ndraft: true\n---\n\n" + self.VIOLATION),
            ]
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("pub.md", result.stdout)
        self.assertIn("drf.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
