---
title: "Terminator Plugin for Claude Code: A Killswitch to automatically close your sessions"
slug: "terminator-plugin-for-claude-code"
date: 2026-06-11
draft: false
description: "A Claude Code plugin that installs Stop hooks to end a session - and optionally its terminal - when the agent's final message contains a kill phrase you choose."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools", "Ticker News"]
tags: ["Claude Code", "Plugin", "Open Source"]
---

{{< sidenote label="Download" >}}[github.com/florianbuetow/claude-code](https://github.com/florianbuetow/claude-code){{< /sidenote >}}

Sometimes I just want to fire a prompt and forget: send Claude Code a prompt from CLI (or inside a session) and have the session close itself when the job is done. This is exactly what the Terminator plugin enables you to do. All you need to do is define a catchphrase and tell the model to utter that exact catchphrase at the end of its task. A hook ensures that when Claude stops and the catchphrase is present in the last message, it will terminate your Claude session and, if configured, the shell that you launched Claude Code from as well.

It works through a Claude Code Stop hook. After each turn, the hook reads the agent's final message, and if your configured catchphrase appears anywhere in it, the session is terminated. The match is an exact substring match, so it still fires even when the model wraps your phrase in its usual preamble. I recommend choosing something rare, like a movie quote or a sentence the model would never write accidentally, so a session never ends unintentionally in the wrong moment; the install skill will guide you to pick a good catchphrase.

You choose what gets terminated by installing one or both of two scripts:

- **single-kill** - terminates Claude and leaves the terminal open.
- **double-kill** - terminates Claude, then the terminal shell that launched it.

Three skills to configure it:

- `/terminator:install` - set up single-kill and/or double-kill, each bound to its own phrase.
- `/terminator:update` - change a phrase or toggle case sensitivity, live, with no restart.
- `/terminator:remove` - uninstall cleanly, leaving any other Stop hooks intact.
- `/terminator:info` - show configuration and catchphrase.

```
claude plugin marketplace add florianbuetow/claude-code
claude plugin install terminator
/reload-plugins
```

## References

- [Terminator plugin on GitHub](https://github.com/florianbuetow/claude-code/tree/main/plugins/terminator)
- [My (free) plugin marketplace](https://github.com/florianbuetow/claude-code)
