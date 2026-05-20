---
title: "X-RAG"
subtitle: "Distributed Search & Indexing for Retrieval-Augmented Generation"
description: "Multi-tenant RAG platform combining vector, lexical, and graph retrieval on a Kubernetes-native stack."
date: 2025-12-21
draft: false
slug: "x-rag"
tech: ["Python", "Weaviate", "OpenSearch", "Neo4j", "Kafka", "Kubernetes"]
categories: ["RAG"]
tags: ["rag", "search", "distributed-systems"]
status: "active"
repo: "https://github.com/florianbuetow/x-rag"
demo: ""
video: ""
featured: true
---

## The Problem with Single-Modality Retrieval

Most RAG tutorials converge on the same architecture: embed your documents, store them in a vector database, query at runtime. That works until you have real queries, real traffic, and real tenants - at which point it starts failing in ways that are hard to instrument and expensive to fix.

The failure mode isn't that vector search is bad. It's that different queries have fundamentally different retrieval shapes. "Who in the conversation thread mentioned the compliance deadline?" is a lexical problem: exact token match, field-scoped. "Find documents semantically related to this concept" is a vector problem: dense embedding space, approximate nearest neighbor. "Which entities connect the customer to this incident through ownership and dependency chains?" is a graph problem: entity-relationship traversal, multi-hop reasoning. A single-modality system doesn't fail gracefully on out-of-domain queries - it quietly returns plausible-looking but wrong results, which is the worst possible failure mode for a system that's feeding an LLM.

x-rag is built around the premise that retrieval mode should match query type, not the other way around.

## Three Backends, Three Data Models

The architecture combines Weaviate for vector search (HNSW index, supports OpenAI, Cohere, and local embedding models), OpenSearch for lexical retrieval (BM25 with field boosts, custom analyzers, and token filters), and Neo4j for graph traversal (Cypher-based query planning, entity-relationship reasoning). Hybrid search fuses Weaviate and OpenSearch scores with a tunable alpha. Multi-hop retrieval uses LLM-powered question decomposition with iterative retrieval passes. A cross-encoder or LLM re-ranker runs post-retrieval.

The complexity cost is real. Three backends means three systems to operate, three data models to keep consistent during ingestion, three failure modes to instrument. This isn't a decision to take lightly. The justification is precision and recall across query types: a graph-only system can approximate lexical search through property queries, but poorly; a vector-only system can approximate entity relationships through embedding similarity, but also poorly. The approximations compound when queries mix modalities, which production queries routinely do.

The alternative - picking one backend and accepting the approximations - is a reasonable starting point. It becomes a liability at scale, where retrieval quality directly affects downstream LLM output quality, and "why is this query returning garbage" becomes a support ticket instead of a tunable parameter.

## Isolation as a First-Class Primitive

Multi-tenancy in x-rag is expressed through per-namespace isolation: separate Weaviate, OpenSearch, and Neo4j indices per domain, with independent autoscaling on the API and indexer tiers. Kafka ingestion uses parallel consumers per namespace with at-least-once delivery semantics.

The cost is infrastructure density. More indices means more headroom to provision, more ingestion pipelines to manage, more Grafana dashboards to maintain. The benefit is that namespaces don't share fate. A noisy tenant running bulk re-indexing doesn't degrade query latency for other tenants. Per-tenant scale knobs mean a high-traffic namespace can scale its retrieval compute independently without pulling up the whole cluster. Per-tenant observability means "this namespace's p95 latency degraded at 14:32" is a queryable fact, not an inference from aggregate metrics.

The alternative - shared indices with namespace filters - is operationally simpler but introduces noisy-neighbor coupling at the storage layer, where it's hardest to isolate and remediate.

## Observability Is an Architecture Decision

The Four Golden Signals (latency, traffic, errors, saturation) applied uniformly to every service is necessary but not sufficient. The substantive observability work in x-rag is in two places.

First: LLM calls are instrumented separately through Langfuse and OpenTelemetry distributed tracing. LLM calls have different latency distributions, different failure modes, and different diagnostic questions than infrastructure calls. Mixing them into the same metric namespace obscures both.

Second: Prometheus histogram buckets are tuned per operation class. FAST operations - cache hits, embedding lookups - target p99 under 100ms. MEDIUM operations - Weaviate queries - target p99 under 500ms. SLOW operations - LLM generation - target p99 under 30 seconds. BATCH operations - Kafka consumption - target p99 under 5 seconds. The same bucket set cannot serve all of these; a bucket granularity that makes a 50ms cache lookup meaningful will render a 15-second LLM generation unreadable, and vice versa. Getting this wrong means your percentiles are technically correct and operationally useless.

Redis caching at the retrieval layer handles the repeated-query pattern that LLM chat loops produce, reducing backend load 60–80% on repeated queries. Target p95 retrieval latency is 100ms.

## Deployment Shape

The Kubernetes deployment follows a clear principle: StatefulSets for the storage backends (Weaviate, OpenSearch, Neo4j), stateless deployments with horizontal pod autoscaling for everything else (API, indexer, re-ranker). Kafka decouples write rate from index update rate, which matters when ingestion bursts - indexing can drain the queue at its own pace without blocking the write path.

The gRPC and FastAPI API layer is stateless by construction. Scaling the retrieval tier is a matter of adding pods; the storage tier scales on its own axis, manually, because storage backends have state that requires more careful capacity planning than compute.

This is the part most RAG tutorials omit: the operational surface area downstream of the retrieval call. Ingestion throughput, per-tenant isolation, histogram tuning, caching strategy - none of it shows up in a proof-of-concept, and all of it determines whether the platform survives a real workload. The implementation is on [GitHub](https://github.com/florianbuetow/x-rag).
