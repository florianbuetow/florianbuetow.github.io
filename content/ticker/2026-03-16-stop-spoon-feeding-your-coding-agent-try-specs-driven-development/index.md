---
title: "Stop Spoon-Feeding Your Coding Agent - Try Specs-Driven Development"
date: 2026-03-16
draft: false
description: "spec-dd is a specification-driven development workflow for Claude Code that captures behavioral intent before coding, with traceability from acceptance criteria to tests."
author: "Florian Buetow"
readTime: "3 min read"
categories: ["AI Engineering", "Tools", "Ticker News"]
tags: ["Claude Code", "Plugin", "Open Source"]
---

If you are still spoon-feeding your coding agent with instructions and trying to keep it on track with prompting, you need to try specs-driven development.

The issue with prompts is that they hardly capture enough of your intent. Unless you've specified things rigorously, the AI will make assumptions that produce results you did not ask for.

When you have a fully specified feature, the AI aligns much better with your intent and can actually build it to specification without interpretation. That's the idea behind **spec-dd** - a specification-driven development workflow I built for Claude Code.

Instead of jumping straight to implementation, it walks you through:

- writing a behavioral specification
- deriving Given/When/Then test scenarios
- planning test implementation
- handing off to a coding agent

There are three things that make this more than a "write tests before code" type of workflow:

**1. Behavioral specs, not implementation specs.** Phase 1 captures what the system should do - user stories, acceptance criteria, edge cases, and constraints - without any implementation detail. The moment you describe *how* something should work, you anchor the AI to that approach. The workflow reduces ambiguity and closes gaps early by asking clarifying questions. The resulting behavioral specs are also something you can hand to a non-technical stakeholder and get meaningful feedback on.

**2. Traceability across artifacts.** Every acceptance criterion maps to test scenarios. Every test scenario maps to an implementation plan. Every plan maps to actual test code. When the spec changes, you can trace exactly which tests and code are affected.

**3. Advisory quality gates.** Each phase transition has a gate - unresolved clarifications, missing traceability, sequencing issues. Gates are advisory: the skill flags the issue, explains the risk, and lets you proceed. Rigid gates make people game the process. Advisory gates make people think about the trade-off.

Run the entire workflow with `/spec-dd`, or enter any phase directly: `/spec-dd:spec`, `/spec-dd:test`, `/spec-dd:test-impl`, `/spec-dd:review`. The workflow supports iteration - start rough, refine, and go back when the review surfaces gaps.

```
claude plugin marketplace add florianbuetow/claude-code
claude plugin install spec-dd
```

Comment on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7439196260852453376/)

## References

- spec-dd plugin on [GitHub](https://github.com/florianbuetow/claude-code)
