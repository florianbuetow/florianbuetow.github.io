---
title: "The Planner, The Executor, and The Reviewer: How I Use Three AI Agents as a Development Team"
slug: "three-ai-agents-dev-team"
date: 2026-05-31T10:00:00+02:00
draft: true
description: "A practitioner's guide to a three-agent development workflow: plan with Claude Opus, delegate implementation to a coding agent (OpenAI Codex), and run an adversarial review with a third agent."
author: "Florian Buetow"
categories: ["AI Engineering"]
tags: ["AI Agents", "claude", "codex", "tmux", "software-development", "workflow"]
---

<!-- ============================================================
     STRUCTURE: method-first. The delegation METHOD is the spine;
     the feature is only an illustrative example and is swappable.
     13 sections, dictated:
       1. Title & Intro
       2. Why Three Agents
       3. The Method: Plan, Delegate, Verify
       4. Step 1: Plan with Opus
       5. Step 2: Write an Implementation Plan and a Test Plan
       6. Step 3: Delegate the Implementation to a Coding Agent (Codex)
       7. Step 4: Delegate an Adversarial Review to the Review Agent
       8. Step 5: Review the Review
       9. Step 6: Iterate
      10. Passing Context
      11. How to Get Started
      12. Summary
      13. Resources

     PRESERVED-CONTENT LEGEND used below:
       [REUSED] = lifted verbatim (or near) from the prior draft, still valid.
       [REUSED - NEEDS EDIT] = kept as a base but must be updated (e.g. 2-agent → 3-agent).
       [EXAMPLE - SWAPPABLE] = feature-specific illustration; replace when the real
                               implemented feature's artifacts exist.
       [TODO] = new content to write.
     Dropped "Practical Tips" is preserved as a commented block at the very bottom.
     ============================================================ -->

# The Planner, The Executor, and The Reviewer: How I Use Three AI Agents as a Development Team

<!-- [REUSED - NEEDS EDIT] Title was "The Planner and The Executor ... Two-Agent".
     Updated to three agents (planner / coding agent / review agent). Author to approve wording. -->

<!-- MEDIA: hero-image.png
     Static image or short looping animation.
     Concept: three roles - a planner (conversation/sketches), an executor (terminal
     streaming code), and a reviewer (red-pen/critique overlay).
     Caption: "One plans. One executes. One reviews. Together they ship." -->
<!-- [REUSED - NEEDS EDIT] hero concept was split-screen for two agents; now three. -->
![Hero image: planner / executor / reviewer](media/hero-image.png)

---

<!-- [REUSED] intro paragraph - still valid. -->
I've been building [Guard](https://github.com/florianbuetow/guard), a Go CLI/TUI tool that protects files from unwanted modifications by AI coding agents. Ironic, right? An AI-protection tool built *with* AI agents. Along the way, I discovered that the best workflow isn't choosing one model over another - it's using them as a team.

<!-- [REUSED - NEEDS EDIT] add the third role (review agent) to this framing. -->
**Claude Opus 4.6** (high effort) is my planner, architect, and conversation partner. **OpenAI Codex** - running **GPT-5.3-Codex** at high reasoning effort - is my tireless executor: hand it a precise plan and it implements, tests, and commits with near-perfect fidelity. And a third agent - a **review agent** running an *adversarial review* - checks the executor's work before I trust it.

<!-- [REUSED] -->
This isn't a benchmarks post. This is a practitioner's guide to building a real multi-agent workflow, illustrated with a real feature.

---

## Why Three Agents

<!-- [REUSED] core thesis line. -->
Here's the uncomfortable truth: no single AI model is the best at everything.

<!-- [REUSED - NEEDS EDIT] capability table. Currently two columns (planner vs executor).
     ADD a third column for the Review Agent (adversarial review). Fill its cells. -->
| Capability | Claude Opus 4.6 (high) - Planner | GPT-5.3-Codex (high) - Coding Agent | Review Agent (adversarial) |
|---|---|---|---|
| Conversational design | Excellent | Weak | <!-- TODO --> |
| Asking clarifying questions | Natural, contextual | Doesn't ask - halts or guesses | <!-- TODO --> |
| Long focused execution runs | Good but benefits from check-ins | Exceptional - sustained focus across a full session | <!-- TODO --> |
| Following detailed specs | Good | Near-perfect | <!-- TODO --> |
| Making design decisions | Strong opinions, good taste | Will implement whatever you say | <!-- TODO --> |
| Error rate on complex multi-file changes | Occasional drift | Very low with clear spec | <!-- TODO --> |
| Planning and decomposition | Excellent | Not its job | <!-- TODO --> |
| Catching the executor's mistakes | (is the planner) | Won't critique its own work | <!-- TODO: this is the review agent's whole job --> |

<!-- [REUSED] the archetype framing - strong, keep. Extend with the reviewer archetype. -->
Think of it this way: **Opus is the senior engineer you pair-program with. Codex is the focused specialist who takes a detailed plan to a private room and emerges with a working implementation. The review agent is the skeptical reviewer who tries to break it before you do.**

<!-- [REUSED - folded in from old "Why Not Just Use One Model?" + "The Analogy"]
     These two old sections said the same thing three times between them and the table above.
     Consolidate the non-redundant parts of them HERE, said once. -->
<!-- [TODO] One tight paragraph on the single-model failure modes, drawn from the old
     "Why Not Just Use One Model?" section:
       - Opus-only for implementation → drifts / loses context on large multi-file work.
       - Codex-only for everything → doesn't ask, doesn't push back, implements wrong ideas.
       - Neither critiques its own output → you need an independent reviewer.
     Old source text preserved in the commented block at the bottom of this file. -->

<!-- MEDIA: workflow-overview.gif
     Short looping animation. Three boxes now: Plan (Opus) → Delegate (Codex) → Review (review agent),
     with a feedback arrow looping back to Plan. Spec/plan flows left-to-right; a checkmark at the end. -->
<!-- [REUSED - NEEDS EDIT] was two boxes; now three + feedback loop. -->
![Animated diagram: plan → delegate → review, with feedback loop](media/workflow-overview.gif)

---

## The Method: Plan, Delegate, Verify

<!-- [REUSED] lead-in. -->
Here's the workflow I've converged on after months of iteration:

<!-- [REUSED - NEEDS EDIT] the big ASCII diagram. Currently PLANNING (Opus) / EXECUTION (Codex).
     Update to three stages: PLAN (Opus) → DELEGATE (coding agent) → VERIFY (review agent),
     with an ITERATE feedback arrow back to PLAN. Keep the box style. -->
```
┌-------------------------------------------------------------┐
│                    PLANNING PHASE (Opus)                     │
│                                                             │
│  Developer ←--conversation--→ Claude Opus 4.6               │
│                                                             │
│  1. Brainstorm the feature (back-and-forth Q&A)             │
│  2. Explore approaches (Opus proposes 2-3 options)          │
│  3. Design the architecture (section-by-section approval)   │
│  4. Write the IMPLEMENTATION plan                           │
│  5. Write the TEST plan (how we'll prove it works)          │  <!-- [TODO] added: test plan -->
│  6. Decompose into phased steps                             │
│                                                             │
│  Output: implementation plan + test plan                    │
│                                                             │
├-------------------------------------------------------------┤
│                EXECUTION PHASE (coding agent)               │
│                                                             │
│  Claude Opus --delegates--→ OpenAI Codex (via tmux)        │
│                                                             │
│  1. Codex reads the plan (its single source of truth)       │
│  2. Executes step-by-step: tests, implements, commits       │
│  3. Codex runs the test plan against its own work           │  <!-- [TODO] confirm: who runs tests -->
│                                                             │
│  Output: working, tested, committed code                    │
│                                                             │
├-------------------------------------------------------------┤
│              VERIFICATION PHASE (review agent)              │  <!-- [TODO] new third stage -->
│                                                             │
│  Claude Opus --delegates--→ Review Agent (adversarial)     │
│                                                             │
│  1. Adversarial review of the implementation                │
│  2. Opus reviews the review                                  │
│  3. Iterate: loop back to PLAN for fixes if needed          │
│                                                             │
│  Output: verified code, or a fix plan                       │
│                                                             │
└-------------------------------------------------------------┘
```

<!-- [REUSED - NEEDS EDIT] handoff-artifact bullets. Was "the agent execution spec".
     Now there are TWO artifacts: the implementation plan AND the test plan. -->
The key is the **handoff artifacts** - the implementation plan and the test plan. These documents are the bridge between Opus's planning ability and the coding agent's execution ability. They must be:

- **Zero-ambiguity**: every file path, every struct field, every test assertion spelled out
- **Self-contained**: the coding agent shouldn't need to ask questions
- **Phased**: broken into commits so each step can be reviewed incrementally
- **TDD-enforced**: tests before implementation in every step
- **Verifiable**: the test plan defines, up front, what "done and correct" means <!-- [TODO] expand in Step 2 -->

---

## Step 1: Plan with Opus

<!-- [REUSED] -->
I started by telling Opus what I wanted. Notice how the conversation is *collaborative* - Opus asks smart questions one at a time, I refine:

<!-- [EXAMPLE - SWAPPABLE] the whole fuzzy-search dialogue below is illustrative.
     Replace with the real feature's planning conversation when we implement for real. -->
**Me:** "I want to add a new epic fuzzy-search-improvements"

**Opus** explored the codebase (23 existing search test files, the fuzzy matching library, the search box component, the app wiring) and then asked:

> "What's the main pain point with the current fuzzy search?"

I explained the `//` concept: pressing `/` opens local search, pressing `/` again as the first character upgrades to global project-wide search.

Then Opus asked the right follow-up questions - one at a time, not a wall of questions:

1. **"When the user selects a result, what should happen?"** - I said fzf-style flat paths, files only.
2. **"What happens when the user presses Enter on a result?"** - Same keybindings as always, stay in results.
3. **"Eager or lazy scan?"** - Lazy (on first `//`).
4. **"Sequential upgrade or quick double-tap?"** - Sequential, first char must be `/`.
5. **"Visual indicator for global mode?"** - Prompt changes to ` Search:: ` with different color.

<!-- MEDIA: conversation-flow.mp4 (or GIF, 15-20 seconds)
     Screen recording of the actual Claude Code session.
     user types the request → Opus explores codebase → asks first question → user answers → next question.
     Speed up 3-4x. Crop to terminal. Dark theme.
     Caption: "Opus asks one question at a time, each building on the last." -->
<!-- [REUSED] media note. -->
![Video: Opus conversation flow - one question at a time](media/conversation-flow.mp4)

<!-- [REUSED] -->
This is where Opus excels. It understood my codebase, asked questions that surfaced design decisions I hadn't considered (like the async streaming requirement), and built up the design incrementally. **A coding agent could never do this part.** It would either halt waiting for instructions or implement whatever you told it without questioning whether it's the right approach.

<!-- [TODO] CRITICAL ADDITION (author's instruction): planning produces TWO things, not one.
     Alongside the implementation design, Opus also plans the VERIFICATION up front:
     "How are we going to prove this actually works in the end?" Decide acceptance
     criteria and the shape of the test plan during planning, before any code. This
     paragraph sets up Step 2's split into implementation plan + test plan. -->

---

## Step 2: Write an Implementation Plan and a Test Plan

<!-- [TODO] frame: planning yields two artifacts. The implementation plan (what to build,
     step by step, with exact code) AND the test plan (how we verify it - acceptance
     criteria, the tests that must exist and pass). Both are handoff artifacts. -->

### The implementation plan

<!-- [REUSED] design-doc bullets (was "Phase 2: The Design Doc"). -->
After the conversation, Opus produced a clean design document covering:

- Activation flow (the `//` sequential upgrade mechanism)
- Async directory scanner (goroutine + channel + batched results)
- Cache lifecycle (lazy scan, cache on complete, invalidate on refresh)
- Display (fzf-style flat list with guard indicators)
- Edge cases (gitignored files, guard-tracked overrides, symlink cycles)

<!-- [EXAMPLE - SWAPPABLE] "about 120 lines" is a feature-specific number; re-measure for real feature. -->
The document was about 120 lines of focused specification. No fluff.

<!-- [REUSED] the "bridge document" framing + spec excerpt. -->
Then Opus produced the implementation plan - a document designed specifically for the coding agent to consume. This is what the first lines look like:

<!-- [EXAMPLE - SWAPPABLE] this markdown excerpt is from the (not-yet-built) fuzzy feature.
     Replace with the real plan when implemented. NOTE: file is now called an
     "implementation plan", not an "agent execution spec". -->
```markdown
# Global Fuzzy Search - Implementation Plan

> **This is the single source of truth.** Follow it to the letter.
> Do not improvise. Do not deviate.

## Before You Start

Read these files FIRST, in this order, before writing any code:

1. `AGENTS.md` - project conventions, architecture rules, testing rules
2. `docs/plans/2026-02-18-global-fuzzy-search-design.md` - feature design
3. `internal/tui/search_box.go` - current search box implementation
4. `internal/tui/file_tree.go` - current file tree filtering
5. `internal/tui/fuzzy.go` - existing fuzzy match function
...18 files total...

## Rules

- Do NOT modify any existing test files in `tests/`.
- Architecture rules are enforced by `internal/architecture/layers_test.go`
- Run `go fmt ./...` after every code change.
- Commit after each step as specified.
```

<!-- [REUSED] tone observation - still valid. -->
Notice the tone. It's not conversational - it's **commanding**. "Follow it to the letter. Do not improvise." This is exactly what a coding agent needs. Where Opus would find this insulting, the coding agent finds it clarifying.

<!-- [REUSED] the "each step contains" bullets (was "6 phases each with"). -->
The plan then breaks down into ordered steps, each with:
- Exact files to create/modify
- Complete code snippets (not pseudocode - actual Go)
- Test functions with exact assertion descriptions
- Verification commands with expected output
- Commit messages

<!-- [REUSED] "a taste of specificity" + the Phase 2C code snippet. -->
Here's a taste of the specificity:

<!-- [EXAMPLE - SWAPPABLE] code snippet from the unbuilt feature. -->
```markdown
### Step: Implement global mode in SearchBox

Edit file: `internal/tui/search_box.go`

Changes:
1. Add field `globalSearch bool` to `SearchBox` struct.
2. Add method `IsGlobalSearch() bool`.
3. In `Update()`, add a case BEFORE the default key handler:
   ```go
   if !s.globalSearch && s.textInput.Value() == "" {
       if msg.Type == tea.KeyRunes && string(msg.Runes) == "/" {
           s.globalSearch = true
           s.textInput.Prompt = " Search:: "
           return s, func() tea.Msg { return GlobalSearchActivatedMsg{} }
       }
   }
   ```
```

<!-- [REUSED] -->
**This level of detail is what makes the coding agent fly.** It doesn't need to think about architecture or make design choices - those were already made by Opus. It just needs to type.

### The test plan

<!-- [TODO] NEW SECTION (author's instruction). The companion artifact.
     What it contains:
       - Acceptance criteria: observable behaviour that proves the feature works.
       - The exact tests that must exist and pass (unit + TUI acceptance).
       - How each test maps back to a requirement from Step 1.
     Why it's separate from the implementation plan: it's the independent definition of
     "correct", written during planning so success isn't graded by whoever wrote the code.
     This is what the review agent (Step 4) and the iterate loop (Step 6) check against. -->
_[TODO: show an example test-plan excerpt once the real feature is built.]_

---

## Step 3: Delegate the Implementation to a Coding Agent (Codex)

<!-- [REUSED] DELEGATE.md philosophy quote. -->
I use a delegation skill that teaches Opus *how* to talk to the coding agent via tmux. Here's the key philosophy:

> Treat the agent like it is extremely literal-minded: it follows instructions with exact precision, no more, no less. It will work tirelessly on a task without complaint. Ambiguity is the enemy: every detail you leave unspecified is a potential point where the agent will halt or guess wrong.

### How the tmux bridge actually works

<!-- [REUSED] the real tmux command block - verified against the delegate:codex skill. KEEP. -->
The bridge is plain `tmux` - no special integration, no API glue. Codex runs as an interactive CLI inside a dedicated tmux session, and Opus drives it with ordinary tmux commands:

```bash
# 1. Start Codex in its own detached tmux session
tmux new-session -d -s 'codex' -c "$HOME/Developer/github/guard.git/dev"
tmux send-keys -t 'codex:0.0' 'codex' Enter

# 2. Hand off a step. DON'T paste multi-line text with send-keys -
#    it garbles indentation and newlines. Write the instructions to a
#    buffer (or a file), then paste it, then press Enter SEPARATELY.
cat << 'EOF' | tmux load-buffer -
Read docs/plans/2026-02-18-global-fuzzy-search-plan.md. Execute Step 1.
EOF
tmux paste-buffer -t 'codex:0.0'
tmux send-keys -t 'codex:0.0' Enter      # <-- the Enter is its own call

# 3. Watch it work
tmux capture-pane -t 'codex:0.0' -p | tail -40
```

<!-- [REUSED] the two hard-won lessons. KEEP. -->
Two lessons, both learned the hard way. First: the single most common mistake is pasting a prompt and forgetting the separate `Enter` - without it, Codex just sits there with a full input buffer and nothing happens. Second: never feed raw multi-line text through `send-keys`; it mangles the input. Load it into a buffer (or write a file) and paste instead.

<!-- TODO: Add a screenshot of the split tmux layout - Opus (Claude Code) on the left pane,
     Codex running in the 'codex' session on the right - mid-delegation. media/tmux-bridge-split.png -->
![TODO screenshot: split tmux - Opus left, Codex right](media/tmux-bridge-split.png)

<!-- TODO: Recreate a short, representative transcript excerpt of one delegation round
     (Opus runs capture-pane → sees Codex editing files → Codex commits). Capture from the
     real delegation run when we implement. media/tmux-capture-pane.gif -->

<!-- [REUSED - NEEDS EDIT] startup script. Drop/adjust beads lines per Passing Context decision. -->
The startup script I use launches Claude Code with a pre-written prompt:

```bash
#!/usr/bin/env bash
claude "$(cat <<'PROMPT'
You are implementing the Global Fuzzy Search (// Mode) feature for Guard.

## Step 1: Read these files in order
1. AGENTS.md - project conventions, architecture, testing rules
2. DELEGATE.md - how to delegate work to the coding agent via tmux
3. docs/plans/2026-02-18-global-fuzzy-search-plan.md - the implementation plan
4. docs/plans/2026-02-18-global-fuzzy-search-design.md - feature design

## Step 2: Start delegating to the coding agent
Your role:
- YOU are the planner and reviewer
- The coding agent is the executor
- Send Step 1 first, wait for completion, review the output
- Run `just ci-quiet` after each step to verify
- Move to the next step only after the current one passes CI
PROMPT
)"
```

<!-- [REUSED] same-session vs fresh-session nuance - belongs partly here and partly in Passing Context. -->
One nuance on *which* Opus does the delegating. If my planning session still has plenty of context window left, the same Opus instance that designed the feature also drives Codex - no handoff, full design context retained. If I'm running low on context, I don't push my luck: I write the plans to files, start a fresh Opus session, have it read them, and *that* session does the delegation. Either way the plans carry the context, so a cold Opus can pick up exactly where the planner left off. (More on this in **Passing Context**.)

<!-- [REUSED - NEEDS EDIT] kickoff message. Update file name (plan, not agent-spec) and step wording. -->
Then Opus sends Codex its first message via tmux, following the delegation protocol:

```
Read docs/plans/2026-02-18-global-fuzzy-search-plan.md FIRST.
It is your single source of truth. Follow it to the letter.
Execute the steps in order.
After EACH step, run: go test -v ./internal/manager/ ./internal/tui/
Commit after each step as specified.
Do NOT modify existing test files in tests/.
START NOW by reading the plan file.
```

<!-- [REUSED] -->
And Codex goes to work - methodically, without asking a single question. Because the plan left no ambiguity.

<!-- MEDIA: delegation-flow.mp4 (or GIF, 20-30 seconds)
     Split terminal: Opus left, Codex right. Opus sends first message → Codex reads files →
     writes code → commits → Opus runs CI → green. Speed up Codex portion 10-20x. Dark theme.
     Caption: "Opus delegates a step. Codex works. Opus reviews. Repeat." -->
<!-- [REUSED] media note. -->
![Video: delegation flow - Opus sends, Codex executes, Opus reviews](media/delegation-flow.mp4)

---

## Step 4: Delegate an Adversarial Review to the Review Agent

<!-- [TODO] NEW SECTION (author's instruction). Mostly new content.
     - After the coding agent finishes, Opus delegates an ADVERSARIAL REVIEW to a review agent.
     - This uses the Codex adversarial-review plugin/skill for Claude Code (see Resources).
     - The reviewer's job: try to break the implementation - find missed edge cases, wrong
       patterns, weakened tests, spec deviations - measured against the test plan from Step 2.
     - Why a separate agent: the executor won't critique its own work; independent review
       catches what self-review structurally can't.
     [REUSABLE seed material below, pulled from the old "Refinement Loop" reasoning:] -->

<!-- [REUSED - relocated] the "don't let the implementer grade itself" argument fits here. -->
> If the agent that writes the implementation also owns the verdict on whether it's correct, it has every incentive to declare success - quietly weakening assertions, skipping cases, or special-casing a test. So judgment never stays with the executor. A separate review agent, pointed at the test plan, tries to break the work before I trust it.

<!-- TODO: media - a screenshot/GIF of the adversarial review running via the plugin, with findings. -->

---

## Step 5: Review the Review

<!-- [TODO] NEW SECTION (author's instruction). NOT "confirm implementation using test plan".
     - The review agent produces findings; Opus (and I) review THOSE findings.
     - Not every finding is real - triage: which are genuine defects vs noise/false positives.
     - Decide what must be fixed, what's acceptable, what's out of scope.
     [REUSABLE seed material below:] -->

<!-- [REUSED - relocated] "unreasonable effectiveness" observation fits the review verdict. -->
The **unreasonable effectiveness** of this setup is how rarely a genuine problem survives this far. When the plan is precise, it is uncommon for the review to surface a real defect - but when it does, catching it here, before merge, is the whole point.

---

## Step 6: Iterate

<!-- [TODO] NEW SECTION (author's instruction).
     - Confirmed real findings loop BACK to planning: Opus plans the fixes, re-delegates to
       Codex, re-reviews. The cycle repeats until the test plan passes and the review is clean.
     - This is the feedback arrow in the method diagram.
     [REUSABLE seed material below:] -->

<!-- [REUSED - relocated] the per-step review loop + the phase-boundary safety property. -->
```
┌--------------┐    plan + tests    ┌--------------┐
│              │-------------------→│              │
│  Claude Opus │                    │ OpenAI Codex │
│  (Planner)   │←-------------------│  (Executor)  │
│              │   code + tests      │              │
└------┬-------┘                    └--------------┘
       │  ▲                                  │
       │  │ fix plan                         │ implementation
       │  └--------------┐                   ▼
       │            ┌-----┴--------┐   ┌--------------┐
       └-----------→│ Review Agent │←--│   (commit)   │
         delegate    │ (adversarial)│   └--------------┘
                     └--------------┘
```
<!-- [REUSED - NEEDS EDIT] old loop diagram was 2-agent + Developer; redrawn for the iterate cycle.
     Author to refine ASCII. -->

Because the work is phased, a rare miss surfaces at a step boundary, before it compounds. Each iteration is small: plan the fix, delegate it, review it, confirm.

---

## Passing Context

<!-- [TODO] NEW SECTION (author dictated the content - write it out):
     This section is about HOW we send what-to-do, and how we STORE the artifacts
     (implementation plans, test plans), and how we get them to the different agents.

     Cover, in the author's words:
       - How to send work to each agent and how to store the implementation plans and test plans.
       - Doing it with markdown files - and WHY markdown files:
           * plain text, diffable, version-controlled alongside the code
           * every agent can read them; they survive across sessions and context resets
           * a cold/ fresh agent can pick up exactly where the last left off
       - Alternatives:
           * Beads - for local tickets (Git-backed local issue tracker)
           * JIRA - for team/enterprise tracking
       - The principle: the planner owns the artifacts and the bookkeeping; the coding agent
         is handed exactly one job (implement the current step) and nothing else.
     [REUSABLE seed material below - the beads side-note and the planner-owns-bookkeeping
      paragraph - fold into this section.] -->

<!-- [REUSED - relocated] "what is Beads" side note. -->
> **What is Beads?** Beads (`bd`) is a lightweight, Git-backed issue tracker - tickets, dependencies, and cross-session memory that live in your repo. It's one option for tracking the work locally; plain markdown files or JIRA are others.

<!-- [REUSED - relocated & generalized] planner-owns-bookkeeping principle (was the beads-split paragraph). -->
Whatever the medium, the split is intentional. Tracking and verification stay with the planner. The coding agent is handed exactly one job - implement the current step - and nothing else. Reading tickets, deciding what counts as done, and closing them is the planner's responsibility, because the planner is also the reviewer. Giving the executor write access to the tracker just invites it to mark its own homework.

---

## How to Get Started

<!-- [TODO] write per author's instruction:
     - WHAT YOU NEED INSTALLED: the coding-agent CLI (Codex), tmux, your project's task runner
       (e.g. just), and the Claude Code plugins (delegate skill; Codex adversarial-review plugin).
     - PICK AN EASY EXAMPLE in your own coding project and go through the whole process ONCE
       before tackling anything complex.
     - WHY: learning this process takes time. If your first attempt is a hard feature, you'll
       struggle to get it unstuck when it doesn't work. Build the muscle on something small first.
     [REUSABLE seed material below - the old "Getting Started" 4 points; keep what fits.] -->

<!-- [REUSED] old getting-started points - still useful, trim into the above. -->
1. **Write a delegation doc** for your project. Document how to talk to your executor agent - what it can and can't do, how to prime it, how to structure instructions.
2. **Invest in your plan templates.** Both the implementation plan and the test plan: files to read, rules to follow, steps with exact code, verification commands, commit messages.
3. **Set up a startup script.** One command should launch the planner with all the context it needs.
4. **Trust the process.** The first time feels slow - you're writing detailed plans for a feature you could "just code." But the second time, you have patterns. The third time, it's muscle memory. And the implementation quality is consistently higher than doing it yourself.

---

## Summary

<!-- [REUSED - relocated] the metrics table. Re-measure against the REAL feature when built.
     "Estimated" duration was removed earlier; do not reintroduce an invented number. -->
For the example feature:

| Metric | Value |
|---|---|
| Planning conversation (Opus) | ~30 minutes |
| Design doc produced | 5 KB, 125 lines |
| Implementation plan produced | <!-- TODO: real size --> |
| Test plan produced | <!-- TODO: real size --> |
| TUI acceptance tests written | <!-- TODO: real count --> |
| Go unit test functions | <!-- TODO: real count --> |
| Implementation files | <!-- TODO: real count --> |

<!-- TODO: The exact wall-clock time / session count could not be recovered for the original
     run (transcripts purged). Measure for real when we implement. Frame around "2-4 sessions
     (typical)" - NOT an invented duration. -->

<!-- [TODO] closing payoff: the feature shipped, tests pass, review clean. Include the demo. -->
_[TODO: walk through the finished feature - what shipped, final CI status, a short demo clip
 (media/guard-global-search-demo.mp4 referenced at the foot of this file).]_

<!-- [REUSED] closing thesis line. -->
The future of AI-assisted development isn't picking the best model. It's building teams of models that complement each other's strengths.

---

## Resources

<!-- [TODO] bulleted list of markdown links. Candidates (author specified the plugins): -->
<!--
       - Guard repo: https://github.com/florianbuetow/guard
       - The delegate skill (Claude Code plugin, author's GitHub) - the tmux delegation protocol
       - The Codex adversarial-review plugin for Claude Code - used in Step 4
       - Implementation-plan + test-plan templates ("steal mine")
       - Claude Opus 4.6 announcement: https://www.anthropic.com/news/claude-opus-4-6
       - GPT-5.3-Codex announcement: https://openai.com/index/introducing-gpt-5-3-codex/
-->

---

*Florian Buetow builds [Guard](https://github.com/florianbuetow/guard), a CLI/TUI tool for protecting files from AI coding agents. He writes about AI-assisted development workflows at [his blog].*

<!-- MEDIA: guard-global-search-demo.mp4 (or GIF, 15-20 seconds)
     The finished feature in action. Guard TUI → press / (Search:) → press / again (Search:: ,
     colour change) → files stream in as flat paths → type query, results filter → Space toggles
     guard on a file → Escape back to tree. Dark theme, ~1.5x.
     Caption: "The finished feature: project-wide fuzzy search with guard toggling." -->
<!-- [REUSED] media note. -->
![Video: Guard global fuzzy search in action](media/guard-global-search-demo.mp4)

---

<!-- MEDIA PRODUCTION CHECKLIST (save to docs/blog/media/):
     1. hero-image.png - three-role concept art (planner / executor / reviewer)
     2. workflow-overview.gif - three-stage animated diagram with feedback loop
     3. conversation-flow.mp4 - the Opus planning conversation
     4. delegation-flow.mp4 - the tmux delegation (Opus left, Codex right)
     5. tmux-bridge-split.png - static split-pane screenshot
     6. review-run.* - the adversarial review running via the plugin   <!-- [TODO] new asset -->
     7. guard-global-search-demo.mp4 - the finished feature
     Tools: macOS Cmd+Shift+5; asciinema (+agg for GIF); Gifox/Kap.
     Diagram: Excalidraw → PNG frames → GIF, or Mermaid + screen-record.
-->

<!-- ============================================================
     PRESERVED FOR POSSIBLE REUSE - DROPPED SECTIONS
     The author dropped "Practical Tips" ("already baked into the article") and the
     standalone "Why Not Just Use One Model?" and "The Analogy" (consolidated into
     "Why Three Agents"). Kept here verbatim so we don't lose the wording if we want
     to graft any of it back into a step.

     --- Practical Tips (dropped) ---
     For Opus (The Planner):
       1. Ask one question at a time. Walls of questions overwhelm. Opus is great at follow-up.
       2. Let it explore the codebase first. Opus found 23 existing search tests and used that
          context in its questions.
       3. Trust its design instincts. It proposed the async streaming approach because it
          understood the Bubble Tea event model.
       4. Use it for ticket management. Opus understands dependency graphs - test tickets block
          implementation tickets, epics block specs.
     For Codex (The Executor):
       1. Zero ambiguity or it halts. If it stops to ask, your plan was unclear. Fix the plan.
       2. List every file it needs to read. "read these 18 files in this order", not "understand
          the codebase".
       3. Give it exact code. The actual struct, signature, assertions - not "add fuzzy logic".
       4. Tell it what NOT to do. "Don't modify existing tests. Don't run tmux."
       5. Enforce TDD explicitly. "Write tests first. Verify they fail. Then implement."
     For the Workflow:
       1. The plan is everything. Time spent making it precise is 10x more valuable than fixing
          the agent's mistakes later.
       2. Phase your commits. Break work into steps with verification points.
       3. Keep Opus in the loop for review. Codex codes; Opus validates intent.
       4. Automate the handoff. One command launches the planner with the delegation prompt loaded.

     --- Why Not Just Use One Model? (consolidated into "Why Three Agents") ---
     Opus-only for implementation: works for small features. For a large multi-file feature with
       async channels, TDD, and many test scripts, Opus drifts, loses context, forgets earlier
       decisions. Check-ins help but slow everything down.
     Codex-only for everything: doesn't ask clarifying questions, doesn't push back on bad ideas,
       implements whatever you say even if wrong. Without a detailed plan you get something that
       technically works but misses edge cases and conventions.
     Together: Opus catches design issues, Codex doesn't make implementation mistakes, the review
       agent catches what neither would catch about its own work. The plans are the contract.

     --- The Analogy (consolidated) ---
     Opus is the staff engineer who understands the architecture, asks the right questions, proposes
       approaches with trade-offs, and writes a plan anyone could implement.
     Codex is the focused specialist who takes that plan to a quiet corner and emerges with a clean,
       tested implementation that follows every instruction. Doesn't chitchat, doesn't second-guess.
     The review agent is the skeptic who reads the result assuming it's wrong and tries to prove it.
     ============================================================ -->
