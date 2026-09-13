#!/usr/bin/env python3
"""Regression test for the justfile textlint file-selection contract."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JUSTFILE = REPO_ROOT / "justfile"
TRACKED_FILES = REPO_ROOT / "scripts" / "git_tracked_files.py"


class TestTextlintTrackedDrafts(unittest.TestCase):
    def test_only_tracked_markdown_drafts_are_linted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shutil.copy2(JUSTFILE, root / "justfile")
            scripts = root / "scripts"
            scripts.mkdir()
            shutil.copy2(TRACKED_FILES, scripts / TRACKED_FILES.name)

            content = root / "content"
            content.mkdir()
            self._write_article(content / "tracked-draft.md", draft=True)
            self._write_article(content / "tracked-published.md", draft=False)
            self._write_article(content / "untracked-draft.md", draft=True)
            (content / "tracked-body-mention.md").write_text(
                "---\ndraft: false\n---\n\nExample: draft: true\n", encoding="utf-8"
            )

            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "add",
                    "content/tracked-draft.md",
                    "content/tracked-published.md",
                    "content/tracked-body-mention.md",
                ],
                cwd=root,
                check=True,
            )

            textlint = root / "node_modules" / ".bin" / "textlint"
            textlint.parent.mkdir(parents=True)
            textlint.write_text(
                "#!/usr/bin/env bash\n"
                "last=''\n"
                "for arg in \"$@\"; do last=$arg; done\n"
                "printf '%s\\n' \"$last\" >> \"$TEXTLINT_TEST_LOG\"\n",
                encoding="utf-8",
            )
            textlint.chmod(0o755)

            log = root / "textlint.log"
            env = os.environ.copy()
            env["TEXTLINT_TEST_LOG"] = str(log)
            subprocess.run(
                ["just", "textlint"],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertEqual(
                log.read_text(encoding="utf-8").splitlines(),
                ["content/tracked-draft.md"],
            )

            log.unlink()
            subprocess.run(
                ["just", "textlint", "content/tracked-published.md"],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(
                log.read_text(encoding="utf-8").splitlines(),
                ["content/tracked-published.md"],
            )

            log.unlink()
            subprocess.run(
                ["just", "textlint", "content/untracked-draft.md"],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertFalse(log.exists())

    def _write_article(self, path: Path, *, draft: bool) -> None:
        value = "true" if draft else "false"
        path.write_text(f"---\ndraft: {value}\n---\n\nBody.\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
