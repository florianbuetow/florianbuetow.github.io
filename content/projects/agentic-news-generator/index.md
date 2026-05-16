---
title: "Agentic News Generator"
subtitle: "Generate a custom newspaper with an AI agent based on your favorite YouTube channels"
description: "Crawls AI channels, transcribes video, segments by topic, and generates a weekly newspaper-style digest."
date: 2026-04-15
draft: false
slug: "agentic-news-generator"
tech: ["Python", "MLX Whisper", "Nuxt", "LLMs"]
categories: ["AI Agents"]
tags: ["ai-agents", "llm", "content-generation"]
status: "active"
repo: "https://github.com/florianbuetow/agentic-news-generator"
demo: ""
video: ""
featured: false
---

## The Problem with Per-Video Summaries

There are dozens of AI-focused YouTube channels worth following, and the combined output is several hours of video per week. No one watches all of it, and the common workaround — skimming transcripts or reading per-video summaries — preserves the wrong unit of analysis. Each video is treated as an isolated artifact, which means the more interesting signal gets lost: when three creators who don't coordinate with each other are independently covering the same development, that convergence is meaningful. Per-video summaries can't surface it.

The goal here was a weekly digest where the value comes from cross-video topic clustering, not from summarizing any individual video. If five channels all touched on a particular model release or infrastructure pattern in the same week, the output should reflect that as a coherent piece, not as five separate bullets.

## Where Determinism Beats an LLM

The pipeline has seven stages: download, audio extraction, transcription, hallucination filtering, topic segmentation, cross-video aggregation, and article generation. The interesting design question is not which stages use an LLM — it's which ones shouldn't.

Whisper's failure mode under certain conditions is well-documented: it produces loops of repeated phrases rather than failing cleanly. An LLM judge asked to "check whether this transcript looks right" will sometimes rationalize the repetition rather than flag it, because looped text isn't obviously malformed from a language modeling perspective. A deterministic repetition detector doesn't have that problem. It checks for a structural pattern in the output — repeated n-grams above a threshold — and drops the transcript if the pattern is present. No model needed, no ambiguity.

Filtering also drops videos under 120 seconds and silent audio before transcription runs. These are cheap checks that save compute and prevent bad input from propagating downstream.

The contrast with the later stages is deliberate. Topic segmentation and article generation both have open-ended output spaces — there's no fixed schema for "what topics are in this transcript" or "what makes a good paragraph about them." That's where LLMs earn their place. The segmentation prompt asks the model to identify coherent topic boundaries in a transcript; the generation step asks agents to synthesize aggregated content into readable prose. Neither task has a deterministic equivalent.

## Local Transcription vs. Cloud

MLX Whisper runs on Apple Silicon, which means transcription happens locally. The choice trades raw throughput for cost, privacy, and operational simplicity. Audio never leaves the machine; there's no per-minute billing; and the pipeline can run unattended overnight without accumulating an API bill proportional to how many hours of video were queued.

The latency tradeoff is real but acceptable for an async weekly job. The pipeline isn't trying to serve a real-time use case — it runs once, produces an archive, and the output is consumed later. Cloud transcription would finish faster, but the speed doesn't matter when the consumer is a weekend reader.

Language detection is handled implicitly: the pipeline uses the medium.en Whisper model for English audio and falls back to medium with translation enabled for other languages. That covers the realistic distribution of content from AI-focused channels without requiring a separate language identification step.

## A Stage-Per-Concern Architecture

Each stage of the pipeline is a discrete, restartable unit. Download, convert, transcribe, segment, aggregate, generate, render — each has a single responsibility and writes its output to a predictable location. That structure isn't accidental. When a stage fails or needs to be replaced, you restart from that point without re-running everything upstream. When you want to swap the transcription model or change the aggregation prompt, the surface area of the change is bounded.

The "agent" label applies specifically to the aggregation and generation stages. Elsewhere in the pipeline, the work is deterministic plumbing. That distinction matters for debuggability: if the output is wrong, you can narrow the failure to a stage rather than reasoning about a monolithic prompt chain.

The rendering layer uses Nuxt as a static-site generator — it takes the generated article content and produces a newspaper-style HTML archive. Nuxt isn't doing anything dynamic here; it's a templating tool for structured output.

## What the Design Reveals

Pipelines that mix deterministic and probabilistic stages tend to surface an underappreciated design concern: the interface between them. The repetition detector exists precisely because Whisper's failure mode, if unfiltered, would propagate into the segmentation and aggregation stages. An LLM asked to segment a hallucinated transcript doesn't know the input is bad — it will produce output anyway, and that output will flow downstream.

The pre-filter's job is to catch the known failure mode of the upstream model before the downstream stages amplify it. That's a general pattern: when you chain probabilistic components, the most reliable place to add a check is at the point where you have a structural expectation about the output — and a deterministic way to verify it.
