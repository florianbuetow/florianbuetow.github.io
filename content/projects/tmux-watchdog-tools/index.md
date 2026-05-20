---
title: "Tmux Auto Attach"
subtitle: "Auto-attach terminals to tmux sessions spawned by AI coding agents"
description: "Bash scripts and a zsh helper that auto-attach idle terminals to new tmux sessions, with flock-based mutual exclusion so each session has exactly one watcher."
date: 2026-05-16
draft: false
slug: "tmux-auto-attach"
tech: ["Bash", "zsh", "Just", "tmux", "flock"]
categories: ["Developer Tooling"]
tags: ["tmux", "ai-agents", "automation", "shell-scripts"]
status: "active"
repo: "https://github.com/florianbuetow/tmux-auto-attach"
demo: ""
video: ""
featured: false
image: "/projects/tmux-auto-attach/watcher-terminals.webp"
---

Tmux Auto Attach is a helper script that automatically attaches idle terminals to new tmux sessions spawned by your AI coding agent. The reason to spawn sub-agents, or agents from different vendors, in tmux sessions is observability and interoperability: you get a live window into what each sub-agent is doing, and sub-agents can be from any vendor (Anthropic, Google, OpenAI, …).

For a full walkthrough of how to use it, please read the blog post titled: [Auto-attach to tmux Sessions Spawned by AI Agents](/blog/tmux-auto-attach/).

{{< sidenote label="SCREENSHOT" >}}4 auto-attach runners waiting for new tmux sessions.{{< /sidenote >}}

![Watcher terminals auto-attaching to tmux sessions](watcher-terminals.webp?zoom)

## Quick Install

{{< sidenote label="SETUP" >}}The full installation guide is available on [GitHub](https://github.com/florianbuetow/tmux-auto-attach#install).{{< /sidenote >}}


```sh
mkdir -p ~/scripts
cd ~/scripts
git clone https://github.com/florianbuetow/tmux-auto-attach.git
cd tmux-auto-attach
just init
```

Add these aliases to your `~/.zshrc` (or `~/.bashrc`) as shortcuts:

```sh
alias tmon='(cd ~/scripts/tmux-auto-attach && just attach)'
alias tstat='(cd ~/scripts/tmux-auto-attach && just status)'
```

After reloading your shell with 
```sh 
source ~/.zshrc
```

You are all set. Simply run

```sh
tmon
```

In any terminal, to start watching for new sessions.

## References

- **GitHub** - [tmux-auto-attach](https://github.com/florianbuetow/tmux-auto-attach)
- **Article** - [Auto-attach to tmux Sessions Spawned by AI Agents](/blog/tmux-auto-attach/) 
- **tmux** - [the terminal multiplexer](https://github.com/tmux/tmux)
- **flock** - [the file locking utility used for mutual exclusion](https://linux.die.net/man/1/flock)
- **just** - [justfile command runner](https://github.com/casey/just)

