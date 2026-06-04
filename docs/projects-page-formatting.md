# Projects Page Formatting Guide

How the Open Source / Projects grid page (`/projects/`) renders project cards. Covers: where the pieces live, the front-matter fields that drive a grid card, sort order, how to feature a project (the full-width hero), and the extended `long_description` field.

This guide is about the **grid/listing page** (`layouts/projects/articles.html`), not the individual project page (`layouts/projects/single.html`). For article content conventions (sidenotes, images, Mermaid, the references section), see [`article-formatting.md`](article-formatting.md). For broader conventions (build commands, `slug`), see `CLAUDE.md`.

---

## 1. Where things live

| Piece | Path |
|---|---|
| Project content | `content/projects/<slug>/index.md` (one page bundle per project) |
| Section index | `content/projects/_index.md` (sets `layout: articles`) |
| Grid layout | `layouts/projects/articles.html` |
| Single project page | `layouts/projects/single.html` |
| Card styles | `assets/css/main.css` — `.project-grid`, `.project-card`, `.project-card-featured` |
| New-project archetype | `archetypes/projects.md` |

Each project is a page bundle: a directory under `content/projects/` holding an `index.md` and its image asset. Preview the grid at `http://127.0.0.1:1313/projects/`.

---

## 2. Front-matter fields that drive the grid card

These fields control how a project appears **in the grid**. Other front-matter fields (`slug`, `repo`, `demo`, `video`, `sidenotes`) belong to the single project page and do **not** affect the card.

| Field | Type | Effect on the card |
|---|---|---|
| `title` | string | Card heading (linked). On a featured card it is prefixed with `Featured Project: `. |
| `subtitle` | string | Secondary line under the heading. |
| `description` | string | Body copy on a normal card. Also the fallback for a featured card. |
| `long_description` | string | Body copy on a **featured** card (see §5). Optional. |
| `date` | `YYYY-MM-DD` | Sort key, and the `Mon YYYY` value in the card meta line. Set manually. |
| `status` | string | Title-cased and shown before the date in the meta line (e.g. `Active`). |
| `tech` | list | Rendered as a `·`-joined list in the card footer. |
| `image` | path | Card image, e.g. `/projects/open-source-images/<name>.webp`. Optional. |
| `featured` | bool | `true` promotes the project to the full-width hero (see §4). |
| `categories`, `tags` | list | Emitted as `data-categories` / `data-tags` attributes on the card element; not shown as visible text. |
| `draft` | bool | `true` hides the project from production builds (visible under `just start`). |

> **Not in the archetype.** `image` and `long_description` are absent from `archetypes/projects.md`, so a project scaffolded with `hugo new content projects/<name>` won't have them. Add them by hand when you need a card image or a featured hero.

---

## 3. Sort order

Projects are sorted by `date`, newest first, in two groups:

1. **Featured** projects (`featured: true`), newest first.
2. **Everything else**, newest first.

The template builds that order with `.ByDate.Reverse`:

```go-html-template
{{ $featured := (where $all "Params.featured" true).ByDate.Reverse }}
{{ $rest := (where $all "Params.featured" "!=" true).ByDate.Reverse }}
{{ $posts := $featured | append $rest }}
```

So any featured project comes first (as a full-width hero), then the normal grid follows in date order.

To re-order projects, change their `date`. The date is yours to set — it does not need to match the file's creation time or git history.

---

## 4. Featuring a project

Set `featured: true` in the project's front matter. That does three things:

1. **Promotes it to a full-width hero** at the top of the page. The card spans all three grid columns (`grid-column: 1 / -1`) and switches to a horizontal layout: **image on the left (2 columns wide), text on the right (1 column wide)**. The 2:1 split is `flex: 2` on `.project-card-featured .project-card-image` against the body's `flex: 1` in `main.css`.
2. **Top-aligns the text** beside the image (`align-items: flex-start`), with a left-border accent.
3. **Prefixes the heading** with `Featured Project: ` (e.g. `Featured Project: Memento`). This prefix is hardcoded in `layouts/projects/articles.html` — change the wording there.

A featured card also swaps its body copy to `long_description` when present (see §5).

### One hero at a time

The hero layout assumes a **single** featured project. If you set `featured: true` on more than one, each becomes its own full-width hero, stacked above the normal grid in date order. That renders without breaking, but it is rarely what you want — feature one project at a time.

### Responsive behaviour

- **> 900px** — 3-column grid; hero is the horizontal 2:1 image/text layout.
- **≤ 900px** — grid drops to 2 columns; the hero still spans full width and stays horizontal.
- **≤ 600px** — grid is a single column; the hero **stacks**: full-width image on top, text below.

---

## 5. The extended description (`long_description`)

A normal card shows `description`. A featured card shows `long_description` instead — a longer paragraph that fills the wider hero.

```yaml
description: "One-line summary used on the normal card and for SEO."
long_description: "A longer paragraph shown only when this project is the featured hero. Use the extra room the hero gives you to tell the fuller story."
```

Rules:

- `long_description` renders **only** on a featured card. On a normal card it is ignored.
- If a featured project has no `long_description`, the hero falls back to `description`.
- Keep `description` set regardless — it is the fallback and is still used on every non-featured card.

The template logic:

```go-html-template
{{ if and .Params.featured .Params.long_description }}<p class="card-desc">{{ .Params.long_description }}</p>{{ else }}{{ with .Params.description }}<p class="card-desc">{{ . }}</p>{{ end }}{{ end }}
```

---

## 6. Reference example

`content/projects/memento/index.md` is set up as the featured hero: it has `featured: true`, an `image`, and a `long_description`. Open `/projects/` side-by-side with that file to see how each field maps onto the hero card.
