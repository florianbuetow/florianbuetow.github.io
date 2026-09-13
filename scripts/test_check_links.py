#!/usr/bin/env python3
"""External-link regression tests using temporary Git repos and localhost HTTP."""

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import importlib.util
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().with_name("check-links.py")
spec = importlib.util.spec_from_file_location("check_links", SCRIPT)
checker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checker
spec.loader.exec_module(checker)


class LinkHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.respond()

    def do_GET(self):
        self.respond()

    def respond(self):
        location = None
        if self.path.startswith("/redirect/"):
            status = int(self.path.rsplit("/", 1)[1])
            location = "/ok"
        elif self.path == "/chain":
            status, location = 302, "/redirect/301"
        elif self.path == "/redirect-missing":
            status, location = 302, "/404"
        elif self.path == "/loop":
            status, location = 302, "/loop"
        elif self.path == "/head-missing":
            status = 404 if self.command == "HEAD" else 200
        elif self.path in {"/403", "/404", "/410", "/429", "/500"}:
            status = int(self.path[1:])
        else:
            status = 200
        self.send_response(status)
        if location:
            self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, *args):
        pass


class CurlNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), LinkHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def check(self, path):
        return checker.check_url(self.base + path, timeout=3, connect_timeout=1)

    def test_redirects_to_reachable_pages_pass(self):
        for path in ["/redirect/301", "/redirect/302", "/redirect/303",
                     "/redirect/307", "/redirect/308", "/chain"]:
            with self.subTest(path=path):
                result = self.check(path)
                self.assertTrue(result.ok)
                self.assertEqual(result.final_url, self.base + "/ok")

    def test_head_404_retries_get(self):
        self.assertTrue(self.check("/head-missing").ok)

    def test_redirect_to_missing_page_is_broken(self):
        result = self.check("/redirect-missing")
        self.assertEqual(result.outcome, "broken")
        self.assertEqual(result.final_url, self.base + "/404")

    def test_confirmed_missing_pages_are_broken(self):
        for path in ["/404", "/410"]:
            with self.subTest(path=path):
                self.assertEqual(self.check(path).outcome, "broken")

    def test_denials_and_server_errors_are_unverified(self):
        for path in ["/403", "/429", "/500"]:
            with self.subTest(path=path):
                self.assertEqual(self.check(path).outcome, "unverified")

    def test_redirect_loop_does_not_pass_as_302(self):
        result = self.check("/loop")
        self.assertFalse(result.ok)
        self.assertEqual(result.outcome, "unverified")


class CheckReportingTests(unittest.TestCase):
    def test_report_written_when_all_links_are_skipped_or_no_files(self):
        for files in [[], [Path("article.md")]]:
            with self.subTest(files=files), tempfile.TemporaryDirectory() as temp:
                report = Path(temp) / "report.json"
                sources = {"https://example.com/": ["article.md:1"]} if files else {}
                with (
                    patch.object(sys, "argv", [str(SCRIPT), "--report-json", str(report)]),
                    patch.object(checker.shutil, "which", return_value="curl"),
                    patch.object(checker, "markdown_files", return_value=(files, 0)),
                    patch.object(checker, "collect_links", return_value=sources),
                    patch.object(checker, "load_skip_domains", return_value={"example.com"}),
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    self.assertEqual(checker.main(), 0)
                self.assertEqual(json.loads(report.read_text()), {
                    "results": [], "skipped": sources,
                })

    def test_transfer_error_cannot_pass_with_success_http_status(self):
        response = subprocess.CompletedProcess(
            args=[], returncode=28,
            stdout="200\nhttps://example.com/", stderr="transfer timed out",
        )
        with patch.object(checker.subprocess, "run", return_value=response):
            result = checker.check_url("https://example.com/", 1, 1)
        self.assertFalse(result.ok)
        self.assertEqual(result.outcome, "unverified")
        self.assertIn("timed out", result.detail)

    def test_exit_status_and_json_preserve_classification(self):
        for outcome, status, exit_code in [
            ("reachable", "200", 0), ("broken", "404", 1),
            ("unverified", "403", 2),
        ]:
            with self.subTest(outcome=outcome), tempfile.TemporaryDirectory() as temp:
                report = Path(temp) / "report.json"
                url = "https://example.com/article"
                result = checker.LinkCheckResult(
                    url, outcome == "reachable", status, f"HTTP {status}", outcome, url,
                )
                output = io.StringIO()
                with (
                    patch.object(sys, "argv", [str(SCRIPT), "--report-json", str(report)]),
                    patch.object(checker.shutil, "which", return_value="curl"),
                    patch.object(checker, "markdown_files", return_value=([Path("article.md")], 0)),
                    patch.object(checker, "collect_links", return_value={url: ["article.md:1"]}),
                    patch.object(checker, "load_skip_domains", return_value=set()),
                    patch.object(checker, "check_links", return_value=[result]),
                    contextlib.redirect_stdout(output),
                ):
                    self.assertEqual(checker.main(), exit_code)
                saved = json.loads(report.read_text())["results"][0]
                self.assertEqual(saved["outcome"], outcome)
                self.assertEqual(saved["sources"], ["article.md:1"])
                if outcome == "unverified":
                    self.assertIn("not confirmed broken", output.getvalue())
                    self.assertNotIn("all 1 external link target(s) reachable", output.getvalue())


class TrackedLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "content/nested folder").mkdir(parents=True)
        self.tracked = "content/nested folder/tracked article.md"
        for name, url in [
            (self.tracked, "tracked"),
            ("content/untracked.md", "untracked"),
            ("content/ignored.md", "ignored"),
            ("content/deleted.md", "deleted"),
        ]:
            (self.root / name).write_text(f"[Link](https://example.com/{url})\n")
        (self.root / ".gitignore").write_text("content/ignored.md\n")
        subprocess.run(
            ["git", "add", "--", self.tracked, "content/deleted.md"],
            cwd=self.root, check=True,
        )
        (self.root / "content/deleted.md").unlink()

    def run_checker(self, *args):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--list", *args],
            cwd=self.root, capture_output=True, text=True, check=True,
        )
        return result.stdout

    def test_default_and_directory_scan_exclude_untracked_and_ignored(self):
        for args in [(), ("content",)]:
            with self.subTest(args=args):
                self.assertEqual(self.run_checker(*args), "https://example.com/tracked\n")

    def test_explicit_untracked_file_is_skipped(self):
        for path in ["content/untracked.md", "content/ignored.md"]:
            with self.subTest(path=path):
                self.assertNotIn("https://", self.run_checker("--file", path))

    def test_explicit_tracked_relative_and_absolute_paths(self):
        for path in [self.tracked, str(self.root / self.tracked)]:
            with self.subTest(path=path):
                self.assertEqual(self.run_checker("--file", path), "https://example.com/tracked\n")

    def test_overlapping_paths_deduplicate_tracked_links(self):
        self.assertEqual(
            self.run_checker("content", self.tracked), "https://example.com/tracked\n"
        )

    def test_relative_and_absolute_arguments_scan_file_once(self):
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            files, ignored_count = checker.markdown_files(
                [self.tracked, str(self.root / self.tracked)]
            )
            self.assertEqual(len(files), 1)
            self.assertEqual(ignored_count, 0)
        finally:
            os.chdir(previous)

    def test_ignored_file_count_deduplicates_overlapping_paths(self):
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            files, ignored_count = checker.markdown_files([
                "content", "content/untracked.md", str(self.root / "content/untracked.md"),
            ])
            self.assertEqual(len(files), 1)
            self.assertEqual(ignored_count, 2)  # Untracked plus gitignored Markdown.
        finally:
            os.chdir(previous)

    def test_explicit_untracked_file_prints_ignored_count(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--file", "content/untracked.md"],
            cwd=self.root, capture_output=True, text=True, check=True,
        )
        self.assertIn("ignored 1 markdown file(s) because they are not Git-tracked", result.stdout)


if __name__ == "__main__":
    unittest.main()
