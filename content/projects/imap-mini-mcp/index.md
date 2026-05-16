---
title: "IMAP Mini MCP"
subtitle: "MCP server that lets AI agents read, search, and organize your email inbox"
description: "Read, search, move, star, and draft email through any IMAP server, exposed as MCP tools."
date: 2026-03-01
draft: false
slug: "imap-mini-mcp"
tech: ["Node.js", "TypeScript", "IMAP", "MCP"]
categories: ["MCP"]
tags: ["mcp", "ai-agents", "email", "imap"]
status: "active"
repo: "https://github.com/florianbuetow/imap-mini-mcp"
demo: ""
video: ""
featured: false
---

## The Problem with Handing an Agent Your Inbox

Email is one of the highest-value contexts an AI assistant could have. Most knowledge workers effectively live in their inbox — it's where decisions arrive, where threads stall, where things get lost. Automating any meaningful part of that workflow is genuinely useful.

But handing an agent full email authority is a different proposition. Send and delete are irreversible operations. A misfire on either is categorically worse than most other agent errors: you can't un-send an email to your board, and you can't recover a message that was permanently deleted before you noticed it mattered. The damage is asymmetric — a false positive on an archiving decision costs seconds to fix; a false positive on a send costs real relationships.

The deeper problem is that most email APIs don't distinguish between these risk classes. "Read" and "send" often live on the same permission surface, behind the same OAuth scope or the same credential set. If you want to give an agent read access, you're frequently also giving it send access, whether you intend to or not.

## Reversibility as the Design Axis

The core design decision behind imap-mini-mcp is to treat reversibility as the primary axis for what the agent can and cannot do.

Email operations split cleanly into two groups. Reading, searching, moving between folders, starring, and composing drafts are all reversible — or at worst, trivially correctable. Sending and permanently deleting are not. The agent gets the full reversible set. The irreversible set is withheld entirely — not gated behind a confirmation prompt, not wrapped in a warning, simply absent from the tool surface. There is no `send_email` tool. There is no `delete_message` tool.

This isn't a trust decision about the model. It's an architectural acknowledgment that irreversible operations require a human in the loop, and the cleanest way to enforce that is to make the operation structurally unavailable. The agent drafts; the human sends. The agent moves to trash; the human decides whether to empty it. The latency cost of that human step is low; the downside protection is high.

"Draft, don't send" is the specific form this takes for composition. The agent can do 95% of the work — pulling context from the thread, assembling a response, setting tone — and write it as a draft. The human reviews and hits send. That's a meaningful reduction in friction without a meaningful increase in risk.

## Building on IMAP

IMAP is a 35-year-old protocol. It is also the lingua franca of email: Gmail, Outlook, Fastmail, and ProtonMail Bridge all speak it. Using IMAP as the transport layer means a single code path works across all of them. That's not free — you have to handle TLS and authentication variance across providers — but it's considerably cheaper than maintaining six provider-specific API integrations.

The MCP tool surface maps directly to IMAP operations, with the safety boundary enforced by omission. Moving a message to a different folder: available. Marking it starred: available. Permanent deletion: not exposed. The tool list is the safety policy.

Provider quirks are handled explicitly rather than by auto-detection. ProtonMail Bridge, for example, runs locally, doesn't support STARTTLS, and presents a self-signed certificate. These are not edge cases to paper over — they're differences that require explicit configuration. The env-var approach (`IMAP_TLS_REJECT_UNAUTHORIZED`, `IMAP_STARTTLS`, `IMAP_SECURE`) makes the configuration surface legible. The operator sets the values; the code does what it's told. Clear is better than magic when the failure modes involve credentials.

## Where Speech-to-Text Completes the Loop

The original design goal was a programmable inbox assistant. A secondary use pattern emerged that's worth noting because it fits the tool's shape unusually well: pairing it with speech-to-text input.

Conversational inbox triage — "archive anything from LinkedIn, star the two emails from the infrastructure team, draft a reply to the vendor saying I'll review the proposal by Friday" — maps naturally to how people actually think about their email backlog. It doesn't map naturally to point-and-click. The latency cost of a GUI drops to near zero when the agent handles the mechanics and the human just speaks intent.

On macOS, SuperWhisper works well for this. On Windows, Whisperflow. Neither is part of the project; both connect straightforwardly via Claude Desktop or any MCP-compatible client. The combination is less an integration than a workflow affordance — the tool's shape happens to make it worthwhile.

## What This Demonstrates

The project is a small, self-contained example of a general pattern: constrain the agent's authority to the operations that are safe to automate, and design the constraint into the structure rather than relying on the model to exercise restraint. The model doesn't need to know not to send email. The tool doesn't exist.

That pattern scales. The same reasoning applies to any agent operating in a domain with asymmetric failure modes — financial transactions, infrastructure changes, communications on behalf of an organization. Identify the reversibility boundary, give the agent everything on one side, and withhold everything on the other.

The code and configuration details are in the [repository](https://github.com/florianbuetow/imap-mini-mcp).
