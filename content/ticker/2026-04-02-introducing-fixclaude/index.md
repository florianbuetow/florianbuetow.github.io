---
title: "Introducing /fixclaude"
date: 2026-04-02
draft: false
description: "fixclaude installs 279 lines of directives that override seven structural bottlenecks baked into Claude Code, including the employee-only verification gate."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools", "Ticker News"]
tags: ["Claude Code", "Plugin", "Open Source"]
---

![Introducing fixclaude](illustration.webp?zoom "Infographic: Overcomming the 8 Hidden Limitations of Claude Code")

People were quick to analyze the leaked Claude Code codebase and the findings are startling: Anthropic is aware of Claude Code's "laziness" and hallucinations, but the most effective fixes are gated to employees only.

Internal comments in the source code are reported to document a 29-30% false-claims rate for external users because a critical "verification loop" (type-checking, linting, and testing) is restricted to those with an internal employee flag.

Luckily, we can reverse these choices by optimizing the CLAUDE.md file. I've turned these reverse-engineered recommendations into a new plugin called **fixclaude**.

---

## What fixclaude fixes

fixclaude installs 279 lines of directives that override seven structural bottlenecks baked into the Claude Code source:

- **The Employee-Only Gate:** Forces a mandatory verification loop (type-check, lint, test) before the agent can report a task as "Done."
- **The Context Death Spiral:** Prevents auto-compaction from silently nuking your reasoning and file history at ~167K tokens.
- **The Brevity Mandate:** Countermands the system prompt's "simplest approach" instruction with a Senior Dev "perfectionist" override.
- **The 2,000-Line Blind Spot:** Fixes the hard cap that causes Claude to silently truncate and hallucinate the end of large files.
- **Tool Result Blindness:** Implements "truncation awareness" for searches that are otherwise capped at a 2,000-byte preview.
- **Unlocking Parallel Capacity:** Mandates sub-agent swarming for large tasks, expanding your working memory from 167K to 835K tokens.
- **Semantic Search Fix:** Forces multi-step searches to catch dynamic imports and re-exports that standard grep misses.

## Four new commands for your workflow

- `/fixclaude` - Auto-detects and routes to installation or updates.
- `/fixclaude:init` - Creates a fresh, 9-section CLAUDE.md template.
- `/fixclaude:update` - Merges missing directives into your existing files without ruining your formatting.
- `/fixclaude:analyze` - Produces a gap report rating your current setup against all seven findings.

While a bandage like this isn't a perfect substitute for source-level changes, it is far better than leaving an "open wound" in your development workflow.

Comment on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7445334252608606208/)

## References

- fixclaude plugin on [GitHub](https://github.com/florianbuetow/claude-code/)
