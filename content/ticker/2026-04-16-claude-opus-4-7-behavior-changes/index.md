---
title: "Claude Opus 4.7: The Behavior Changes We Actually Wanted"
date: 2026-04-16
draft: false
description: "Anthropic's Opus 4.7 ships calibrated response length, stricter instruction following, leaner agentic defaults, and higher-resolution image support - but a new tokenizer raises effective cost on text-heavy workloads."
author: "Florian Buetow"
readTime: "3 min read"
categories: ["AI Engineering"]
tags: ["Claude Code", "Anthropic", "LLM"]
---

Anthropic just released Opus 4.7, and the behaviour changes of the new models are the ones we actually wanted. They address a range of long-standing issues many of us had. A TL;DR:

- **Response length calibrated to task:** Short answers to short questions, long answers where they earn it. No more fixed verbosity baseline.
- **More literal instruction following:** No silent generalization, no inferred asks. Better for structured pipelines and tuned prompts.
- **More direct tone:** Less validation-forward phrasing, fewer emoji. Opinionated where 4.6 was warm and more conversational.
- **Built-in progress updates in agentic traces:** You can delete "summarize every N tool calls" scaffolding since the model does it natively now.
- **Fewer subagents by default:** Steerable via prompt, but the default is leaner.
- **Stricter effort calibration:** low finally means low. Raise effort for complex tasks instead of prompt-hacking around an unpredictable dial.
- **Fewer tool calls, more reasoning:** Thinks before it reaches for grep. Less trash, better results in most cases.
- **Real-time cybersecurity safeguards:** May refuse high-risk topics. Legitimate security work routes through the Cyber Verification Program.
- **High-resolution image support:** Up to 2576px long edge (from 1568). Bounding-box coordinates are now 1:1 with image pixels - no scale conversion required.

The through-line: prompts get simpler, outputs get sharper, and agents get leaner. A lot of the CLAUDE.md directives people have been carrying around since 4.5 as quasi guardrails can probably be retired.

The literalism change also means a prompt that was slightly underspecified on 4.6 may now do exactly - and only - what it says.

## The catch

But there is also a downside of the upgrade: Opus 4.7 ships a new tokenizer that uses roughly 1x–1.35x as many tokens per text as 4.6, depending on the task. Although pricing remains at $5/$25 per MTok, the effective cost per task is expected to rise on text-heavy workloads.

[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7450575161302458368/)

## References

- [Guide for migrating to Claude Opus 4.7 and Claude 4.6 models from previous Claude versions](https://platform.claude.com/docs/en/about-claude/models/migration-guide)
