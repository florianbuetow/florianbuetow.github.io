---
title: "AI Guardrails"
subtitle: "Project templates for C++, Elixir, Go, Java, Python, and Rust with a rich set of automatic guardrails for AI coding agents"
description: "Copier templates for six languages that enforce strict validation so AI-generated code fails fast on antipatterns."
date: 2026-04-04
draft: false
slug: "ai-guardrails"
tech: ["Copier", "Python", "Java", "Go", "Elixir", "C++", "Rust"]
categories: ["AI Safety"]
tags: ["ai-agents", "guardrails", "templates", "safety"]
status: "active"
repo: "https://github.com/florianbuetow/ai-guardrails"
demo: ""
video: ""
featured: false
---

## The Problem Is Structural

AI coding agents produce code that compiles, passes type checks, and makes tests green. That sounds like success. Often it is. But there is a class of failure that looks like success until a later layer of the system collapses under it: the agent reached a problem it could not solve cleanly, so it used one of its learned exits.

`# type: ignore`. `catch (Exception e) { return null; }`. A parameter with a default value of `""` that silently short-circuits a validation branch. These patterns are not bugs in the conventional sense — they do not crash. They suppress the signal that a crash would have sent. The type checker is quiet. The test passes. The invariant is gone.

Left to accumulate, this is not a single bad function. It is a codebase that has quietly agreed to carry the complexity it should have surfaced. The exits compound. The feedback loop that would have taught the model to do better never fires.

## The Feedback Loop That Actually Works

An AI agent, in the context of a software project, is operating in a loop: generate, observe, iterate. The question is what it observes. Prompts are read once and drift. Documentation — including `AGENTS.md` — is consulted selectively. Human code review is slow and inconsistent.

The CI pipeline is what the agent actually listens to. It runs on every commit, produces structured output, and exits with a code that is either zero or not. Shape the pipeline to fail loudly on the specific antipatterns the model reaches for, and the agent's next iteration incorporates that signal. The model did not solve the real problem; the pipeline said so; the model tries again without the suppression.

This requires three properties in the pipeline. It has to be fast, because a five-minute wait between attempt and feedback teaches the model to tolerate ambiguity. It has to fail fast — exit on the first failure, not collect all warnings and summarize at the end. And the failures have to be unignorable: no warnings treated as informational, no lint output the agent can amble past. Errors only, blocking the build.

## What the Templates Do

[ai-guardrails](https://github.com/florianbuetow/ai-guardrails) is a set of Copier templates — one for each of six language ecosystems: Python, Java, Go, Elixir, C++, and Rust. Each template is installable in a single command and provisions a project with the full pipeline rather than a 40-page setup guide that gets skipped.

The core of each template is the same regardless of language. A multi-step CI pipeline exits on first failure. Pre-commit hooks run the full CI locally so the agent's own loop already includes the feedback before anything reaches a remote. A `justfile` gives the agent (and the human) a consistent interface for `init`, `test`, `ci`, and `destroy` without having to remember per-project incantations.

The `AGENTS.md` file documents project conventions in the format AI assistants are built to read at session start. It complements the pipeline rather than replacing it. The pipeline is authoritative; `AGENTS.md` is context that helps the agent understand why the rules exist.

The Semgrep rules are where the per-agent specificity lives. Generic linters catch generic problems. These rules were written to match the specific patterns that appear in agent-generated code when the agent is stuck: default mutable parameters, blanket type suppressions, exception handlers that swallow errors and return a plausible-looking fallback. The goal is not to catch every possible defect — it is to close the specific exits the model has learned to use.

## Per Language, Not Per Principle

The same philosophy applies across all six ecosystems, but the antipatterns are not the same. Python's `# type: ignore` and Java's `catch (Exception e) { return null; }` are structurally equivalent — both suppress a signal — but they require different rules to detect. Go's error handling patterns differ from Rust's. The tooling for each language is chosen for its ecosystem: where one language has an established linter with strong static analysis, that linter runs in the pipeline; where a language has an auditing tool for known vulnerabilities, it runs too. The per-language choices are documented in the repository.

What does not change across languages: fail fast, errors not warnings, full CI on pre-commit, Semgrep targeting agent-specific antipatterns.

## What This Is Not

These templates do not make AI-generated code safe in any absolute sense. They do not eliminate the need for review. They do not check for correctness at the level of business logic. Tests still need to be written and maintained. A model that is determined to produce low-quality output will find exits that no static ruleset anticipated.

What the templates do is close the specific exits that appear most frequently in agent-produced code, and ensure the feedback loop is tight enough that the agent iterates on real signal rather than accumulating suppressed failures. The human reviewer inherits code that has passed a strict automated bar — not perfect, but not quietly broken either.
