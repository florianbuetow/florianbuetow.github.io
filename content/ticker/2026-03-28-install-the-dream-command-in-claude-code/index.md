---
title: "Claude Code: Install the /dream Command"
slug: "install-the-dream-command-in-claude-code"
date: 2026-03-28
draft: false
description: "How to install Anthropic's /dream memory consolidation command in Claude Code before it rolls out natively to all users."
author: "Florian Buetow"
readTime: "1 min read"
categories: ["AI Engineering", "Ticker News"]
tags: ["Claude Code"]
---

Anthropic silently added a new `/dream` feature for memory consolidation in Claude Code. Unfortunately, it is not yet available to everyone.

If you do not have native access yet, you can use the public Dream prompt today by installing it as a global slash command. Ask Claude Code in CLI to do it for you with this prompt:

> Fetch the Dream prompt from `https://raw.githubusercontent.com/Piebald-AI/claude-code-system-prompts/main/system-prompts/agent-prompt-dream-memory-consolidation.md`, create the global Claude commands directory at `~/.claude/commands` if it does not already exist, and save the file as `~/.claude/commands/dream.md`. Then tell me to restart Claude Code so the new `/dream` command is loaded and becomes available system-wide.

After that, simply type `/dream` to consolidate your project's memory.

Comment on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7443552472767434752/)

## References

- [Dream memory consolidation prompt on GitHub](https://github.com/Piebald-AI/claude-code-system-prompts)
