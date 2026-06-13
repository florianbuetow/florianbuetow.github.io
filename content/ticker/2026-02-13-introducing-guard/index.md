---
title: "Introducing Guard - Protect Files from AI Coding Agents"
date: 2026-02-13
draft: false
description: "Guard is a CLI/TUI tool that uses Unix file permissions and immutable flags to physically protect files from AI coding agents."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools", "Guardrails", "Ticker News"]
tags: ["Open Source"]
---

![Introducing Guard](illustration.webp?zoom "Logo: Yes, You Are Absolutely Right!")

2001: A Space Odyssey predicted "I'm sorry, I can't do that, Dave". Instead, we got "Yes, you are absolutely right!" - which is equally frightening if you're a software developer.

I'm frankly tired of AI assistants "helpfully" rewriting files I wasn't even working on. You tell it to fix a bug in one file, and suddenly three other files are modified. You point it out and get "Yes, you are absolutely right, I shouldn't have changed those files. Let me fix that." And then it breaks something else. We've all been there - it's the reason why we don't trust AI to run unsupervised on critical code that must not change.

The solution I found for myself is now a mini open-source tool that everyone can use.

---

## What Guard does

Guard is a CLI/TUI tool that protects your files from AI coding agents. It uses Unix file permissions and immutable flags to make files physically read-only on disk. The agent literally cannot modify guarded files. Guard never touches file contents - it only changes permissions and remembers the originals so it can restore everything when you're done.

- Guard and unguard individual files or entire collections with one command
- Interactive terminal UI for power users who need speed
- Works with any AI agent - Claude, Cursor, Copilot, or anything
- Toggle protection on and off as your task evolves
- Creates a `.guardfile` in your project root

**Requirements:** Go, a UNIX filesystem with immutable flag support (Linux/Mac: ext*, Btrfs, XFS, HFS+, APFS), run with `sudo guard`, AI without sudo access.

Comment on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7428093313297113088/)

## References

- Guard on [GitHub](https://github.com/florianbuetow/guard)
