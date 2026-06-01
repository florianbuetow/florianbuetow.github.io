# Stable URLs and Redirects

How to decouple article URLs from folder names, and how to redirect one URL to another.

---

## 1. Fixed slug

By default, Hugo derives the URL from the folder name. A post at `content/blog/2026-05-24-my-review/` gets the URL `/blog/2026-05-24-my-review/`.

Add `slug` to the front matter to override this:

```yaml
slug: "my-review"
```

The article then lives at `/blog/my-review/` regardless of the folder date prefix.

**When to use:** You want to share a stable URL before you know the publish date, or you want a clean URL without the date embedded. The URL only becomes live once the article is deployed (flipped from `draft: true` to `draft: false`).

---

## 2. Hugo aliases

Hugo's `aliases` front-matter field generates a static redirect HTML page at each listed path. Visitors to an alias URL are automatically redirected to the canonical article URL.

```yaml
aliases:
  - /blog/my-old-slug/
  - /blog/some-vanity-name/
```

Hugo writes a redirect page at each alias path, so both old and new URLs resolve after the next deploy.

**When to use:** An article moved (date prefix or slug changed) and you want to preserve inbound links. Or you want a short vanity URL pointing to a date-based canonical URL.

---

## Choosing between them

| Situation | Approach |
|---|---|
| You need to share a URL before the publish date is known | Fixed `slug` (omits date from URL) |
| Article moved or was renamed after publishing | `aliases` pointing from old URL to new canonical |
| You want a clean vanity URL alongside the date-based URL | `aliases` on the vanity path pointing to the canonical |

Note: neither approach makes the URL resolvable before the article is deployed. If the recipient needs the link to work immediately (before publishing), you would need a server-level redirect or a placeholder page in place first.
