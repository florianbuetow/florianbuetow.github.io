---
title: "Token Economics Playground: Single session vs. Orchestration"
slug: "single-session-vs-orchestrator-token-economics"
date: 2026-06-12
draft: false
description: "An interactive playground that shows, qualitatively, when an orchestrator session dispatching tasks to subagents becomes cheaper than running everything in a single session."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools", "Ticker News"]
tags: ["Claude Code", "Agent Orchestration", "LLM"]
---

{{< sidenote label="The Crossover" >}}For one or two tasks, a single session is cheaper. Past that, delegating to subagents wins depending on context length and task complexity. A single session keeps everything in one growing context and takes advantage of caching that avoids reloading the context when it completes new tasks itself.{{< /sidenote >}}

![Chart comparing the token cost of a single session against an orchestrator that dispatches to subagents](dispatch-economics.webp?zoom "Dispatch Economics Dashboard/Playground")

To learn more about the token economics of using a single session vs. an orchestrator session that dispatches tasks to subagents, I created a tool with Claude to make it visible. 

The result is an interactive dashboard/playground that shows how token consumption and API costs change when using either method. You can create and configure agents to see how the economics change or select one of the predefined scenarios with up to four agents. Even though this was vibe coded with a few prompts, it shows that there is a line where one method becomes cheaper than the other, depending on the size of your agent team.

You can try the interactive playground [here](https://claude.ai/public/artifacts/1b7ad4b1-66c6-4dca-b2ce-dc93a117665b)

Comment on [LinkedIn](https://www.linkedin.com/posts/fbuetow_last-night-i-played-around-a-bit-with-claude-share-7470843456207265794-3DnU/)

## Links

- Interactive Playground: [Dispatch Economics](https://claude.ai/public/artifacts/1b7ad4b1-66c6-4dca-b2ce-dc93a117665b)
