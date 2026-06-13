# Ticker News Article Formatting Guide

How to format ticker news items (`content/ticker/<YYYY-MM-DD>-<slug>/index.md`). For the general article rules that also apply here (dashes, sidenotes, zoomable images), see [`article-formatting.md`](article-formatting.md). For link, citation, and reference-list formatting (footnotes, the references/sources list, plain-list links, links that open in a new tab), see the [URL and References Formatting Guide](url-and-references-formatting-guide.md).

## Cross-post items (teasers)

A ticker item whose only job is to point at a full article (a teaser: an interview write-up, an essay announcement) carries no footnote citations, so it does **not** use the footnote reference list. Instead:

- **Body link to the article:** use a relative path with the link text `[Continue reading ...](/blog/<slug>/)`. Never write "Visit cracking-ai-engineering.com for the full article" or any wording that tells the reader to visit the site, the reader is already on cracking-ai-engineering.com, so naming it is redundant. For the same reason, never put the domain in link text.
- **Footer heading:** `## Links`, not `## References`, there are no citations to number, only links.
- **Links** under it: the link to the article and the `[Comment on LinkedIn](url)` link are **mandatory** (these two are the default; you may add more). For the article link, use the article's **entire** title as the link text, never a shortened version and no prefix: `[The complete article title goes here](/blog/<slug>/)`.
- **Before the post is live:** wrap the LinkedIn body line and the LinkedIn `Links` entry in HTML comments with a `TODO`; never invent the activity ID, the URL comes from the post file outside this repo.

### Example footer

```markdown
[Continue reading ...](/blog/<slug>/)

<!-- TODO: add the LinkedIn post URL once published (source it from the post file, do not invent the activity ID).
To comment or share please head on over to [LinkedIn](LINKEDIN_POST_URL)
-->

## Links

- [The complete article title goes here](/blog/<slug>/)
<!-- TODO: add the LinkedIn post URL once published (source it from the post file, do not invent the activity ID).
- [Comment on LinkedIn](LINKEDIN_POST_URL)
-->
```
