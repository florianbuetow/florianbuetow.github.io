---
title: "Guard"
subtitle: "Protect your files from unwanted modifications by AI coding agents"
description: "Toggles file immutability and ownership so AI agents cannot silently overwrite your work."
date: 2026-03-06
draft: false
slug: "guard-tool"
tech: ["Go", "CLI", "Unix permissions"]
categories: ["AI Safety"]
tags: ["ai-agents", "guardrails", "safety"]
status: "active"
repo: "https://github.com/florianbuetow/guard"
demo: ""
video: ""
featured: false
---

## The Failure Mode

An AI coding agent, given broad write access to a repository, does not distinguish between files it was asked to change and files it considers adjacent to the problem. That distinction matters to the developer; the agent is reasoning about coherence, not authorization. The result is a refactor that touches configuration files, shared utilities, or build scripts that were never in scope — sometimes silently, sometimes buried in a diff the developer skims too quickly to catch.

Recovering from this is not catastrophic, but it is expensive. `git reflog`, cherry-picking, manual comparison across worktrees — none of it is hard, but it takes time that should have gone into the actual work. More importantly, it erodes trust in the workflow. Developers start hedging: committing more frequently, stashing work before agent runs, reviewing diffs more defensively than productively.

The problem is not that agents are careless. It is that the default filesystem configuration gives them no signal about which files are off-limits. Absent any constraint, gradient descent continues until it hits something that fails — a test, a syntax error, a build break. Files that do not produce immediate failures are fair game.

## Enforcement Below the Agent

The obvious response is to tell the agent what not to touch. Write a careful CLAUDE.md, front-load the system prompt with a list of protected files, repeat the constraint in every session. This works, until it does not. Prompt constraints are persuasion. They operate at the same layer as the agent's reasoning, which means they are subject to the same failures: context window pressure, conflicting instructions, a plausible-sounding rationale the agent constructs mid-task.

The more durable insight is that protection should live below the layer the agent controls. Unix file permissions are not a suggestion the process can override by reconsidering. If a file is not writable by the agent's user, the write fails — not because the agent remembered the constraint, but because the kernel refused the syscall. The enforcement is outside the agent's authority.

This is not a novel idea in systems design. It is the same reasoning behind privilege separation in any multi-process architecture: don't rely on the higher-level component to police itself when a lower-level boundary will do the job reliably.

## How guard Implements This

[guard](https://github.com/florianbuetow/guard) is a Go CLI tool for Linux, macOS, and BSD that makes toggling that enforcement layer fast enough to use routinely. The mechanism is layered: it changes file ownership, removes write permission, and sets the immutable flag. The immutable flag is the load-bearing step — on most Unix systems it means even root cannot modify the file without first clearing the flag, which requires an explicit privileged operation.

To make protection reversible without manual bookkeeping, guard tracks original permissions in a `.guardfile` at the repository root. Restoration reads that state back and undoes each change in order. The workflow is: protect before a risky agent session, restore when the session is done and the results have been reviewed.

The interaction model is an interactive TUI with fuzzy search. The reason for this is friction. A workflow that requires typing file paths or editing configuration by hand gets skipped when a developer is in the middle of something. The fuzzy search interface lets you toggle protection on individual files or named collections in a few keystrokes. The expected use is "ten seconds before starting the agent, ten seconds after reviewing the diff."

There is a genuine limitation that narrows the tool's applicability. Guard depends on the AI agent's user account not having passwordless sudo. If it does, the agent can clear the immutable flag and restore write permissions on its own — the protection collapses. This is not a bug; it is the boundary of what file-permission enforcement can guarantee. Developers running agents under accounts with full passwordless sudo need a different approach, or need to revoke that privilege for the agent account specifically before guard is useful.

## What Was Left Out

Two alternatives come up when thinking about this problem. The first is filesystem event monitoring — tools like fanotify on Linux or fsnotify-based watchers that intercept write calls before they land. This would give finer-grained control and the ability to log or prompt rather than just block. The tradeoff is complexity: a daemon, a kernel interface, platform-specific code paths, and a new abstraction the developer has to understand and trust. Unix permissions are already there, already auditable, and already understood by everyone who has used a terminal for more than a week.

The second is a git-based approach: pre-commit hooks, branch protection, a wrapper that checks file membership before allowing a commit. This shifts the enforcement point later — after the write, at commit time. An agent that touches a protected file can still produce a confusing intermediate state even if the commit eventually fails. Catching the problem at the filesystem layer means the write never happens.

Neither alternative is wrong. Both may be the right answer for different threat models. Guard's position is that for the common case — a developer who wants fast, reversible, no-daemon protection during an agent session — Unix permissions are the correct primitive, and the right design is to make them easy to toggle.
