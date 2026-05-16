# hugo-blog

A custom Hugo static site with a hand-built theme (no third-party theme dependency). Layouts, CSS, and JS live directly in the project root — no `themes/` directory.

## Prerequisites

- [Hugo](https://gohugo.io/) extended edition (0.160+): `brew install hugo`
- [just](https://github.com/casey/just) command runner: `brew install just`

Verify installation:

```bash
just check
```

## Installation

### Go

Hugo Modules require Go. Install it from the [official Go installation page](https://go.dev/doc/install).

### Alternative: mise

[mise](https://mise.jdx.dev/) pins all tool versions for the project. With `.mise.toml` present at the repo root:

```bash
mise trust
mise install
```

This installs Hugo, just, and Go at the exact versions the project uses.

## Project structure

```
hugo-blog/
├── hugo.toml                    # Site config: title, menu, taxonomies, params
├── justfile                     # Task runner: start/stop server, build, ci
├── archetypes/
│   └── blog.md                  # Front-matter template for new blog posts
├── assets/
│   ├── css/
│   │   └── main.css             # All site styles (processed by Hugo Pipes)
│   └── js/
│       ├── filter.js            # Blog index: tag/category filter sidebar
│       └── toc.js               # Article: table-of-contents scroll spy
├── content/
│   ├── _index.md                # Home page
│   ├── about.md                 # About page
│   ├── blog/
│   │   ├── _index.md            # Blog section index
│   │   └── *.md                 # Blog posts (one file per post)
│   └── projects/
│       └── _index.md            # Projects section index
├── layouts/
│   ├── _default/
│   │   ├── baseof.html          # Shared page shell (header + footer)
│   │   ├── list.html            # Blog index + taxonomy list pages
│   │   └── single.html          # Article view (3-column layout)
│   ├── index.html               # Home page layout
│   ├── partials/
│   │   ├── head.html            # <head> meta, CSS include
│   │   ├── header.html          # Site header with nav + search box
│   │   └── footer.html          # Site footer with socials
│   └── shortcodes/
│       ├── sidenote.html        # {{< sidenote >}} inline note block
│       └── sidequote.html       # {{< sidequote >}} inline quote block
└── public/                      # Generated site output (gitignored)
```

### Key files

| File | Purpose |
|---|---|
| `hugo.toml` | Site title, menu entries, taxonomies, author, socials, permalink rules |
| `layouts/_default/baseof.html` | Outer HTML shell — shared header, footer, main region |
| `layouts/_default/single.html` | Article page with TOC, author card, and side notes |
| `layouts/_default/list.html` | Blog index + tag/category list pages with filter sidebar |
| `assets/css/main.css` | All styles — edit here, Hugo Pipes fingerprints and minifies |

## Running the site locally

Start the development server (backgrounded, with drafts enabled):

```bash
just start
```

The site is served at **http://127.0.0.1:1313**. Hugo watches files and hot-reloads on changes.

Check status:

```bash
just status
```

Stop the server:

```bash
just stop
```

## Adding a new blog article

### Option 1: Use the archetype (recommended)

```bash
hugo new content blog/my-new-post.md
```

This creates `content/blog/my-new-post.md` pre-filled from `archetypes/blog.md` with the correct front matter skeleton. The file is created as `draft: true` — flip to `false` when ready to publish.

### Option 2: Create the file manually

Create `content/blog/my-new-post.md` with front matter:

```markdown
---
title: "My New Post"
subtitle: "Optional one-line subtitle"
date: 2026-04-14
draft: false
author: "Florian Buetow"
readTime: "5 min read"
categories: ["Prompt Engineering"]
tags: ["prompts", "llm"]
sidenotes:
  - label: "Note"
    text: "A side note that renders in the right column of the article view."
  - quote: "Constraints are the friend of creativity."
    cite: "Marvin Minsky"
---

## First heading

Body text. Markdown, code blocks, lists, blockquotes — all supported.

You can also drop shortcodes inline for side notes inside the article body:

{{< sidenote label="Tip" >}}
This renders as a styled note block.
{{< /sidenote >}}

{{< sidequote cite="Author Name" >}}
An inline pull quote.
{{< /sidequote >}}
```

### Front-matter fields

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Post title |
| `subtitle` | no | Shown under the H1 on the article page |
| `date` | yes | Publication date (ISO format: `YYYY-MM-DD`) |
| `draft` | yes | `true` hides the post from production builds |
| `author` | no | Defaults to `site.Params.author` from `hugo.toml` |
| `readTime` | no | Free-text string, e.g. `"7 min read"` |
| `categories` | no | List — rendered as filter pills and taxonomy pages |
| `tags` | no | List — rendered as filter pills and taxonomy pages |
| `sidenotes` | no | List of `{label, text}` or `{quote, cite}` objects for the right column |

### Publishing workflow

1. Create the file with `draft: true`.
2. Run `just start` and preview at `http://127.0.0.1:1313/blog/`.
3. When ready, set `draft: false`.
4. Run `just build` to generate the production site into `public/`.

### URLs and slugs

By default the URL comes from the filename: `content/blog/my-new-post.md` → `/blog/my-new-post/`. Override by adding `slug: "custom-slug"` or `url: "/custom/path/"` to the front matter.

## Building the site

Generate the production site into `public/`:

```bash
just build
```

Run the full validation pipeline (currently `check` + `build`):

```bash
just ci
```

Clean build artifacts:

```bash
just clean
```

Wipe everything (artifacts + server state):

```bash
just destroy
```

## All `just` targets

```bash
just help
```

- **Setup & lifecycle:** `init`, `destroy`, `clean`, `check`, `help`
- **Run:** `start`, `stop`, `status`
- **CI & testing:** `build`, `ci`

## Configuration notes

- **Site title, author, socials** — edit `[params]` and `[params.socials]` in `hugo.toml`.
- **Navigation menu** — edit `[[menu.main]]` entries in `hugo.toml`.
- **Taxonomies** (tags, categories) — defined in `[taxonomies]`; Hugo auto-generates `/tags/<tag>/` and `/categories/<category>/` list pages.
- **baseURL** — currently `https://example.org/`. Update when deploying.

## Deployment

Not yet configured. The old blog remains the public site. A GitHub Pages workflow can be added later under `.github/workflows/` once deployment is desired.
