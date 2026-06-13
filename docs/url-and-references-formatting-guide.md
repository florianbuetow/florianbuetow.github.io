# URL and References Formatting Guide

How to format links, citations, and reference lists across all blog content (blog posts, ticker items, project pages). The [article guide](article-formatting.md) and the [ticker news guide](tickernews-formatting.md) both defer to this document for these rules.

For broader conventions (file layout, build commands, when to use `slug`), see `CLAUDE.md`.

---

## 1. Citations

Articles cite sources with Markdown footnotes: an inline marker at each claim in the body, and a matching definition in the reference list at the foot of the article. This is the standard for every article's references. (The `resources` shortcode, documented at the end of this guide, renders a source table and stays available for the [resources](/resources/) page and other tabular lists, but footnotes are the default for article references.)

### Inline citations

Put a footnote marker `[^label]` in the body immediately after the claim it supports, with no space before it. `label` is a short mnemonic such as `metr` or `dora`, not a number. Hugo numbers the references automatically, in order of first appearance.

```markdown
A controlled trial found experienced engineers about 19 percent slower with AI on a mature codebase.[^metr]
```

When one sentence rests on two sources, stack the markers with no space between them:

```markdown
The pressure does not depend on AI actually being faster, which the evidence says it is not.[^metr][^dora]
```

### The reference list

Close the article with this block, in this order:

1. A `[Comment on LinkedIn](url)` link.
2. A `## References` (or `## Sources`) heading.
3. One footnote definition per source, each on its own line: `[^label]: Description. URL`.

```markdown
[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:XXXXXXXXXXXXXXXXXXXX/)

## References

[^metr]: METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developers," a randomized trial finding experienced developers about 19 percent slower with AI despite feeling faster. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
[^dora]: DORA, 2024 Accelerate State of DevOps Report, finding that AI amplifies a team's existing strengths and weaknesses rather than delivering a uniform gain. https://dora.dev/research/2024/dora-report/
```

Hugo renders the definitions as a numbered list under the heading, each with a back-link to its citation in the body. Order the definitions to match first use in the body, so the source and the rendered numbering stay easy to cross-check while editing.

### Notes

- Write each definition as a phrase naming the publisher and title, then why it is cited, then the bare URL last. Use a bare URL, not a `[label](url)` link, inside footnote definitions; this matches the existing articles.
- The divider line Hugo (Goldmark) inserts above the footnote list is hidden site-wide by a `.footnotes hr { display: none; }` rule in `assets/css/main.css`, so the heading sits directly above the list. Do not add it back per article.
- Use `## References` for ticker articles and `## Sources` for longer essays. Both are accepted; pick one and stay consistent within the article.
- The LinkedIn URL must come from the actual LinkedIn post file outside this repo. Don't invent activity IDs.
- Nothing should follow the reference list. It is the article's footer.

---

## 2. Plain-list reference links

When a `## References` or `## Resources` section uses a plain Markdown list instead of footnotes (common in ticker articles and project pages), every entry **must** follow this format:

```
Description [Page](url)
```

- **Description** is plain text naming the source context (publisher, tool name, person, document type).
- **Page** is the clickable label for the link.
- For internal links (articles, project pages on this site), use the prefix `Article:` and the full title as the link label: `Article: [Full Article Title](/blog/<slug>/)`.
- Never put prepositions like "on" inside the link label (`[on GitHub]` is wrong; `[GitHub]` is correct).
- Never use `**bold**` or other Markdown formatting inside reference list entries.

```markdown
## References

- Guard CLI [GitHub](https://github.com/florianbuetow/guard)
- Paul Buetow [on LinkedIn](https://www.linkedin.com/in/paul-buetow-b4857270/)
- Article: [Yes, You Are Absolutely Right!](/blog/yes-you-are-absolutely-right/)
```

---

## 3. The `resources` shortcode

`{{< resources >}}` renders a two-column source table. It powers the dedicated [resources](/resources/) page and stays valid where a tabular source list reads better than footnotes, but it provides no inline citation markers, which is why footnotes are the default for article references.

```markdown
## Sources

{{< resources >}}
[Descriptive label for the source](https://example.com/path) | What this source is and why it is cited.
[Another source, what it is](https://example.com/other) | One-sentence description of the source.
{{< /resources >}}
```

- One row per non-empty line inside the shortcode body.
- Each row has two cells separated by a single `|` character: the link on the left, the description on the right.
- Both cells accept inline Markdown. The link cell is always wrapped in `<strong>` by the template, so write a plain `[label](url)`, not `**[label](url)**`.
- The shortcode emits a `<table class="resources-table">`. The same CSS class powers the dedicated [resources](/resources/) page, so the appearance stays consistent across the site.
- Every `<a>` in the rendered table is emitted with `target="_blank" rel="noopener"`, so all reference links open in a new tab by default. You do not need to write the anchor by hand to get this behaviour.
- A row with zero or more than one `|` is a hard error. The build will fail with `resources shortcode: expected exactly one \`|\` per row`.
- Do not hand-write an HTML `<table>` block for sources. Use the `resources` shortcode so the markup stays in one place.

---

## 4. Links that open in a new tab

Markdown's `[text](url)` syntax has no way to set `target="_blank"`. Use a raw HTML anchor instead. This works because `markup.goldmark.renderer.unsafe = true` is set in `hugo.toml`.

```markdown
<a href="https://example.com" target="_blank" rel="noopener">link text</a>
```

Use `rel="noopener"` whenever you set `target="_blank"`, which prevents the opened page from accessing `window.opener`.
