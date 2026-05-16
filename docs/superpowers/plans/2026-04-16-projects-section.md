# Projects Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a `/projects/` section with a filterable list page and seven individual portfolio case-study pages, matching the existing Hugo blog's 3-column visual language.

**Architecture:** Hugo content section under `content/projects/` using page bundles. Custom `layouts/projects/articles.html` (list) and `layouts/projects/single.html` (detail) mirror the blog/ticker templates but render project-specific meta. Reuses the existing `assets/js/filter.js` by populating `data-tags` from `tech` front-matter. Adds a small CSS block for status dots and a detail-sidebar project-meta card.

**Tech Stack:** Hugo (static site), Go templates, vanilla JS (existing filter.js), CSS (existing single-file `assets/css/main.css`).

---

## Reference — spec location

Full design spec: `docs/superpowers/specs/2026-04-16-projects-section-design.md`. Re-read it if any task detail is unclear.

## Reference — verification approach

This codebase has no unit-test framework; it is a Hugo static site. TDD here means:

1. Before each change, state the expected visible result (built HTML, rendered page element, URL resolution).
2. Make the change.
3. Run `just ci-quiet` — expect "All CI checks passed".
4. For UI changes, run `just start` then `curl -s http://127.0.0.1:1313/<path>/ | grep <marker>` to confirm the expected element renders.
5. Run `just stop` when done with a server session.

Commit frequently — one commit per completed task.

## File Structure

**Create:**
- `layouts/projects/articles.html` — list page template
- `layouts/projects/single.html` — detail page template
- `archetypes/projects.md` — new-project scaffold
- `content/projects/mini-rag/index.md` — project page
- `content/projects/guard/index.md` — project page
- `content/projects/agentic-news-generator/index.md` — project page
- `content/projects/x-rag/index.md` — project page
- `content/projects/imap-mini-mcp/index.md` — project page
- `content/projects/touchtask/index.md` — project page
- `content/projects/ai-guardrails/index.md` — project page

**Modify:**
- `hugo.toml` — add `projects = '/projects/:slug/'` to `[permalinks]`
- `content/projects/_index.md` — set `layout: "articles"`
- `assets/css/main.css` — append `/* === PROJECTS === */` block

---

## Task 1: Wire Hugo permalink + section layout

**Files:**
- Modify: `hugo.toml:45-47` (the `[permalinks]` block)
- Modify: `content/projects/_index.md` (entire file)

- [ ] **Step 1: State expected result**

After this task, `hugo list all | grep projects` should show the `projects` section and any project pages that exist, and the section URL should be `/projects/`. No project pages exist yet, so the list will be empty.

- [ ] **Step 2: Modify `hugo.toml`**

Replace the current `[permalinks]` block:

```toml
[permalinks]
  blog = '/blog/:slug/'
  ticker = '/ticker/:slug/'
```

with:

```toml
[permalinks]
  blog = '/blog/:slug/'
  ticker = '/ticker/:slug/'
  projects = '/projects/:slug/'
```

- [ ] **Step 3: Rewrite `content/projects/_index.md`**

Replace the existing contents with:

```markdown
---
title: "Projects"
layout: "articles"
---
```

- [ ] **Step 4: Verify build**

Run: `just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 5: Commit**

```bash
git add hugo.toml content/projects/_index.md
git commit -m "feat(projects): wire permalink and section layout"
```

---

## Task 2: Scaffold seven project stubs

Create minimal page bundles for all seven projects so the list page has real data to render in Task 3. Bodies are one-paragraph placeholders that will be replaced with real case-study content in Tasks 8–14.

**Files:**
- Create: `content/projects/mini-rag/index.md`
- Create: `content/projects/guard/index.md`
- Create: `content/projects/agentic-news-generator/index.md`
- Create: `content/projects/x-rag/index.md`
- Create: `content/projects/imap-mini-mcp/index.md`
- Create: `content/projects/touchtask/index.md`
- Create: `content/projects/ai-guardrails/index.md`

- [ ] **Step 1: State expected result**

Seven new files exist. Each has full front matter (title, subtitle, description, date, slug, tech, categories, status, repo, demo, video, featured) and a one-sentence placeholder body. The build succeeds.

- [ ] **Step 2: Create `content/projects/mini-rag/index.md`**

```markdown
---
title: "MiniRAG"
subtitle: "Local hybrid search for your docs with MCP integration"
description: "A minimalist hybrid search engine for local documents, served to AI agents over MCP."
date: 2026-03-15
slug: mini-rag
tech: ["Python", "FastText", "FAISS", "Tantivy", "SQLite", "MCP"]
categories: ["Search & Retrieval"]
status: "active"
repo: "https://github.com/florianbuetow/mini-rag"
demo: ""
video: ""
featured: true
---

Placeholder body. Real case-study content lands in a later task.
```

- [ ] **Step 3: Create `content/projects/guard/index.md`**

```markdown
---
title: "Guard"
subtitle: "Protect files from unwanted modification by AI coding agents"
description: "Toggles file immutability and ownership so AI agents cannot silently overwrite your work."
date: 2026-02-13
slug: guard
tech: ["Go", "CLI", "Unix permissions"]
categories: ["Developer Tooling"]
status: "active"
repo: "https://github.com/florianbuetow/guard"
demo: ""
video: ""
featured: false
---

Placeholder body. Real case-study content lands in a later task.
```

- [ ] **Step 4: Create `content/projects/agentic-news-generator/index.md`**

```markdown
---
title: "Agentic News Generator"
subtitle: "AI-agent-driven newspaper from curated YouTube channels"
description: "Crawls AI channels, transcribes video, segments by topic, and generates a weekly newspaper-style digest."
date: 2026-03-20
slug: agentic-news-generator
tech: ["Python", "MLX Whisper", "Nuxt", "LLMs"]
categories: ["AI Agents"]
status: "active"
repo: "https://github.com/florianbuetow/agentic-news-generator"
demo: ""
video: ""
featured: false
---

Placeholder body. Real case-study content lands in a later task.
```

- [ ] **Step 5: Create `content/projects/x-rag/index.md`**

```markdown
---
title: "X-RAG"
subtitle: "Distributed search and indexing for RAG at scale"
description: "Multi-tenant RAG platform combining vector, lexical, and graph retrieval on a Kubernetes-native stack."
date: 2026-01-15
slug: x-rag
tech: ["Python", "Weaviate", "OpenSearch", "Neo4j", "Kafka", "Kubernetes"]
categories: ["Search & Retrieval"]
status: "active"
repo: "https://github.com/florianbuetow/x-rag"
demo: ""
video: ""
featured: true
---

Placeholder body. Real case-study content lands in a later task.
```

- [ ] **Step 6: Create `content/projects/imap-mini-mcp/index.md`**

```markdown
---
title: "IMAP Mini MCP"
subtitle: "An MCP server that lets AI agents read and organise your inbox"
description: "Read, search, move, star, and draft email through any IMAP server, exposed as MCP tools."
date: 2026-03-05
slug: imap-mini-mcp
tech: ["Node.js", "TypeScript", "IMAP", "MCP"]
categories: ["MCP & Integrations"]
status: "active"
repo: "https://github.com/florianbuetow/imap-mini-mcp"
demo: ""
video: ""
featured: false
---

Placeholder body. Real case-study content lands in a later task.
```

- [ ] **Step 7: Create `content/projects/touchtask/index.md`**

```markdown
---
title: "TouchTask"
subtitle: "Time blocks, habits, and focused work sessions in one interface"
description: "A client-side productivity app combining time blocking, habit tracking, pomodoro, and kanban."
date: 2025-10-10
slug: touchtask
tech: ["React", "Vite", "localStorage"]
categories: ["Productivity"]
status: "active"
repo: "https://github.com/florianbuetow/touchtask"
demo: "https://cracking-ai-engineering.com/touchtask/"
video: "https://www.youtube.com/watch?v=Bihlr5uGq8g"
featured: false
---

Placeholder body. Real case-study content lands in a later task.
```

- [ ] **Step 8: Create `content/projects/ai-guardrails/index.md`**

```markdown
---
title: "AI Guardrails"
subtitle: "Project templates with built-in guardrails for AI coding agents"
description: "Copier templates for six languages that enforce strict validation so AI-generated code fails fast on antipatterns."
date: 2026-02-20
slug: ai-guardrails
tech: ["Copier", "Python", "Java", "Go", "Elixir", "C++", "Rust"]
categories: ["Developer Tooling"]
status: "active"
repo: "https://github.com/florianbuetow/ai-guardrails"
demo: ""
video: ""
featured: false
---

Placeholder body. Real case-study content lands in a later task.
```

- [ ] **Step 9: Verify build**

Run: `just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 10: Commit**

```bash
git add content/projects/
git commit -m "feat(projects): scaffold seven project stubs with front matter"
```

---

## Task 3: Create list template `layouts/projects/articles.html`

**Files:**
- Create: `layouts/projects/articles.html`

- [ ] **Step 1: State expected result**

After this task, `curl -s http://127.0.0.1:1313/projects/` returns HTML that lists all seven projects, with `featured: true` entries (`mini-rag`, `x-rag`) on top, then the rest sorted by date descending. Each `<article class="post">` carries `data-categories` and `data-tags` attributes. A status dot appears in the left meta column.

- [ ] **Step 2: Create the file**

```html
{{ define "main" }}
<div class="main-layout">
    <div class="post-list">
        {{ $all := where .Pages "Type" "!=" "page" }}
        {{ if not $all }}{{ $all = .Pages }}{{ end }}
        {{ $featured := where $all "Params.featured" true }}
        {{ $rest := where $all "Params.featured" "!=" true }}
        {{ $posts := $featured | append $rest }}
        {{ range $i, $p := $posts }}
            <article class="post"
                     data-categories="{{ delimit ($p.Params.categories | default slice) "," }}"
                     data-tags="{{ delimit ($p.Params.tech | default slice) "," }}">
                <aside class="post-meta">
                    {{ with $p.Params.status }}
                    <div class="meta-item"><span class="status-dot status-{{ . }}"></span> {{ . | title }}</div>
                    {{ end }}
                    <div class="meta-item"><span class="meta-icon"></span> {{ $p.Date.Format "Jan 02, 2006" }}</div>
                </aside>
                <div class="post-content">
                    <h2><a href="{{ $p.RelPermalink }}">{{ $p.Title }} &raquo;</a></h2>
                    {{ with $p.Params.subtitle }}<h3>{{ . }}</h3>{{ end }}
                    <p>{{ with $p.Params.description }}{{ . }}{{ else }}{{ $p.Summary | plainify | truncate 280 }}{{ end }}</p>
                </div>
            </article>
            {{ if lt (add $i 1) (len $posts) }}<hr class="divider">{{ end }}
        {{ end }}
        <p class="no-results" id="no-results">No projects match your filters.</p>
    </div>
    <aside class="filter-sidebar" id="filter-sidebar"></aside>
</div>
{{ end }}

{{ define "scripts" }}
{{ $js := resources.Get "js/filter.js" | js.Build | minify | fingerprint }}
<script src="{{ $js.RelPermalink }}" integrity="{{ $js.Data.Integrity }}" defer></script>
{{ end }}
```

- [ ] **Step 3: Verify build**

Run: `just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 4: Verify list renders**

Run:
```bash
just start
sleep 2
curl -s http://127.0.0.1:1313/projects/ | grep -c 'class="post"'
```
Expected: `7`

- [ ] **Step 5: Verify featured-first ordering**

Run:
```bash
curl -s http://127.0.0.1:1313/projects/ | grep -oE 'href="/projects/[^"]+"' | head -2
```
Expected (order may vary between the two featured entries, but both should appear before any non-featured):
```
href="/projects/x-rag/"
href="/projects/mini-rag/"
```
(Acceptable if `mini-rag` precedes `x-rag` — both are `featured: true`.)

- [ ] **Step 6: Stop server**

Run: `just stop`

- [ ] **Step 7: Commit**

```bash
git add layouts/projects/articles.html
git commit -m "feat(projects): add list template with featured-first ordering"
```

---

## Task 4: Create detail template `layouts/projects/single.html`

**Files:**
- Create: `layouts/projects/single.html`

- [ ] **Step 1: State expected result**

After this task, `curl -s http://127.0.0.1:1313/projects/mini-rag/` returns HTML with: back link to `/projects/`, a `.project-meta-card` containing status, date, category, tech list, and repo link, a TOC placeholder, the article body, and the right sidebar for side notes.

- [ ] **Step 2: Create the file**

```html
{{ define "main" }}
<div class="article-layout">

    <nav class="article-sidebar-left">
        <a href="{{ with .Parent }}{{ .RelPermalink }}{{ else }}/projects/{{ end }}" class="meta-row back-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
            Back to projects
        </a>
        <hr class="sidebar-divider">

        <div class="project-meta-card">
            {{ with .Params.status }}
            <div class="meta-row">
                <span class="status-dot status-{{ . }}"></span>
                <span>{{ . | title }}</span>
            </div>
            {{ end }}
            <div class="meta-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <span>{{ .Date.Format "2006/01/02" }}</span>
            </div>
            {{ with .GetTerms "categories" }}
            <div class="meta-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                <span>{{ range $i, $t := . }}{{ if $i }}, {{ end }}<a href="{{ $t.RelPermalink }}">{{ $t.LinkTitle }}</a>{{ end }}</span>
            </div>
            {{ end }}
            {{ with .Params.tech }}
            <div class="meta-row meta-row-stacked">
                <strong class="meta-label">Tech</strong>
                <div class="tech-list">
                    {{ range $i, $t := . }}{{ if $i }}, {{ end }}<span>{{ . }}</span>{{ end }}
                </div>
            </div>
            {{ end }}
            {{ with .Params.repo }}
            <div class="meta-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                <a href="{{ . }}" rel="noopener">Repository</a>
            </div>
            {{ end }}
            {{ with .Params.demo }}
            <div class="meta-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M10 14L21 3"/><path d="M21 14v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7"/></svg>
                <a href="{{ . }}" rel="noopener">Live demo</a>
            </div>
            {{ end }}
            {{ with .Params.video }}
            <div class="meta-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
                <a href="{{ . }}" rel="noopener">Video</a>
            </div>
            {{ end }}
        </div>
        <hr class="sidebar-divider">

        <p class="toc-title">Table of Contents</p>
        {{ .TableOfContents }}
    </nav>

    <article class="article-body">
        <h1>{{ .Title }}</h1>
        {{ with .Params.subtitle }}<p class="subtitle">{{ . }}</p>{{ end }}
        {{ .Content }}
    </article>

    <aside class="article-sidebar-right">
        {{ with .Params.sidenotes }}
            {{ range . }}
                {{ if .quote }}
                    <div class="side-quote">
                        {{ .quote }}
                        {{ with .cite }}<cite>&mdash; {{ . }}</cite>{{ end }}
                    </div>
                {{ else }}
                    <div class="side-note">
                        {{ with .label }}<strong>{{ . }}</strong>{{ end }}
                        {{ .text }}
                    </div>
                {{ end }}
            {{ end }}
        {{ end }}
    </aside>

</div>
{{ end }}

{{ define "scripts" }}
{{ $js := resources.Get "js/toc.js" | js.Build | minify | fingerprint }}
<script src="{{ $js.RelPermalink }}" integrity="{{ $js.Data.Integrity }}" defer></script>
{{ end }}
```

- [ ] **Step 3: Verify build**

Run: `just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 4: Verify detail renders**

Run:
```bash
just start
sleep 2
curl -s http://127.0.0.1:1313/projects/mini-rag/ | grep -c 'class="project-meta-card"'
```
Expected: `1`

Run:
```bash
curl -s http://127.0.0.1:1313/projects/mini-rag/ | grep -c 'Back to projects'
```
Expected: `1`

Run:
```bash
curl -s http://127.0.0.1:1313/projects/touchtask/ | grep -c 'Live demo'
```
Expected: `1`

Run:
```bash
curl -s http://127.0.0.1:1313/projects/guard/ | grep -c 'Live demo'
```
Expected: `0` (guard has no demo URL, so row must be omitted)

- [ ] **Step 5: Stop server**

Run: `just stop`

- [ ] **Step 6: Commit**

```bash
git add layouts/projects/single.html
git commit -m "feat(projects): add detail template with project meta card"
```

---

## Task 5: Add CSS for status dots and project meta card

**Files:**
- Modify: `assets/css/main.css` (append at end)

- [ ] **Step 1: State expected result**

After this task, the three status dots render with their brand colors, and the project meta card has a stacked tech row with a small muted label.

- [ ] **Step 2: Append CSS block to `assets/css/main.css`**

Open `assets/css/main.css` and append the following at the very end of the file, after the existing responsive blocks:

```css

/* === PROJECTS === */

.status-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    margin-right: 8px;
    border-radius: 50%;
    background-color: #bbb;
    flex-shrink: 0;
}
.status-dot.status-active { background-color: #4a9a4a; }
.status-dot.status-archived { background-color: #999; }
.status-dot.status-experiment { background-color: #4a7aa0; }

.project-meta-card {
    margin-bottom: 20px;
}
.project-meta-card .meta-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.75rem;
    color: #777;
    margin-bottom: 8px;
}
.project-meta-card .meta-row svg {
    width: 14px;
    height: 14px;
    flex-shrink: 0;
    opacity: 0.5;
}
.project-meta-card .meta-row a {
    color: #555;
    transition: color 0.15s;
}
.project-meta-card .meta-row a:hover {
    color: #111;
    text-decoration: underline;
    text-decoration-color: #ccc;
    text-underline-offset: 3px;
}
.project-meta-card .meta-row-stacked {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
}
.project-meta-card .meta-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #999;
    font-weight: 600;
}
.project-meta-card .tech-list {
    font-size: 0.75rem;
    color: #666;
    line-height: 1.5;
}
```

- [ ] **Step 3: Verify build**

Run: `just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 4: Verify CSS bundles**

Run:
```bash
just build
grep -oE '\.status-dot\.status-active' public/**/*.css | head -1
```
Expected: a match containing `.status-dot.status-active`.

- [ ] **Step 5: Commit**

```bash
git add assets/css/main.css
git commit -m "style(projects): add status dots and project meta card styles"
```

---

## Task 6: Add archetype for future projects

**Files:**
- Create: `archetypes/projects.md`

- [ ] **Step 1: State expected result**

Running `hugo new projects/foo/index.md` produces a file with the full project front-matter skeleton.

- [ ] **Step 2: Create the file**

```markdown
---
title: "{{ replace .Name "-" " " | title }}"
subtitle: ""
description: ""
date: {{ .Date }}
draft: true
slug: "{{ .Name }}"
tech: []
categories: []
status: "active"
repo: ""
demo: ""
video: ""
featured: false
sidenotes: []
---

```

- [ ] **Step 3: Verify build still passes**

Run: `just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 4: Commit**

```bash
git add archetypes/projects.md
git commit -m "feat(projects): add archetype for scaffolding new project pages"
```

---

## Tasks 7–13: Replace placeholder bodies with case-study content

These seven tasks are structurally identical. Each writes the case-study body for one project, replacing the single placeholder line. The front matter stays as scaffolded in Task 2 — do not edit the front matter.

### Reference — writing guide highlights

From `/Users/flo/Developer/Blog/reference/writing-guide/writing-guide.md`:

- **Voice:** calm authority, technically fluent, systems-aware, subtly human. No hype, no moralising, no clickbait. Calibrated language.
- **Recommended lens for these case studies:** Decision Stack (Context → Tradeoffs → Decision). Engineering Lens (Problem → Principle → Practice) works for `guard` and `ai-guardrails`. Use the one that fits the project.
- **Length:** 600–1000 words per project (short-form case study; shorter than a full blog article).
- **Structure:** use `## ` headings so the TOC in the left sidebar populates. Aim for 3–5 body sections per project.
- **Evidence:** ground claims in what the project actually does. Link to the repo for code-level detail rather than pasting code blocks.

### Reference — project source material

Collected during brainstorming. These are factual starting points, not prose to transcribe:

- **mini-rag** — BM25 + FAISS + FastText embeddings + SQLite, all in-process. Reranking via cross-encoder (off by default). Ships an MCP server. Design principle: no individual delete; re-ingest from source folders. Runs locally, no cloud services. Repo: `https://github.com/florianbuetow/mini-rag`.
- **guard** — Go CLI. Changes file owner, group, and permissions; sets immutable flag. Uses a `.guardfile` to remember state. Interactive TUI with fuzzy search. Critical security note: the account running the AI agent must not have passwordless sudo. Unix-only (Linux, macOS, BSD). Repo: `https://github.com/florianbuetow/guard`.
- **agentic-news-generator** — Python pipeline: YouTube download → audio extraction → MLX Whisper transcription → topic segmentation via LLM → cross-video topic aggregation → article generation → Nuxt-rendered HTML newspaper. Includes hallucination detection for the transcription stage. Repo: `https://github.com/florianbuetow/agentic-news-generator`.
- **x-rag** — Production-grade multi-tenant RAG platform. Weaviate (vector) + OpenSearch (BM25) + Neo4j (graph) + Kafka (ingestion). Per-namespace isolation, HPA, Redis caching. Prometheus Four Golden Signals. Target p95 sub-100ms retrieval. Repo: `https://github.com/florianbuetow/x-rag`.
- **imap-mini-mcp** — Node/TypeScript MCP server. Reads, searches, moves, stars, drafts email via IMAP. Cannot send or delete (safety boundary). Works with Gmail, Outlook, Fastmail, ProtonMail Bridge. Good paired with speech-to-text for conversational inbox workflows. Repo: `https://github.com/florianbuetow/imap-mini-mcp`.
- **touchtask** — React/Vite client-side app. No server, no account: data lives in localStorage. Combines time blocks, habit tracking, pomodoro, and kanban. Live at `https://cracking-ai-engineering.com/touchtask/`. Video overview on YouTube. Repo: `https://github.com/florianbuetow/touchtask`.
- **ai-guardrails** — Copier templates for Python, Java, Go, Elixir, C++, Rust. Each template bundles: multi-step fail-fast CI, pre-commit hooks running full CI, custom Semgrep rules banning default values and type suppressions, an `AGENTS.md` with development conventions, a `justfile` for common tasks, and test infrastructure with coverage gates. Repo: `https://github.com/florianbuetow/ai-guardrails`.

### Task 7 template — mini-rag

**Files:**
- Modify: `content/projects/mini-rag/index.md` (body only, below the front matter)

- [ ] **Step 1: State expected result**

The project page at `/projects/mini-rag/` shows a 600–1000 word case-study body organised into 3–5 `##` sections, with calm authority voice, no README-style tables. The TOC in the left sidebar populates with the section headings.

- [ ] **Step 2: Replace the placeholder body**

Open `content/projects/mini-rag/index.md`. Keep the front matter unchanged. Replace the line `Placeholder body. Real case-study content lands in a later task.` with a case-study body using the Decision Stack lens (Context → Tradeoffs → Decision). Draw on the mini-rag source material above. Cover:

- Why a local-first hybrid search was the right shape (personal knowledge over a small-to-medium corpus, AI agents over MCP, offline usability).
- Tradeoffs considered: cloud embedding service vs. local FastText; Elasticsearch vs. Tantivy; dense-only vs. hybrid.
- Decisions that fall out: the no-individual-delete design principle, reranking off by default, config-driven behaviour.
- What this enables for an AI agent connecting over MCP.

Do not paste tables from the README. Prose, not catalogue.

- [ ] **Step 3: Verify build**

Run: `just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 4: Verify TOC populates**

Run:
```bash
just start
sleep 2
curl -s http://127.0.0.1:1313/projects/mini-rag/ | grep -c 'id="TableOfContents"'
```
Expected: `1`

Run:
```bash
curl -s http://127.0.0.1:1313/projects/mini-rag/ | grep -oE '<h2[^>]*>' | wc -l | tr -d ' '
```
Expected: `3` or greater (confirms at least three section headings rendered).

- [ ] **Step 5: Stop server**

Run: `just stop`

- [ ] **Step 6: Commit**

```bash
git add content/projects/mini-rag/index.md
git commit -m "content(projects): add mini-rag case study"
```

### Task 8 — guard

Same structure as Task 7, using `content/projects/guard/index.md`. Recommended lens: **Engineering Lens** (Problem → Principle → Practice). Cover: the failure mode where AI agents modify unrelated files; the principle (make the protection a capability the user can toggle without friction); the practice (Unix permissions + immutable flag + `.guardfile` state + interactive TUI). Address the passwordless-sudo safety constraint honestly — it is a real limitation. 600–1000 words. Same verification steps and commit form (message: `content(projects): add guard case study`).

### Task 9 — agentic-news-generator

Same structure as Task 7, using `content/projects/agentic-news-generator/index.md`. Recommended lens: **Decision Stack**. Cover: the pipeline as a series of agent-driven stages (download, transcribe, segment, aggregate, write, render); where LLMs help and where deterministic code is better (transcription hallucination detection is a good example); what was deliberately kept offline vs. model-dependent. 600–1000 words. Commit message: `content(projects): add agentic-news-generator case study`.

### Task 10 — x-rag

Same structure as Task 7, using `content/projects/x-rag/index.md`. Recommended lens: **Decision Stack**. Cover: why three retrieval backends instead of one; per-namespace isolation as a multi-tenancy primitive; the observability stance (Four Golden Signals, LLM-specific tracing); explicit scaling tradeoffs (storage backends scale independently; stateless API scales with HPA). This is the most infrastructure-heavy project — lean into the systems-thinking angle. 600–1000 words. Commit message: `content(projects): add x-rag case study`.

### Task 11 — imap-mini-mcp

Same structure as Task 7, using `content/projects/imap-mini-mcp/index.md`. Recommended lens: **Engineering Lens**. Cover: the problem (AI agents with useful context about your inbox without handing over send/delete authority); the principle (read and draft, but never an irreversible action); the practice (IMAP as a universal protocol; what maps cleanly to MCP tool calls and what does not). Mention the speech-to-text workflow as a real use case. 600–1000 words. Commit message: `content(projects): add imap-mini-mcp case study`.

### Task 12 — touchtask

Same structure as Task 7, using `content/projects/touchtask/index.md`. Recommended lens: **Decision Stack**. Cover: the choice to go fully client-side (no backend, no account, localStorage); what combining time blocks + pomodoro + habits + kanban in one UI costs in complexity and what it buys in daily practice; what was deliberately left out. Shorter is fine — this is a focused tool. Linking to the live demo and video is appropriate. 600–900 words. Commit message: `content(projects): add touchtask case study`.

### Task 13 — ai-guardrails

Same structure as Task 7, using `content/projects/ai-guardrails/index.md`. Recommended lens: **Engineering Lens**. Cover: the friction (AI-generated code passes type checks because suppressions and default values hide problems); the principle (treat the CI pipeline as the teaching signal the agent actually listens to); the practice (Copier templates, Semgrep rules banning suppressions, fail-fast justfile recipes, `AGENTS.md` as a rule book the agent reads). Six languages means noting what is universal vs. language-specific. 600–1000 words. Commit message: `content(projects): add ai-guardrails case study`.

---

## Task 14: End-to-end verification

**Files:** none modified.

- [ ] **Step 1: State expected result**

The site builds cleanly, all seven project URLs resolve with non-empty bodies, the main-nav `Projects` link is marked active when browsing under `/projects/`, filter pills render with Categories and Technology pills, and mobile breakpoints collapse correctly.

- [ ] **Step 2: Full build**

Run: `just clean && just ci-quiet`
Expected: `✓ All CI checks passed`

- [ ] **Step 3: List page check**

Run:
```bash
just start
sleep 2
curl -s http://127.0.0.1:1313/projects/ | grep -c 'class="post"'
```
Expected: `7`

- [ ] **Step 4: Detail pages check**

Run:
```bash
for slug in mini-rag guard agentic-news-generator x-rag imap-mini-mcp touchtask ai-guardrails; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:1313/projects/$slug/")
  printf "%-30s %s\n" "$slug" "$code"
done
```
Expected: every row ends in `200`.

- [ ] **Step 5: Nav active-state check**

Run:
```bash
curl -s http://127.0.0.1:1313/projects/ | grep -oE 'class="active"[^>]*>Projects'
```
Expected: one match.

- [ ] **Step 6: Filter pills render**

Run:
```bash
curl -s http://127.0.0.1:1313/projects/ | grep -c 'data-categories='
```
Expected: `7` (one per project).

Run:
```bash
curl -s http://127.0.0.1:1313/projects/ | grep -c 'data-tags='
```
Expected: `7`.

- [ ] **Step 7: Stop server**

Run: `just stop`

- [ ] **Step 8: Final commit if anything changed**

Run: `git status`
If clean, no commit needed. If anything was fixed during verification, stage and commit with message `fix(projects): verification follow-ups`.

---

## Self-review summary

- **Spec coverage:** Section 1 (goal) → Tasks 1–2, 7–13. Section 3.1 (list page) → Task 3. Section 3.2 (detail page) → Task 4. Section 3.3 (status colors) → Task 5. Section 4.1 (front-matter schema) → Task 2. Section 4.2 (page bundles) → Task 2. Section 5.1 (hugo.toml permalink) → Task 1. Section 5.2 (layouts) → Tasks 3, 4. Section 5.3 (CSS additions) → Task 5. Section 6 (seed content) → Tasks 2, 7–13. Section 7 (error cases — missing demo/video/status/tech) → Task 4 template uses `{{ with }}` guards that cover each case; Task 4 Step 4 explicitly verifies the `Live demo` omission path on `guard`. Section 8 (testing/verification) → Task 14. Section 9 (archetype) → Task 6.
- **Placeholder scan:** No "TBD", "TODO", "implement later", or "add appropriate X". Task 7 shows the full template; Tasks 8–13 reference Task 7's structure but restate the slug, recommended lens, content guidance, and commit message explicitly.
- **Type consistency:** Front-matter keys (`tech`, `categories`, `status`, `repo`, `demo`, `video`, `featured`, `subtitle`, `description`) used in Task 2 match those referenced in the templates in Tasks 3 and 4 and in the archetype in Task 6. `layouts/projects/articles.html` populates `data-tags` from `$p.Params.tech` and the list template renders `status-{{ . }}` using the literal status string — consistent with the CSS classes in Task 5 (`status-active`, `status-archived`, `status-experiment`).

---

**End of plan.**
