---
title: "Claude Plugin: Automate Your CHANGELOG.md"
slug: "automate-your-changelog-md-with-this-claude-code-plugin"
date: 2026-03-30
draft: false
description: "A Claude Code plugin that reads your Git history and writes a proper CHANGELOG.md following Keep a Changelog format - one command, no config, no templates."
author: "Florian Buetow"
readTime: "3 min read"
categories: ["AI Engineering", "Tools"]
tags: ["Claude Code", "Plugin", "Open Source"]
---

Unless you already automated maintaining `CHANGELOG.md` in your projects, you might find this skill useful.

The changelog skill reads your Git history and writes a proper `CHANGELOG.md` following the "Keep a Changelog" format with semantic versioning. One command. No config. No templates.

Available commands:

```
/changelog         # auto-detects: creates new or updates existing
/changelog:create  # generate from full git history
/changelog:update  # append new version to existing changelog
```

Here's what happens under the hood:

**1. Version Boundary Detection.** Finds all semver tags and slices the commit history into version ranges. No tags? Everything goes under `[Unreleased]`. Mixed tagged and untagged commits? Tagged versions get dated sections; new commits land in `[Unreleased]` until you cut the next release.

**2. Commit Classification.** Every commit gets categorized into Added, Changed, Deprecated, Removed, Fixed, or Security. Conventional commit prefixes (`feat:`, `fix:`, `refactor:`) take priority - keyword matching is the fallback. Merge commits are skipped automatically.

**3. Synthesis, Not Copy-Paste.** Related commits get grouped into single user-facing bullet points. "Fixed crash when uploading large files", not "fix: null check in upload handler." Internal noise (CI tweaks, trivial chores, docs-only changes) gets filtered unless it affects users.

**4. Incremental Updates.** Already have a changelog? `/changelog:update` finds the boundary commit for the last documented version, analyzes only new commits since then, and inserts the new version section without touching existing entries.

**5. Version Comparison Links.** Reference-style links at the bottom, auto-generated from your Git remote URL. Each version links to the diff between that tag and the previous one. `[Unreleased]` always points to the latest tag vs. HEAD.

The key distinction from dumping `git log --oneline` into a file: the changelog describes what users see and feel. Commits describe what engineers did. These are not the same thing, and the gap between them is precisely what makes changelogs tedious to maintain manually.

```
claude plugin marketplace add florianbuetow/claude-code
claude plugin install changelog
/reload-plugins
```

[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7444246959869087744/)

## References

- [changelog plugin on GitHub](https://github.com/florianbuetow/claude-code)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
