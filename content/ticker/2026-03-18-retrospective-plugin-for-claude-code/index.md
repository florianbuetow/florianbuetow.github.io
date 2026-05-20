---
title: "Retrospective Plugin for Claude Code"
date: 2026-03-18
draft: false
description: "A Claude Code plugin that runs retrospectives on your past Claude sessions to surface what's working, where you're losing time, and exactly what to fix."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools"]
tags: ["Claude Code", "Plugin", "Open Source"]
---

In engineering, retrospectives uncover work patterns that work well and those that can be improved. I built a Claude Code plugin that performs a retrospective based on your past Claude sessions to tell you how to make your interactions with Claude Code more effective.

Run `/retrospective`, and you get a report that tells you exactly:

- What's working well - and how to apply those strengths to the areas where you keep struggling
- Where and why you're losing time - bad prompts? Missing rules? A tooling gap?
- What to fix first - sorted by impact and effort, so you start with the changes that matter most
- Exactly what to change: copy-paste CLAUDE.md rules, hook configs, skill files, and a command to verify each one worked
- How your interactions have shifted since your last retro - resolved issues, recurring ones, and what's new

Retrospectives are based on up to 3 months of your project's session logs and stored as date-versioned markdown files in `docs/retrospectives/`.

```
claude plugin marketplace add florianbuetow/claude-code
claude plugin install retrospective
```

[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7439943755094237184/)

## References

- [retrospective plugin on GitHub](https://github.com/florianbuetow/claude-code)
