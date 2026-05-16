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
