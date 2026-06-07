---
title: "Auto-attach to tmux Sessions Spawned by AI Agents"
slug: "tmux-auto-attach"
date: 2026-05-16
draft: true
description: "A tool that auto-attaches terminals to tmux sessions spawned by AI agents, plus a companion convention for making your own sessions discoverable by a supervising agent."
author: "Florian Buetow"
readTime: "7 min read"
categories: ["AI Engineering", "Tools"]
tags: ["tmux", "AI Agents", "Shell Scripts", "Automation"]
---

Not too long ago I created a Claude Code plugin that lets me delegate tasks to from one AI agent, be it Claude, Codex or Gemini to other one, using tmux sessions. In this short article I'm going to show you how I automatically attach to these tmux sessions to be able to see what the agent actually does. A level of observability that you don't get when you use sub-agents in Claude Code for example.

## Delegating a task to another terminal

Let's start with a simple example. Here, I'm launching a new tmux session to launch A local server for my blog.

<u>Terminal A</u>
```bash
❯ Please launch the dev server in a new tmux session for me
     so that I can see the live log of the server.        

⏺ Bash(tmux new-session -d -s hugo-dev -c ./ 'zsh -i -c "just dev"' …
  ⎿ hugo-dev: 1 windows (attached)
     … +15 lines (ctrl+o to expand)

⏺ Dev server is running in tmux session hugo-dev,
     serving at http://localhost:1313/.
  Attach with: tmux attach -t hugo-dev (detach: Ctrl-b d)
```

<u>Terminal B</u>

Using the name of the session I just spawned can attach to it from another terminal window.

```bash
$ tmux attach -t hugo-dev

=== Hugo Dev Server (foreground, auto-rebuild + LiveReload) ===

Watching for changes in ./…
Watching for config changes in …/hugo.toml, …/go.mod
Start building sites with hugo v0.161.1
Built in 38 ms

Web Server is available at http://localhost:1313/
Press Ctrl+C to stop

Change detected, rebuilding site (#1).
Source changed /blog/2026-05-16-tmux-auto-attach/index.md
Web Server is available at http://localhost:1313/
Total in 45 ms

Change detected, rebuilding site (#2).
Source changed /blog/2026-05-16-tmux-auto-attach/index.md
Web Server is available at http://localhost:1313/
Total in 39 ms```
```

The nice thing about this is that, now, I can remote control terminal B using tmux session spawned by my agent. I can start and stop the service running in B with a simple prompt in A. You can already see how this can be useful for many other scenarios in which you want your agent to be able to monitor and direct what's going on in another terminal.

## Agents controlling agents.

Let's put it to the test and take our previous example a step further. We know that in many AI CLIs we can use sub-agents or teams of agents to launch and orchestrate a number of them so that they collaborate or at the very least complement each other when working on a task.

### Example
```bash
> Fan out 2 subagents, one to determien how much space is left on\
 /Volumes/2TB and one to count the number of folders in\
 /Volumes/2TB/ 

TODO: example of delegating a code review 
```


This time however we're going to use the autoattach script that I promised to show you.

If you follow up the installation instructions, you can launch it from any terminal or path you like.
```bash
$ tmon
```

And you will see something like this where the monitor shows us a list of past TMAX sessions and is waiting for new ones to automatically attach to.

```bash
=== Tmux Session Status ===

┌──────────────────────────┬──────┬───────┬────────┬─────────────────────┐
│ Session Name             │ Path │ Watch │ Attach │ Created             │
├──────────────────────────┼──────┼───────┼────────┼─────────────────────┤
│ codex-review-1779215283  │      │   -   │   -    │ 2026-05-19 20:35:45 │
│ codex-find1779316237     │      │   -   │   -    │ 2026-05-21 00:48:57 │
│ codex-review-1779326160  │      │   -   │   -    │ 2026-05-21 11:36:22 │
│ gemini-check-1779356178  │      │   -   │   -    │ 2026-05-21 11:57:30 │
│ gemini-review-1779215283 │      │   -   │   -    │ 2026-05-19 20:35:45 │
│ guard_tui_test_64427     │      │   -   │   -    │ 2026-05-21 00:31:06 │
└──────────────────────────┴──────┴───────┴────────┴─────────────────────┘

All sessions already attached.

[23:59:53] retrying in 3s - Ctrl-C to stop



```



The effect is agents controlling other agents. Unlike the built-in sub-agent or team-of-agents features that most of these CLIs now ship with, my plugin creates a new tmux session for each delegated task. That session can be observed by the developer - all I have to do is run a CLI command to attach to it.

The manual `tmux attach -t <session>` step at the end is a bit clunky, but it works. I have since found a better way: automatically attach to the sessions Claude Code spawns. I turned this into an open source tool you can grab on GitHub here:

[github.com/florianbuetow/tmux-auto-attach](https://github.com/florianbuetow/tmux-auto-attach)

All you need to do is install it, open one or more terminals, and run the tool in each of them:

```
just init      # once, to verify flock and create ./LOCKS/
just attach    # in each terminal you want to watch with
```

Each terminal now loops, checking for new tmux sessions every few seconds. As soon as a new session is detected, all idle watchers race to attach to it. `flock` guarantees that only one wins. The others move on and keep looking for the next available session. This is what prevents multiple terminals from piling onto the same tmux session.

<video controls width="100%" poster="watcher-terminals.webp">
  <source src="tmux-attach-15x-cut.mp4" type="video/mp4">
</video>

If you just want to use the tool, this is all you need to know. The next section goes deeper into how the watcher works, and after that I'll cover a companion tool that makes it easier for an AI to find tmux sessions you spawned yourself.

## How it works

The `just` interface wraps three shell scripts that you can also invoke directly:

- `auto-attach.sh` - one-shot. Lists tmux sessions sorted by creation time, newest first, and attaches to the first one no other watcher has locked.
- `loop.sh` - the outer loop. Clears the screen and repeatedly re-runs `auto-attach.sh`. All pacing lives inside `auto-attach.sh`; the loop itself does not sleep.
- `cleanup.sh` - removes lockfiles whose tmux session no longer exists.

The corresponding `just` targets are `just attach` (runs the loop), `just status` (shows which sessions are currently under watch), and `just cleanup` (removes orphaned locks).

The locking works as follows. For each candidate session name, the watcher opens a file at `./LOCKS/<sanitized-name>` and attempts a non-blocking `flock -n` on it. If it acquires the lock, it attaches. If it does not, it moves on. The lock is held only while the terminal is attached, so when a session is detached or killed, the slot frees up for the next watcher.

The session name is sanitized via `tr -c 'a-zA-Z0-9._-' '_'` before being used as a lockfile name. This is lossy: two session names that differ only in characters outside `[A-Za-z0-9._-]` collapse to the same lock key. For example, `my session` and `my_session` share a single lock and cannot be watched in parallel. If you need parallel watch on similar names, make them differ in characters from the allowed class.

To avoid two watchers grabbing the same session in a tight race, `auto-attach.sh` sleeps a random 0–199 ms after detaching, and 3 seconds when no free session was available. `cleanup.sh` has two safety layers before deleting anything: the lockfile's key must not match an active tmux session, and `flock -n` must succeed against the file. If `tmux list-sessions` fails for any reason other than "no server running", cleanup exits non-zero without deleting - this prevents a transient tmux error from being interpreted as "every lock is orphaned."

`just status` reflects the live lock state. The ✅ column is a real-time `flock -n` probe against each lockfile, not a cached value. Greyed rows are stale lockfiles whose tmux session no longer exists.

Requirements: `tmux`, `flock` (on macOS: `brew install flock`), and `just` if you want the `just` interface (on macOS: `brew install just`).

## Wrap

The watcher solves one half of the problem: I want to see what an AI-spawned session is doing. The other half is the reverse: I want an AI to see and act on a session *I* spawned.

The scenario where this matters most for me is the long-running session. Say I'm kicking off something that will run overnight - a multi-step refactor, a long evaluation, a build I expect to get stuck on permission prompts. I don't want to sit at the computer all night unblocking it. I also don't want to launch it with `--dangerously-skip-permissions`, because the whole point of permission prompts is that some of them deserve a "no". What I want is an intelligent feedback mechanism: another AI watching the session and unblocking it for a narrow, pre-agreed set of operations.

For that to work, the supervising AI has to find my session. That's what `wrap` is for. It is a zsh function that creates tmux sessions whose names always start with `WRAP-`. Any agent can then enumerate them with:

```
tmux ls | grep '^WRAP-'
```

The convention is the API. Once the session is discoverable by name, the supervising agent can `tmux capture-pane` to read its output, `tmux send-keys` to respond to prompts, and so on.

Concretely, the workflow looks like this. In one terminal:

```
wrap new       # creates a WRAP- session for the current directory
# inside that session, launch the long-running AI task
```

In another terminal, launch a second CLI AI and prompt it along the lines of: *monitor the tmux session matching `WRAP-*-<dir>`. If it prompts for permission to create or run a new shell, approve it. For any other permission prompt, do nothing and wait for me.* The supervising agent now handles the narrow class of interruptions you've explicitly approved, and escalates everything else by leaving it for you in the morning.

The other `wrap` subcommands handle the lifecycle of these sessions:

- `wrap` - list all wrap sessions, show usage.
- `wrap new` - create a new wrap session for `$PWD`. Refuses to run from inside an existing tmux session.
- `wrap -r` - reattach to a wrap session for `$PWD`. If exactly one matches the current directory, attaches directly; otherwise prompts.
- `wrap -d` - kill a wrap session for `$PWD`.

Session names follow `WRAP-[N]-<dir>`, where `<dir>` is `$PWD` with `$HOME` rewritten to `~` and `.` replaced by `_`. `N` auto-increments globally across all wrap sessions, so names are stable and unique.

`wrap` is a sourced zsh library, not a runnable script. To install, add one line to your `~/.zshrc`:

```
[ -f "$HOME/path/to/tmux-auto-attach/wrapfunc.sh" ] && \
    source "$HOME/path/to/tmux-auto-attach/wrapfunc.sh"
```

It uses zsh-specific syntax (associative arrays, regex captures, prompted `read`) and will not run in bash without modification.

## Conclusion

The watcher and `wrap` are two halves of the same idea: make tmux sessions discoverable and observable so that humans and AIs can share them as a substrate. The watcher gives me a live window into every session an agent spawns. `wrap` gives an agent a stable way to find sessions I spawned, so it can supervise them on my behalf.

**Takeaways**

- The watcher auto-attaches terminals to new tmux sessions, newest first, with `flock`-based mutual exclusion so no two watchers grab the same session.
- The three scripts (`auto-attach.sh`, `loop.sh`, `cleanup.sh`) and the `just` interface (`init`, `attach`, `status`, `cleanup`) are small enough to read end-to-end.
- `wrap` creates sessions named `WRAP-[N]-<dir>` so agents can discover them with `tmux ls | grep '^WRAP-'` and supervise long-running work.
- Tested on macOS with zsh. `wrap` requires zsh; the watcher is plain shell.

[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:PLACEHOLDER/)

## References

- [tmux-auto-attach on GitHub](https://github.com/florianbuetow/tmux-auto-attach) - the repo with the watcher and `wrap`.
- [tmux](https://github.com/tmux/tmux) - the terminal multiplexer everything here is built on.
- [flock](https://linux.die.net/man/1/flock) - the file locking utility used for mutual exclusion. On macOS: `brew install flock`.
- [just](https://github.com/casey/just) - the command runner used for the `just init`, `just attach`, etc. interface.
