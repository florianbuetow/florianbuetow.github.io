# Article Formatting Guide

How to format article content in this blog. Covers: dashes (global style rule), the references section, Mermaid diagrams, and sidenotes.

For broader conventions (file layout, build commands, when to use `slug`), see `CLAUDE.md`.

---

## 1. Dashes

**Never use em dashes (`—`), en dashes (`–`), or any other Unicode dash character anywhere in article content.** The only dash character allowed in this repo is the ASCII hyphen-minus (`-`).

This rule applies to:

- All article prose (`content/blog/`, `content/ticker/`, `content/projects/`, `content/about.md`, top-level pages).
- Front-matter strings (titles, descriptions, subtitles).
- Headings, list items, and link labels.
- Comments inside fenced code blocks (the code itself can use whatever the language requires).
- Layout files (`layouts/`) that produce text the reader will see, including shortcode templates.

### Forbidden characters

| Character | Name | Codepoint |
|---|---|---|
| `—` | Em dash | U+2014 |
| `–` | En dash | U+2013 |
| `‒` | Figure dash | U+2012 |
| `―` | Horizontal bar | U+2015 |
| `−` | Minus sign | U+2212 |

### How to replace

Do NOT blindly substitute every em dash with an ASCII hyphen. In almost every case the right replacement is a comma, period, or colon, not a hyphen. Decide based on what the dash is doing in the sentence:

| Role of the dash | Replace with |
|---|---|
| Strong pause or sentence break | Period (`.`) |
| Inserting a clause | A pair of commas (`, ... ,`) |
| Introducing a list or definition | Colon (`:`) |
| Setting off a parenthetical | Parentheses (`(...)`) |
| Compound modifier (e.g. `petabyte-scale`) | ASCII hyphen (`-`) |

### Why this rule exists

Unicode dashes have become a tell for AI-written text. Even when stylistically correct, an em dash inside a personal essay signals "machine wrote this" to a meaningful share of readers. Plain ASCII punctuation does the same work without the tell.

### Auditing a file

Search the file for the literal characters `—` and `–`. Anything you find is a violation. Replace each per the table above.

---

## 2. References section

Every article ends with the same closing block, in this order:

1. A `[Comment on LinkedIn](url)` link.
2. A `## References` (or `## Sources`) heading.
3. A bullet list of links, each with a descriptive label, never a bare URL.

### Template

```markdown
[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:XXXXXXXXXXXXXXXXXXXX/)

## References

- [Descriptive label for the source](https://example.com/path)
- [Another source, what it is](https://example.com/other)
```

### Notes

- The LinkedIn URL must come from the actual LinkedIn post file outside this repo. Don't invent activity IDs.
- Use `## References` for ticker articles and `## Sources` for longer essays. Both are accepted; pick one and stay consistent within the article.
- Use descriptive link text. Readers, screen readers, and search engines all benefit. `[Hugo docs on shortcodes](...)` beats `[link](...)` or `[https://gohugo.io/...](...)`.
- Nothing should follow the references list. The references block is the article's footer.

---

## 3. Mermaid diagrams

Mermaid is rendered client-side from a locally bundled package. The JS only loads on pages that actually contain a Mermaid block, so there's no cost on articles without one.

### How to write one

Use a fenced code block with the `mermaid` language tag. That's it. No shortcode needed.

````markdown
```mermaid
flowchart LR
    A[Agent proposes change] --> B[Guardrails fire]
    B --> C{Pass?}
    C -- no --> D[Agent reads failure]
    D --> A
    C -- yes --> E[Change committed]
```
````

### Notes

- Any Mermaid diagram type works (`flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram`, `gantt`, etc.). The renderer is the upstream Mermaid package.
- Use `<br/>` inside node labels for line breaks. Quote labels that contain spaces or special characters: `A["Some label<br/>with two lines"]`.
- Preview locally with `just dev`. Mermaid renders in-browser, so a saved file should refresh and show the diagram immediately.
- Don't paste an SVG export. The whole point of writing the diagram source is that it stays diffable.

---

## 4. Sidenotes and sidequotes

Two shortcodes float content into the right margin of the article column:

- `sidenote`: labelled aside (Note / Tip / See also / ...).
- `sidequote`: pull quote with an optional attribution.

Both are inline shortcodes. Place them immediately before the paragraph they should sit alongside.

### Sidenote

```markdown
{{< sidenote label="Note" >}}This framing technique is sometimes called persona prompting. Microsoft research suggests 10-15% accuracy gains on domain-specific benchmarks.{{< /sidenote >}}

The paragraph this sidenote attaches to goes here. The note floats into the right column next to it.
```

- `label` is optional but recommended. Conventional labels: `Note`, `Tip`, `See also`, `Caveat`, `Aside`.
- The body supports inline Markdown. Links, emphasis, code spans all work.
- Keep sidenotes short. One or two sentences. If it needs a paragraph, it belongs in the main text.

### Sidequote

```markdown
{{< sidequote cite="Marvin Minsky" >}}Constraints are the friend of creativity. They force you to think harder, not less.{{< /sidequote >}}

The paragraph the quote sits beside goes here.
```

- `cite` is optional. When present, it renders as an attribution line.
- **Known violation of the Dashes rule:** the sidequote shortcode template currently emits an em dash before the citation name. To bring it into compliance, edit `layouts/shortcodes/sidequote.html` to use an ASCII hyphen (or a colon, period, etc.) instead. Until that change ships, every sidequote on the site silently violates Section 1.
- Use sparingly. One or two per article. Sidequotes lose their effect when they stack.

### Placement rules

- One sidenote/sidequote per paragraph. Two in a row collide visually.
- Place the shortcode **before** the paragraph it should align with. Hugo renders it inline, and the CSS floats it.
- On narrow viewports the floated column collapses and the sidenote falls inline. Write the body so it reads naturally in both layouts.

---

## 5. Zoomable images

Append `?zoom` to any image path to make it clickable. Clicking the image opens a full-resolution lightbox overlay.

### Syntax

```markdown
![Alt text](image.webp?zoom "Optional title shown on hover")
```

### How it works

The render hook (`layouts/_default/_markup/render-image.html`) strips `?zoom` from the src, adds `class="zoomable"` and a `data-zoom-src` attribute pointing to the full-resolution file. `assets/js/lightbox.js` attaches the click handler; `assets/css/main.css` sets `cursor: zoom-in`.

### Notes

- Works with page-bundle images (most common) and external URLs alike.
- The title string becomes the `title` attribute on the `<img>` tag -- it appears as a browser tooltip, not a caption.
- Use for illustrations, screenshots, or any image where detail matters at full size. Skip it for decorative images.
- One zoom per paragraph is enough; don't stack multiple zoomable images side by side.

---

## Reference article

`content/blog/2026-05-17-yes-you-are-absolutely-right/index.md` uses Mermaid diagrams and the references section.
`content/blog/test-sidenotes.md` exists specifically to exercise the sidenote and sidequote shortcodes. Open it side-by-side with the rendered page when iterating.
