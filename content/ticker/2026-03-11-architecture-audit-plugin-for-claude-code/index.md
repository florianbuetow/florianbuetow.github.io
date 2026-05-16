---
title: "Architecture Audit Plugin for Claude Code and Codex"
date: 2026-03-11
draft: false
description: "beyond-solid-principles audits your codebase at the architecture level across ten system-level design principles — from separation of concerns to YAGNI."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools"]
tags: ["Claude Code", "Plugin", "Open Source", "Architecture"]
---

SOLID covers class design. But architecture rot happens at a larger scale — tangled services, leaky abstractions, hidden coupling between modules, brittle failure propagation. By the time these problems surface, untangling them is far more expensive than fixing a single class.

So I built a second plugin.

**beyond-solid-principles** audits your codebase at the architecture level: modules, services, layers, and component boundaries. After installing, type `/beyond-solid-principles` and get an instant analysis covering ten system-level design principles:

- **SoC** — Separation of Concerns
- **SRP-Sys** — Single Responsibility (system-level)
- **DRY** — Don't Repeat Yourself
- **Demeter** — Law of Demeter
- **Coupling** — Loose Coupling, High Cohesion
- **Evolvability** — Build for Change
- **Resilience** — Design for Failure
- **KISS** — Keep It Simple
- **POLA** — Principle of Least Surprise
- **YAGNI** — You Aren't Gonna Need It

Each violation comes with a severity rating (HIGH / MEDIUM / LOW), the exact location, a clear explanation, and a concrete remediation suggestion. Want to focus on just one principle? Run `/sw-dry` or `/sw-coupling`. Want Claude to fix the violations? Ask it to refactor after the analysis.

The two plugins are designed to complement each other — solid-principles for class-level design, beyond-solid-principles for system-level architecture.

Works with any language and any architecture style — monoliths, microservices, serverless, event-driven, hexagonal.

```
claude plugin marketplace add florianbuetow/claude-code
claude plugin install beyond-solid-principles
```

[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7437423642940080128/)

## References

- [beyond-solid-principles plugin on GitHub](https://github.com/florianbuetow/claude-code)
