# Projects Section — Design Spec

**Date:** 2026-04-16
**Status:** Approved
**Scope:** Add a projects section to the Hugo blog: a list page at `/projects/` and individual detail pages for each portfolio project currently linked from `github.com/florianbuetow`.

---

## 1. Goal

Create a projects section that:

- Lists many showcase projects on `/projects/` with filtering by technology and category.
- Renders each project as an individual case-study page at `/projects/<slug>/`.
- Seeds the section with the seven projects listed on the GitHub profile README: `mini-rag`, `guard`, `agentic-news-generator`, `x-rag`, `imap-mini-mcp`, `touchtask`, `ai-guardrails`.
- Stays consistent with the existing blog/ticker visual language and the "Cracking AI Engineering" brand (calm authority, systems thinking, no hype).

## 2. Non-Goals

- No hero images, thumbnails, or screenshots on list or detail pages. The site has no image pattern anywhere else.
- No sort controls beyond `featured` pin-to-top and date descending.
- No pagination — 7–30 projects fits a single page.
- No DRY refactor of `layouts/blog/articles.html` and `layouts/ticker/articles.html` into a shared partial. Three small focused templates beat one conditional template.
- No automated sync from GitHub. Content is hand-written Markdown. (Front matter holds the repo URL; that is the only link between the two.)

## 3. Visual & UX Design

### 3.1 List page — `/projects/`

Reuses the existing 3-column grid (`200px | 1fr | 200px`) shared by header, blog list, and article pages.

- **Left column (meta)**: status indicator (colored dot — green `#4a9a4a` active, gray `#999` archived, blue `#4a7aa0` experiment), followed by the date. Uses existing `.post-meta` / `.meta-item` / `.meta-icon` styling, with the indicator styled via a new `.status-dot.status-<value>` class.
- **Center column (content)**: `<h2>` title linked to the detail page, `<h3>` subtitle, truncated description paragraph. Reuses existing `.post-content` styling.
- **Right column (filter sidebar)**: same pill filter UX as the blog list, with **Technology** and **Category** sections. Reuses `filter.js` without modification (relies on `data-categories` and `data-tags` attributes on each `.post` element).

No cards. No grid of tiles. Text-forward list with dividers, matching blog/ticker exactly.

### 3.2 Detail page — `/projects/<slug>/`

Reuses the 3-column article layout (`200px | 1fr | 200px`).

- **Left sidebar**: back link (to `/projects/`), a **Project meta card** (replaces the author card), and the table of contents. Project meta card contains:
  - Status badge (colored dot + label)
  - Date
  - Category
  - Tech stack (compact list of tags)
  - Repo link
  - Demo link (if present)
  - Video link (if present)
- **Center column**: free-form case-study body written in the brand voice. Body structure is the author's choice per project — the template only renders `.Content`. Recommended lens is Decision Stack (Context → Tradeoffs → Decision), but Engineering Lens or Basics But Better also fit. Not a README dump.
- **Right sidebar**: side notes / side quotes, using the existing `sidenotes` front-matter shortcode mechanism inherited from the default single template.

### 3.3 Status indicator colors

| Status       | Color      | Meaning                                                    |
|--------------|------------|------------------------------------------------------------|
| `active`     | `#4a9a4a`  | Currently maintained and used.                             |
| `archived`   | `#999`     | No longer maintained; kept for reference.                  |
| `experiment` | `#4a7aa0`  | Prototype or learning exercise; not polished for users.    |

Colors chosen to sit within the existing muted palette — no saturation spikes.

## 4. Data Model

### 4.1 Front-matter schema (per project)

```yaml
---
title: "MiniRAG"
subtitle: "Local hybrid search for your docs with MCP integration"
description: "One-line description used on the list page and in meta tags."
date: 2026-03-15
slug: mini-rag
tech: ["Python", "FastText", "FAISS", "Tantivy", "SQLite", "MCP"]
categories: ["Search & Retrieval"]
status: "active"          # active | archived | experiment
repo: "https://github.com/florianbuetow/mini-rag"
demo: ""                  # optional, omit if none
video: ""                 # optional, omit if none
featured: true            # pinned to top of list when true
---
```

Notes:

- `categories` is used (plural, matching existing Hugo taxonomy in `hugo.toml`) rather than a new `category` field. This reuses `[taxonomies]` wiring and the `filter.js` `data-categories` attribute path.
- `tech` is a per-project list rendered as `data-tags` on the list page so `filter.js` treats it as the tag filter dimension. (Existing filter.js reads `data-tags` under the "Tags" heading — a future cosmetic change can rename the heading to "Technology" without touching the data path.)
- `status`, `repo`, `demo`, `video`, `featured` are new project-specific params.

### 4.2 Content layout

Each project lives in a page bundle:

```
content/projects/
├── _index.md
├── mini-rag/
│   └── index.md
├── guard/
│   └── index.md
├── agentic-news-generator/
│   └── index.md
├── x-rag/
│   └── index.md
├── imap-mini-mcp/
│   └── index.md
├── touchtask/
│   └── index.md
└── ai-guardrails/
    └── index.md
```

Page bundles allow per-project assets later (diagrams, etc.) without restructuring.

## 5. Hugo Wiring

### 5.1 `hugo.toml`

Add permalink pattern so project URLs match blog/ticker:

```toml
[permalinks]
  blog = '/blog/:slug/'
  ticker = '/ticker/:slug/'
  projects = '/projects/:slug/'
```

No other config changes. The menu entry for Projects already exists.

### 5.2 New layout files

- `layouts/projects/articles.html` — list template. Structurally identical to `layouts/blog/articles.html`, with three differences:
  1. Meta column renders a `.status-dot` span instead of the generic `.meta-icon` for the status indicator.
  2. `data-tags` is populated from `$p.Params.tech` (not `$p.Params.tags`).
  3. `featured: true` posts are sorted to the top before the date-descending sort.
- `layouts/projects/single.html` — detail template. Structurally mirrors `layouts/_default/single.html`, with the author card in the left sidebar replaced by a **Project meta card** that renders status, date, category, tech stack, repo link, demo link, video link.

### 5.3 CSS additions

Add the following to `assets/css/main.css` under a `/* === PROJECTS === */` section:

- `.status-dot` base class: 10px circle, same box size as `.meta-icon`.
- `.status-dot.status-active { background: #4a9a4a; }`
- `.status-dot.status-archived { background: #999; }`
- `.status-dot.status-experiment { background: #4a7aa0; }`
- `.project-meta-card` styles for the detail sidebar card (matches `.author-card` spacing; no avatar).
- `.project-meta-card .tech-list` — small inline list of tech tags (muted gray, comma-separated or pill-style with existing `.pill` class).
- `.project-meta-card a` — same muted color treatment as existing `.meta-row a`.

No changes to existing blog/ticker styles.

## 6. Seed Content — 7 Projects

Each project page uses the front-matter schema above and a case-study body following the writing guide. The README content gathered during brainstorming is the source material but is not transcribed verbatim — each page is written in the brand voice.

| Slug | Title | Subtitle | Categories | Tech | Status | Notes |
|------|-------|----------|------------|------|--------|-------|
| `mini-rag` | MiniRAG | Local hybrid search for your docs with MCP integration | Search & Retrieval | Python, FastText, FAISS, Tantivy, SQLite, MCP | active | Featured |
| `guard` | Guard | File guarding against unwanted AI coding agent modifications | Developer Tooling | Go, CLI, Unix permissions | active | |
| `agentic-news-generator` | Agentic News Generator | AI-agent-driven newspaper from curated YouTube channels | AI Agents | Python, MLX Whisper, Nuxt, LLMs | active | |
| `x-rag` | X-RAG | Distributed search and indexing for RAG at scale | Search & Retrieval | Python, Weaviate, OpenSearch, Neo4j, Kafka, Kubernetes | active | Featured |
| `imap-mini-mcp` | IMAP Mini MCP | MCP server that lets AI agents read and organise your inbox | MCP & Integrations | Node.js, TypeScript, IMAP, MCP | active | |
| `touchtask` | TouchTask | Time blocks, habits, and focused work sessions in one interface | Productivity | React, Vite, localStorage | active | Has demo + video |
| `ai-guardrails` | AI Guardrails | Project templates with built-in guardrails for AI coding agents | Developer Tooling | Copier, Python, Java, Go, Elixir, C++, Rust | active | |

`date` on each project corresponds to its most recent significant milestone (TBD per project by the author, based on repo history).

## 7. Error Cases & Edge Behavior

- **Missing `status`**: list page shows no dot; detail sidebar omits the status row.
- **Missing `demo` / `video`**: detail sidebar omits those rows. `{{ with .Params.demo }}...{{ end }}` guards each.
- **Missing `tech`**: list page has no tag data attributes; filter sidebar simply shows fewer Technology pills. No error.
- **Unknown `status` value**: rendered with base `.status-dot` only (no color class). Visible as a neutral dot.
- **Featured with no date**: treated as date `0001-01-01` by Hugo; still sorted to top of featured group. Not a concern if all projects have dates.
- **Empty section**: if all projects are deleted, list page falls back to the `.no-results` message via existing filter.js logic.

## 8. Testing / Verification

Since this is a static Hugo site with no test suite, verification is manual:

1. `just ci-quiet` — build passes with no warnings.
2. `just dev` — visually inspect:
   - `/projects/` — list renders 7 entries, filter pills appear, clicking pills filters correctly.
   - Each `/projects/<slug>/` — detail renders, sidebar meta card shows correct values, TOC works, back link returns to list.
   - Mobile breakpoint (`<900px`, `<768px`) — layout collapses cleanly as existing blog/ticker pages do.
3. Main menu "Projects" link resolves to `/projects/`.

## 9. Out of Scope for This Spec

- Future project authoring: a Hugo archetype at `archetypes/projects.md` with the front-matter skeleton is nice-to-have but not required for v1. Can be added later without changing this spec.
- Content authoring for the 7 case-study bodies is covered by the implementation plan, not by this spec. The spec defines the schema and layout; the plan will handle the writing task.

---

**End of spec.**
