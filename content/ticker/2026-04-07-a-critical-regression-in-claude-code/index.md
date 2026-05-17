---
title: "A Critical Regression in Claude Code"
date: 2026-04-07
draft: false
description: "Stella Laurenzo's analysis of 234,000 tool calls reveals how redacting thinking tokens collapsed Claude Code's reasoning quality and autonomous performance."
author: "Florian Buetow"
readTime: "3 min read"
categories: ["AI Engineering"]
tags: ["Claude Code"]
---

![A critical regression in Claude Code](illustration.webp?zoom "Infographic: The anatomy of an AI regression")

Stella Laurenzo's analysis reveals a critical regression in Claude Code for AI-driven complex engineering, correlating the redaction of "thinking" tokens with a collapse in reasoning quality.

Her data from over 234,000 tool calls across nearly 7,000 session files indicates that as the model's internal reasoning depth declined — dropping from ~2,200 characters to just ~600 — it began prioritizing speed over correctness.

---

## Practical implications for software development

- **Research-First → Edit-First:** The read-to-edit ratio dropped from 6.6 to 2.0. The model now frequently edits files it hasn't read, breaking semantic associations and duplicating logic.
- **"Simplest Fix" Mentality:** Without sufficient reasoning budget to evaluate alternatives, the model defaults to superficial workarounds and "ownership-dodging" — seeking permission to stop or disclaiming responsibility.
- **Net Token Waste:** The per-request compute savings are illusory — thrashing from wrong changes and retries increased API request volume ~80x for the same human effort.
- **Autonomy Erosion:** Extended thinking is structurally required for planning-heavy tasks (systems programming, multi-agent coordination). Without it, the model regresses from autonomous partner to supervised tool.

Reasoning depth is a core structural requirement for complex agentic coding, and the thinking token regression eliminates that advantage entirely. With deep reasoning degraded, the 2x+ price premium is no longer justified for many use cases over models that have not exhibited this regression and deliver stronger autonomous performance at a lower cost without requiring constant human supervision to compensate for the observed regressions.

[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7447253977718550528/)

## References

- [Full analysis on GitHub](https://github.com/anthropics/claude-code/issues/42796)
