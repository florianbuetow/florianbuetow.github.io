# Blog conventions

## Best practices

- Use `just` for all build and preview commands — never call `hugo` directly
- Before editing an article, read the file first to understand its current structure
- LinkedIn post URLs live outside this repo — always source URLs from the LinkedIn post files, never guess
- Never delete content before a replacement is ready and the build succeeds
- If a ticker article title contains a `/` (e.g. `/dream`, `/fixclaude`), add an explicit `slug` field in the front matter — Hugo treats the slash as a path separator, creating a broken URL

## Content structure

### Ticker articles

End every ticker article with this structure (in order):

1. `[Comment on LinkedIn](url)` — link to the LinkedIn post where readers can comment
2. `## References` heading
3. Bullet list of references with descriptive link text

Example:

```markdown
[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:XXXX/)

## References

- [Descriptive label](https://example.com)
```

### Blog articles

Same structure — comment link comes before the `## Sources` / `## References` section.

<!-- progressive-disclosure:index:start -->
## Documentation Index

### Introduction
- For prerequisites, install steps, and how to build/preview the blog locally, see [`README.md`](README.md)
- For the `tools/` Python sub-project (autotag and description-rewriting utilities), see [`tools/README.md`](tools/README.md)

### Architecture
- For the Projects section design spec, see [`docs/superpowers/specs/2026-04-16-projects-section-design.md`](docs/superpowers/specs/2026-04-16-projects-section-design.md)

### Development
- When authoring or editing article content — Mermaid diagrams, sidenotes, zoomable images, the closing References section — see [`docs/article-formatting.md`](docs/article-formatting.md)
- For the Projects section implementation plan, see [`docs/superpowers/plans/2026-04-16-projects-section.md`](docs/superpowers/plans/2026-04-16-projects-section.md)
- For autotag-tool technique and research notes (used by the Python sub-project), see [`tools/docs/autotag.md`](tools/docs/autotag.md)

### Appendix
- For research notes on automated blog-post tagging methods (NLI zero-shot, LLM prompting, TnT-LLM), see [`research_automated_blog_post_tagging.md`](research_automated_blog_post_tagging.md)
<!-- progressive-disclosure:index:end -->
