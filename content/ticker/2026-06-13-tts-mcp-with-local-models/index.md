---
title: "TTS-MCP With Local Models"
slug: "tts-mcp-with-local-models"
date: 2026-06-13
draft: true
description: "A local, open-source MCP server that lets your AI agents speak their status out loud with Mistral's Voxtral text-to-speech models, so you can step away from the terminal and still know what they are doing."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools", "Ticker News"]
tags: ["MCP", "Local Models", "TTS", "Claude Code"]
---

{{< sidenote label="Code" >}}[github.com/florianbuetow/tts-mcp](https://github.com/florianbuetow/tts-mcp){{< /sidenote >}}

![TTS-MCP architecture: an AI agent, HTTP client, and terminal user feed an MCP server and a FastAPI server that run the Voxtral 4B TTS model on Apple Silicon via MLX and stream audio to the speakers.](tts-mcp.webp?zoom "How TTS-MCP fits together, from your AI agent down to your speakers")

When you kick off a long-running task with an autonomous agent, whether it is Claude Code, Codex, or a custom runner, you usually end up locked into the terminal. You sit there, watching text buffers scroll, waiting to see when it finishes, breaks, or needs human input.

Personally, I don't want to watch a terminal. I want to be able to pace around the room, let my mind wander, and actually think about the system architecture while the agents execute their tasks in the background.

To achieve that, I decided to equip my agents with a way to report their status to me via audio and built a local voice layer for autonomous tooling: TTS-MCP.

TTS-MCP is open-source and exposes a local text-to-speech engine, based on Mistral's open-weight Voxtral TTS models, directly to your AI agents via MCP. You simply prompt them to use TTS-MCP to give you a TLDR when they are done or need human input because they got stuck. And they'll literally just tell you.

Here is a sample of the local voice output:

{{< audio src="tts-mcp-male-de.m4a" caption="Sample output: German, male voice" >}}

## The Architecture

The architecture is entirely self-hosted and straightforward:

```mermaid
flowchart LR
    A["AI Agent<br/>(Claude)"] --> B["MCP Server<br/>(TypeScript)"]
    B --> C["FastAPI Server<br/>(Python)"]
    C --> D["Voxtral 4B<br/>via MLX"]
    D --> E["Speakers"]
```

The system coordinates a few distinct pieces to make the interaction seamless:

- Local Inference: It runs Mistral's Voxtral 4B text-to-speech model. The weights stay in memory via the TTS API Server, running completely offline with no API costs or cloud privacy leaks.
- Lookahead Chunking: To eliminate the latency gap between sentences, the FastAPI backend processes requests sequentially through a background work queue using a lookahead pattern - generating the next semantic audio slice while your speakers are still playing the current one.
- Broadcast-Standard Loudness Matching: Synthetic voices vary in their base gain levels. To keep transitions smooth, the audio pipeline passes every generated utterance through a boost-only normalization filter to keep playback levels balanced.

If you want to run TTS-MCP yourself, the setup instructions are provided in the links below.

## Links

- [TTS-MCP project page](/projects/tts-mcp/)
- TTS-MCP source on [GitHub](https://github.com/florianbuetow/tts-mcp)
