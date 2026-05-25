---
title: "Fight Context Rot with the Progressive Disclosure Plugin for Claude Code"
slug: "prevent-context-rot-with-this-claude-code-plugin"
date: 2026-05-06
draft: false
description: "A Claude Code plugin that audits how your repository discloses documentation to AI agents, detects anti-patterns, and restructures root configuration files into thematic indexes."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools", "Ticker News"]
tags: ["Claude Code", "Plugin", "Open Source"]
---

{{< sidenote label="Download" >}}[github.com/florianbuetow/claude-code](https://github.com/florianbuetow/claude-code){{< /sidenote >}}

![From context rot to progressive disclosure](from-context-rot-to-progressive-disclosure.webp?zoom)

If your `CLAUDE.md` has grown into a monolith, every convention, every workflow rule, and every stray note inlined, it is doing the opposite of progressive disclosure. The agent loads everything at session start, burns through its instruction budget, and starts ignoring directives. That is context rot.

The progressive-disclosure plugin audits and fixes this. It scans common root configuration files (`README.md`, `AGENTS.md`, `CLAUDE.md`, …), maps their reference graphs, and detects orphaned documentation that exists on disk but is invisible to the agent.

Run `/progressive-disclosure`, and you get a report that tells you:

- How your documentation is layered: discovery metadata (always loaded), activation docs (loaded on demand), and deep-dive references (loaded only when executing against detailed content)
- Which anti-patterns are present: monolithic config files, broken references, orphaned docs, generic instructions like `write clean code`, style rules that belong in linter config, and duplicate content across files
- Whether you have exceeded the instruction budget, roughly 100 directives after the system prompt claims its share

The `/progressive-disclosure:restructure` command goes further. It rewrites your highest-precedence root configuration file with a thematic, book-style index grouped by theme (Getting Started, Architecture, Development, Security, and so on) rather than by directory structure. Each entry uses a conversational link that tells the agent *when* to load the document, not just *what* it contains. The generated section is fenced with HTML comment markers, so re-running replaces rather than duplicates.

```
claude plugin marketplace add florianbuetow/claude-code
claude plugin install progressive-disclosure
/reload-plugins
```

## Links

- Source: [github.com/florianbuetow/claude-code/…progressive-disclosure](https://github.com/florianbuetow/claude-code/tree/main/plugins/progressive-disclosure)
- My (free) marketplace: [github.com/florianbuetow/claude-code](https://github.com/florianbuetow/claude-code)
