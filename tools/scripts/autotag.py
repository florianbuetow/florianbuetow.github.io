"""Two-phase blog post tagger using a local LM Studio model.

Phase 1: Generate a tag taxonomy from a sample of blog posts.
Phase 2: Assign tags from that taxonomy to every post.

Output files (in data/output/):
  taxonomy.json     — generated tag taxonomy; review/edit before Phase 2
  suggestions.json  — per-post tag suggestions; review before applying

Usage:
    uv run scripts/autotag.py                    # full pipeline
    uv run scripts/autotag.py --phase1-only      # taxonomy generation only
    uv run scripts/autotag.py --phase2-only      # tag posts using existing taxonomy.json
    uv run scripts/autotag.py --apply            # write tags back to frontmatter
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from openai import OpenAI

# ---------------------------------------------------------------------------
# Paths (all derived from this file's location — tools/scripts/autotag.py)
# ---------------------------------------------------------------------------
_TOOLS_DIR = Path(__file__).parent.parent
_CONTENT_DIR = _TOOLS_DIR.parent / "content"
_OUTPUT_DIR = _TOOLS_DIR / "data" / "output"
TAXONOMY_FILE = _OUTPUT_DIR / "autotag_taxonomy.json"
SUGGESTIONS_FILE = _OUTPUT_DIR / "autotag_suggestions.json"

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
LM_STUDIO_URL = "http://localhost:1234/v1"
TAXONOMY_MODEL = "google/gemma-4-26b-a4b"
LABELING_MODEL = "google/gemma-4-26b-a4b"
PHASE1_SAMPLE_SIZE = 30
MAX_CONTENT_CHARS = 2000
MAX_TAGS_PER_POST = 3
TEST_TITLE_PREFIX = "TEST:"

# Company / vendor names that must never appear as tags. Use product-level
# names (e.g. "Claude Code") instead when a product is genuinely the subject.
BANNED_TAGS: frozenset[str] = frozenset(
    {
        "Anthropic",
        "OpenAI",
        "Google",
        "Meta",
        "Microsoft",
        "Mistral",
    }
)

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------
type Frontmatter = dict[str, Any]
type TagEntry = dict[str, str]  # {"name": ..., "description": ...}
type Suggestion = dict[str, Any]


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[Frontmatter, str]:
    """Split YAML frontmatter from markdown body.

    Args:
        text: Full markdown file content.

    Returns:
        Tuple of (frontmatter dict, body string). Frontmatter is empty dict
        when no valid YAML block is found.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    parsed = yaml.safe_load(text[3:end])
    fm: Frontmatter = parsed if isinstance(parsed, dict) else {}
    return fm, text[end + 4 :]


def serialize_frontmatter(meta: Frontmatter, body: str) -> str:
    """Reconstruct a markdown file from frontmatter dict and body.

    Args:
        meta: Frontmatter key-value pairs.
        body: Markdown body (everything after the closing ---).

    Returns:
        Full file content as string.
    """
    fm_yaml = yaml.dump(meta, allow_unicode=True, default_flow_style=False).strip()
    return f"---\n{fm_yaml}\n---{body}"


# ---------------------------------------------------------------------------
# Post collection
# ---------------------------------------------------------------------------
def collect_posts(content_dir: Path) -> list[Frontmatter]:
    """Collect all published posts from a Hugo content directory.

    Args:
        content_dir: Path to the Hugo content/ directory.

    Returns:
        List of post dicts with keys: path, title, description,
        current_tags, current_categories, body.

    Raises:
        SystemExit: If content_dir does not exist.
    """
    if not content_dir.exists():
        print(f"[ERROR] Content directory not found: {content_dir}", file=sys.stderr)
        sys.exit(1)

    posts: list[Frontmatter] = []
    for path in sorted(content_dir.rglob("*.md")):
        if path.name == "_index.md":
            continue
        # Skip top-level pages like about.md, newsletter.md, resources.md —
        # they are site navigation, not articles.
        if path.parent == content_dir:
            continue
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        if meta.get("draft"):
            continue
        # Skip test fixtures.
        if str(meta.get("title", "")).startswith(TEST_TITLE_PREFIX):
            continue
        posts.append(
            {
                "path": str(path),
                "title": meta.get("title", ""),
                "description": meta.get("description", ""),
                "current_tags": meta.get("tags", []),
                "current_categories": meta.get("categories", []),
                "body": body.strip()[:MAX_CONTENT_CHARS],
            }
        )
    return posts


def post_summary(post: Frontmatter, include_body: bool = True) -> str:
    """Build a compact text summary of a post for LLM prompts.

    Args:
        post: Post dict from collect_posts.
        include_body: If False, skip the body excerpt — tag from title+description only.

    Returns:
        Multi-line string with title, description, and optionally a content excerpt.
    """
    parts: list[str] = []
    if post["title"]:
        parts.append(f"Title: {post['title']}")
    if post["description"]:
        parts.append(f"Description: {post['description']}")
    if include_body and post["body"]:
        parts.append(f"Content excerpt:\n{str(post['body'])[:800]}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Phase 1: taxonomy generation
# ---------------------------------------------------------------------------
def generate_taxonomy(client: OpenAI, posts: list[Frontmatter], model: str) -> list[TagEntry]:
    """Generate a tag taxonomy from a sample of posts using an LLM.

    Args:
        client: Configured OpenAI-compatible client.
        posts: All collected posts (first PHASE1_SAMPLE_SIZE are used).
        model: LM Studio model ID to use.

    Returns:
        List of tag dicts, each with "name" and "description" keys.

    Raises:
        SystemExit: On JSON parse failure or unexpected response structure.
    """
    sample = posts[:PHASE1_SAMPLE_SIZE]
    existing_tags: list[str] = sorted({t for p in posts for t in p["current_tags"]})
    posts_block = "\n\n---\n\n".join(post_summary(p) for p in sample)
    existing_block = ", ".join(existing_tags) if existing_tags else "(none)"

    banned_block = ", ".join(sorted(BANNED_TAGS))
    prompt = f"""You are helping build a tag taxonomy for a professional technical blog
about AI engineering, software tools, and developer productivity.

Existing tags already in use: {existing_block}

Below are {len(sample)} blog posts. Analyze them and produce a clean taxonomy of 15-25 tags
that covers the full topic space of this blog. Incorporate and refine the existing tags —
keep useful ones, merge duplicates, add missing ones.

Hard rules on tag NAMES:
- Short: 1-2 words. Never more than 3 words.
- No parentheses, no acronym expansions. Use the bare acronym: "MCP", "RAG", "SRE".
- No compound "X & Y" names unless both words are needed for disambiguation.
- Title Case. No trailing punctuation.
- Never propose company or vendor names as tags: {banned_block}.
  Use product-level names only when a specific product is genuinely the subject
  of multiple posts (e.g. "Claude Code" for the CLI, not "Anthropic").

Hard rules on DESCRIPTIONS:
- Each description MUST end with an explicit "Do not apply" clause stating when
  the tag should not be used, so boundaries are clear.
- Tags must be topically disjoint — if two descriptions overlap, rewrite one.

Coverage rules:
- Cover every concrete domain that appears in the posts. If multiple posts cover
  a programming language (e.g. Rust) or a specific platform (e.g. Email/IMAP),
  include a tag for it.
- Favor sharp, narrow tags over broad catch-alls, but do not drop domains that
  the posts actually cover.

Return ONLY valid JSON in this exact format:
{{
  "tags": [
    {{"name": "Claude Code", "description": "Articles about the Claude Code CLI, plugins, and commands. Do not apply to generic agentic coding posts."}},
    ...
  ]
}}

Blog posts:
---
{posts_block}
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    raw = resp.choices[0].message.content or ""
    raw = re.sub(r"^```[a-z]*\n?", "", raw.strip())
    raw = re.sub(r"\n?```$", "", raw)

    try:
        data: dict[str, Any] = json.loads(raw)
        tags: list[TagEntry] = data["tags"]
    except (json.JSONDecodeError, KeyError) as exc:
        print(f"[ERROR] Failed to parse taxonomy JSON: {exc}", file=sys.stderr)
        print(f"Raw response:\n{raw}", file=sys.stderr)
        sys.exit(1)

    # Strip any banned tags the model produced despite instructions.
    filtered: list[TagEntry] = []
    removed: list[str] = []
    for t in tags:
        name = str(t.get("name", "")).strip()
        if name in BANNED_TAGS:
            removed.append(name)
            continue
        filtered.append(t)
    if removed:
        print(f"  [INFO] Dropped banned tags from taxonomy: {', '.join(removed)}", file=sys.stderr)
    return filtered


# ---------------------------------------------------------------------------
# Phase 2: post labeling
# ---------------------------------------------------------------------------
def assign_tags(client: OpenAI, post: Frontmatter, taxonomy: list[TagEntry], model: str, include_body: bool = True) -> list[str]:
    """Assign tags from the taxonomy to a single post using an LLM.

    Args:
        client: Configured OpenAI-compatible client.
        post: Post dict from collect_posts.
        taxonomy: Full tag taxonomy from Phase 1.
        model: LM Studio model ID to use.
        include_body: If False, tag from title+description only (simulates tldr-based tagging).

    Returns:
        List of tag name strings (subset of taxonomy names).
        Returns empty list on parse failure (with warning to stderr).
    """
    tag_list = "\n".join(f"- {t['name']}: {t['description']}" for t in taxonomy)
    content = post_summary(post, include_body=include_body)

    prompt = f"""You are tagging a blog post for a professional technical blog.
Tag quality matters more than tag count — a wrong tag is worse than a missing one.

Available tags (name: description):
{tag_list}

Blog post:
{content}

Rules:
- Return between 1 and {MAX_TAGS_PER_POST} tag names — the minimum that accurately describes the post.
- Only return a tag when the post is clearly about that topic. Respect each tag's "do not apply" guidance.
- Do not pad the list to reach the maximum. Fewer, sharper tags are preferred.
- Order tags from most to least central to the post.
- Choose only from the available tags above.

Return ONLY a JSON array. Example: ["Claude Code", "MCP"]
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    raw = resp.choices[0].message.content or ""
    raw = re.sub(r"^```[a-z]*\n?", "", raw.strip())
    raw = re.sub(r"\n?```$", "", raw)

    match = re.search(r"\[.*?\]", raw, re.DOTALL)
    if not match:
        print(f"  [WARN] No JSON array for '{post['title']}' — skipping", file=sys.stderr)
        return []

    try:
        result: list[str] = json.loads(match.group())
    except json.JSONDecodeError:
        print(f"  [WARN] Bad JSON for '{post['title']}': {raw[:80]}", file=sys.stderr)
        return []

    valid_names = {t["name"] for t in taxonomy}
    cleaned: list[str] = []
    for name in result:
        if name in BANNED_TAGS:
            continue
        if name not in valid_names:
            continue
        if name in cleaned:
            continue
        cleaned.append(name)
    return cleaned[:MAX_TAGS_PER_POST]


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------
def apply_suggestions(suggestions: list[Suggestion]) -> None:
    """Write suggested tags into each file's YAML frontmatter.

    Args:
        suggestions: List of suggestion dicts from Phase 2 output.

    Raises:
        SystemExit: If a post file cannot be read or written.
    """
    for s in suggestions:
        path = Path(str(s["path"]))
        if not path.exists():
            print(f"[ERROR] Post file not found: {path}", file=sys.stderr)
            sys.exit(1)
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        meta["tags"] = s["suggested_tags"]
        path.write_text(serialize_frontmatter(meta, body), encoding="utf-8")
        print(f"  Updated: {path.name}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Auto-tag Hugo blog posts via a local LM Studio model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--phase1-only", action="store_true", help="Generate taxonomy only")
    parser.add_argument("--phase2-only", action="store_true", help="Tag posts using existing taxonomy.json")
    parser.add_argument("--dry-run", action="store_true", help="Run Phase 2, print results, write nothing to disk")
    parser.add_argument("--apply", action="store_true", help="Write suggestions.json to frontmatter")
    parser.add_argument("--and-apply", action="store_true", help="Run Phase 2 then immediately apply to frontmatter")
    parser.add_argument("--from-description", action="store_true", help="Tag from title+description only (ignore body)")
    parser.add_argument("--taxonomy-model", default=TAXONOMY_MODEL, help="Model for Phase 1")
    parser.add_argument("--labeling-model", default=LABELING_MODEL, help="Model for Phase 2")
    parser.add_argument("--lm-studio-url", default=LM_STUDIO_URL, help="LM Studio base URL")
    parser.add_argument("--content-dir", type=Path, default=_CONTENT_DIR, help="Hugo content/ directory")
    return parser


def run_phase1(client: OpenAI, posts: list[Frontmatter], model: str) -> list[TagEntry]:
    """Run Phase 1: print sample list, generate taxonomy, save to disk.

    Args:
        client: Configured OpenAI-compatible client.
        posts: All collected posts.
        model: LM Studio model ID to use.

    Returns:
        Generated tag taxonomy.
    """
    sample = posts[: min(PHASE1_SAMPLE_SIZE, len(posts))]
    print(f"\nPhase 1: generating taxonomy from {len(sample)} posts via {model}...")
    print("  Posts used as taxonomy input:")
    for p in sample:
        rel = Path(str(p["path"])).relative_to(_CONTENT_DIR.parent)
        print(f"    {rel}  ({p['title']})")
    print()
    taxonomy = generate_taxonomy(client, posts, model)
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TAXONOMY_FILE.write_text(json.dumps({"tags": taxonomy}, indent=2))
    print(f"Taxonomy saved → {TAXONOMY_FILE}")
    print(f"  {len(taxonomy)} tags: {', '.join(t['name'] for t in taxonomy)}")
    return taxonomy


def run_phase2(client: OpenAI, posts: list[Frontmatter], taxonomy: list[TagEntry], model: str, dry_run: bool, and_apply: bool, include_body: bool = True) -> None:
    """Run Phase 2: assign tags, print summary, optionally save or apply.

    Args:
        client: Configured OpenAI-compatible client.
        posts: All collected posts.
        taxonomy: Tag taxonomy from Phase 1.
        model: LM Studio model ID to use.
        dry_run: If True, print results but write nothing to disk.
        and_apply: If True, write suggestions then apply to frontmatter.
        include_body: If False, tag from title+description only.
    """
    mode = "title+description only" if not include_body else "title+description+body"
    print(f"\nPhase 2: tagging {len(posts)} posts via {model} ({mode})...")
    suggestions_list: list[Suggestion] = []
    for i, post in enumerate(posts, 1):
        tags = assign_tags(client, post, taxonomy, model, include_body=include_body)
        changed = post["current_tags"] != tags
        title = str(post["title"])[:55]
        print(f"  [{i:>3}/{len(posts)}] {title:<55} → {tags}{' *' if changed else ''}")
        suggestions_list.append(
            {"path": post["path"], "title": post["title"], "current_tags": post["current_tags"], "suggested_tags": tags}
        )

    _print_summary(suggestions_list, dry_run, and_apply)


def _print_summary(suggestions_list: list[Suggestion], dry_run: bool, and_apply: bool) -> None:
    """Print the post/tag summary table and handle save or apply.

    Args:
        suggestions_list: Per-post tag suggestions from Phase 2.
        dry_run: If True, print results but write nothing to disk.
        and_apply: If True, write suggestions then apply to frontmatter.
    """
    print("\n" + "─" * 72)
    print(f"{'POST':<48} {'SUGGESTED TAGS'}")
    print("─" * 72)
    for s in suggestions_list:
        title = str(s["title"])[:47]
        tags_str = ", ".join(str(t) for t in s["suggested_tags"]) if s["suggested_tags"] else "(none)"
        marker = " *" if s["current_tags"] != s["suggested_tags"] else ""
        print(f"  {title:<46} {tags_str}{marker}")
    print("─" * 72)
    changed_count = sum(1 for s in suggestions_list if s["current_tags"] != s["suggested_tags"])
    print(f"  {len(suggestions_list)} posts  |  {changed_count} with tag changes  |  * = differs from current")
    print()

    if dry_run:
        print("(dry run — no files written)")
    elif and_apply:
        apply_suggestions(suggestions_list)
        print("\n\033[32m✓ Tags applied to frontmatter\033[0m")
    else:
        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        SUGGESTIONS_FILE.write_text(json.dumps(suggestions_list, indent=2))
        print(f"Suggestions saved → {SUGGESTIONS_FILE}")
        print("Review, then run with --apply to update frontmatter.")
    print("\n\033[32m✓ Phase 2 complete\033[0m")


def main() -> None:
    """Entry point — parse args and dispatch to the selected phase(s)."""
    args = build_parser().parse_args()

    if args.apply:
        if not SUGGESTIONS_FILE.exists():
            print(f"[ERROR] No suggestions file found at {SUGGESTIONS_FILE}. Run Phase 2 first.", file=sys.stderr)
            sys.exit(1)
        suggestions: list[Suggestion] = json.loads(SUGGESTIONS_FILE.read_text())
        print(f"Applying tags to {len(suggestions)} posts...")
        apply_suggestions(suggestions)
        print("\n\033[32m✓ Tags applied\033[0m")
        return

    client = OpenAI(base_url=args.lm_studio_url, api_key="lm-studio")
    posts = collect_posts(args.content_dir)
    print(f"Found {len(posts)} published posts.")

    taxonomy: list[TagEntry] = []
    if not args.phase2_only:
        taxonomy = run_phase1(client, posts, args.taxonomy_model)

    if args.phase1_only:
        print("\n\033[32m✓ Phase 1 complete\033[0m")
        return

    if args.phase2_only:
        if not TAXONOMY_FILE.exists():
            print(f"[ERROR] No taxonomy file found at {TAXONOMY_FILE}. Run Phase 1 first.", file=sys.stderr)
            sys.exit(1)
        taxonomy = json.loads(TAXONOMY_FILE.read_text())["tags"]
        print(f"Loaded {len(taxonomy)} tags from {TAXONOMY_FILE}")

    run_phase2(client, posts, taxonomy, args.labeling_model, args.dry_run, args.and_apply, include_body=not args.from_description)


if __name__ == "__main__":
    main()
