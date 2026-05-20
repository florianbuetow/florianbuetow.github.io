---
title: "MiniRAG"
subtitle: "Local hybrid search engine for your docs with MCP integration for AI agents"
description: "A minimalist hybrid search engine for local documents, served to AI agents over MCP."
date: 2026-04-01
draft: false
slug: "mini-rag"
tech: ["Python", "FastText", "FAISS", "Tantivy", "SQLite", "MCP"]
categories: ["RAG"]
tags: ["rag", "search", "mcp", "ai-agents"]
status: "active"
repo: "https://github.com/florianbuetow/mini-rag"
demo: ""
video: ""
featured: true
---

## Why Local-First

The use case that shaped this project is narrow on purpose: a personal corpus of markdown and text files - books on refactoring, prompting, and architecture - that an AI agent like Claude Desktop or Codex should be able to query as a grounded tool. No multi-tenant access, no petabyte scale, no SLA. Just one person's reading list, indexed and searchable offline.

That constraint eliminates most of the surface area where cloud RAG services earn their keep. There are no cold-start costs to amortize across users, no compliance requirement forcing data into a managed platform, and no latency budget that requires a globally distributed inference tier. What remains is the question of how to build something that is fast enough, private enough, and simple enough to maintain without infrastructure overhead.

Local-first is not a philosophical stance here - it follows from the workload. Documents never leave the machine, which matters when the corpus includes notes on proprietary codebases or personal research. The index rebuilds from scratch in under ten minutes for ten thousand documents on a modern laptop, so the system does not need to be particularly clever about state. It needs to be correct and cheap to operate.

## The Embedding Decision

The most consequential early decision was which embedding model to use. The options reduce to two families: API-based models from providers like OpenAI or Cohere, and locally runnable models like Facebook's FastText.

API embeddings produce higher-quality dense representations for most English-language semantic tasks. The cost is latency on indexing (each chunk requires a round-trip), a per-token fee that compounds across re-indexes, and a hard dependency on network availability and provider uptime. For a personal knowledge base, that last point is disqualifying - the whole motivation for local-first is offline usability.

FastText runs in-process via FAISS. The embedding quality is lower, particularly on queries that require nuanced semantic matching across long paraphrases. For a corpus of technical documents queried by engineers who know approximately what they're looking for, this is an acceptable tradeoff. The gap between FastText and a frontier embedding model matters more when queries are vague; precise technical queries tend to anchor on vocabulary that lexical search already handles well, which is why the hybrid approach exists.

The decision: local FastText, with the acknowledgment that semantic recall on open-ended queries is not the design center. The design center is retrieval that a human expert would recognize as relevant, at zero marginal cost per query.

## Lexical Search: Tantivy Over a Standing Server

BM25 lexical search handles what dense vector search reliably misses: named entities, exact identifiers, code tokens, version numbers, acronyms. Any RAG pipeline serving technical documents needs both modes. The question is which BM25 backend to use.

The two realistic options were Elasticsearch/OpenSearch (run locally via Docker) and Tantivy (a Rust-native embedded search library). Elasticsearch is the obvious choice if you need a query DSL, aggregations, multi-index federation, or integration with an existing observability stack. None of those apply here.

Tantivy embeds into the Python process via its bindings, requires no sidecar, and starts in milliseconds. It gives up the Elasticsearch ecosystem entirely - no Kibana, no index snapshots with S3, no plugin architecture. For this workload, those are not losses. The simpler operational model is the point: one process, one config file, one place to look when something goes wrong.

## Simplicity Wagers in the Design

Two design choices in mini-rag look like omissions but are deliberate bets on operational simplicity.

The first is no individual document deletion. Documents stay in their source folders; the index reflects whatever is in those folders at indexing time. Re-indexing from scratch is the only supported way to remove a document. This eliminates the bookkeeping required to maintain a consistent delete log across the SQLite document store, the FAISS index, and the Tantivy index - three independent data structures that would each need a synchronized delete path. Re-indexing ten thousand documents in under ten minutes makes that complexity unnecessary. The wager is that the corpus changes slowly enough that full re-indexing is the right abstraction boundary.

The second is that cross-encoder reranking ships off by default. Reranking can improve precision on hybrid results by re-scoring the top-k candidates with a more expensive model. The cost is latency added to every query. For personal knowledge base queries - where the user typically knows what they are looking for and the top result is usually sufficient - the precision gain does not justify the added latency in the common case. The option exists for corpora where it does.

Everything else is configuration-driven via `config.yaml`. Corpus path, chunk size, embedding model, reranking flag - none of these are hardcoded. The same binary serves a notes corpus and a book corpus without recompilation, which matters when the use case evolves.

## What This Gives an AI Agent

The MCP server is where the design choices compound into something useful for AI workflows. When Claude Desktop or a Codex agent queries mini-rag as a tool, it gets a typed call with a structured response: ranked chunks with source attribution, ready to include in context. The agent does not need to manage retrieval logic or handle raw document bytes.

Latency matters here in a specific way: retrieval that takes too long increases the probability that the model starts generating before grounded context arrives, which suggests a higher hallucination rate on factual questions. The in-process design keeps query latency low enough that it is not a bottleneck in the agent's reasoning loop.

The privacy-sensitive case is also concrete. A corpus of internal architecture notes or proprietary API documentation should not transit a cloud embedding endpoint on every query. With mini-rag, it does not. The agent gets fast, typed, grounded retrieval over private documents without any data leaving the machine.

The [repository](https://github.com/florianbuetow/mini-rag) has the configuration reference and setup instructions for connecting to Claude Desktop over MCP.
