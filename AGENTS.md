# Blog conventions

## Best practices

- Use `just` for all build and preview commands — never call `hugo` directly
- Before editing an article, read the file first to understand its current structure
- Run `just spell-check <file>` after editing a draft article to catch spelling and grammar issues before publishing; add legitimate false positives (proper names, technical terms) to `config/harper/dictionary.txt`
- Always run `just spell-check <file>` before flipping `draft: true` to `draft: false` — never publish without a passing spell check
- After editing any `.wtg2` file, run `just wardley-render` before committing — the generated `.svg` must travel with its source (`just build` and `just ci` re-render maps, so a stale `.svg` fails the `check-clean-worktree` gate)
- LinkedIn post URLs live outside this repo — always source URLs from the LinkedIn post files, never guess
- Never delete content before a replacement is ready and the build succeeds
- If a ticker article title contains a `/` (e.g. `/dream`, `/fixclaude`), add an explicit `slug` field in the front matter — Hugo treats the slash as a path separator, creating a broken URL

<!-- progressive-disclosure:index:start -->
## Documentation Index

### Introduction
- For prerequisites, install steps, and how to build/preview the blog locally, see [`README.md`](README.md)
- For the `tools/` Python sub-project (autotag and description-rewriting utilities), see [`tools/README.md`](tools/README.md)

### Architecture
- For the Projects section design spec, see [`docs/superpowers/specs/2026-04-16-projects-section-design.md`](docs/superpowers/specs/2026-04-16-projects-section-design.md)

### Development
- When authoring or editing article content — Mermaid diagrams, Wardley maps, sidenotes, zoomable images, the closing References section — see [`docs/article-formatting.md`](docs/article-formatting.md)
- When authoring or editing ticker news items — the "Continue reading" body link, the `## Links` footer, and the mandatory article + LinkedIn links — see [`docs/tickernews-formatting.md`](docs/tickernews-formatting.md)
- For the Open Source / Projects grid page — how to feature a project, sort order, the full-width hero layout, and the extended `long_description` field — see [`docs/projects-page-formatting.md`](docs/projects-page-formatting.md)
- For stable pre-publication URLs, fixed slugs, and redirect aliases — see [`docs/stable-urls.md`](docs/stable-urls.md)
- For autotag-tool technique and research notes (used by the Python sub-project), see [`tools/docs/autotag.md`](tools/docs/autotag.md)

### Appendix
- For research notes on automated blog-post tagging methods (NLI zero-shot, LLM prompting, TnT-LLM), see [`research_automated_blog_post_tagging.md`](research_automated_blog_post_tagging.md)
<!-- progressive-disclosure:index:end -->
