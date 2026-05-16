# autotag — Technique and Research

## What it does

`autotag` automatically assigns tags to Hugo blog posts using a locally-hosted LLM (via LM Studio). It runs in two phases:

**Phase 1 — Taxonomy generation ("training")**
A sample of existing posts is fed to the LLM in a single prompt. It reads across all posts and produces a coherent set of 20–35 tags with descriptions, incorporating existing tags from frontmatter and filling any gaps. Output: `data/output/autotag_taxonomy.json`.

**Phase 2 — Per-post classification ("labeling")**
For each post, a separate prompt is sent containing the full taxonomy (each tag as `name: description`) and the post content. The LLM picks 2–5 tags from the fixed vocabulary. Because descriptions are included, it understands intent rather than matching on name alone.

The two phases are intentionally separate: generating the taxonomy once from all posts ensures every classification uses the same vocabulary. Running Phase 2 per-post without a shared taxonomy would produce inconsistent, ad-hoc tags across the blog.

## Workflow

```
just autotag-train    # Phase 1 — generate taxonomy.json
just autotag-dryrun   # Phase 2 (dry run) — preview assignments, nothing written
just autotag-apply    # Phase 2 — tag posts and write to frontmatter
```

Edit `data/output/autotag_taxonomy.json` between train and dryrun to tune tag names or descriptions without re-training.

---

## Research basis

### TnT-LLM: Text Mining at Scale with Large Language Models
**arxiv: 2403.12173** — Wan et al., Microsoft (2024) — 20 upvotes on HuggingFace

The direct basis for this implementation. Proposes a two-phase framework:
1. Zero-shot multi-stage LLM reasoning to produce and iteratively refine a label taxonomy from a corpus sample.
2. LLM-annotated pseudo-labels used to train a lightweight supervised classifier for large-scale deployment.

The TnT-LLM paper targets Bing Copilot at web scale (48k+ conversations). For a personal blog, Phase 3 (distilling to a BERT/LR classifier) is unnecessary — the LLM itself handles labeling directly.

https://arxiv.org/abs/2403.12173

---

### LLM4Tag: Automatic Tagging System for Information Retrieval via Large Language Models
**arxiv: 2502.13481** — KDD 2025, deployed to 100M+ users

Industrial SOTA for automated content tagging. Three modules:
1. **Graph-based tag recall** — builds a content-tag graph using embeddings; walks two meta-paths (content→tag similarity, content→similar-content→their-tags) to assemble candidate tags from a million-tag repository.
2. **Knowledge-enhanced tag generation** — long-term and short-term domain knowledge injection into the LLM prompt.
3. **Tag confidence calibration** — reliable per-tag confidence scores.

The graph recall module solves a problem that doesn't apply here (a vocabulary of millions of tags). For a personal blog with a fixed 20–35 tag vocabulary, the entire tag list fits in a single prompt.

https://arxiv.org/abs/2502.13481

---

### Building Efficient Universal Classifiers with Natural Language Inference
**arxiv: 2312.17543** — Laurer et al., Hugging Face (2024) — 55M+ downloads

Explains the NLI-based zero-shot classification approach as an alternative to LLM prompting. Any classification task reformulates as a binary entailment decision:

- Premise: post content
- Hypothesis: `"This text is about {tag}"`
- Decision: entailment score

The resulting model (`MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33`) runs locally via the HuggingFace `pipeline("zero-shot-classification")` API — no LM Studio required, no API costs, ~1–3s per post on CPU. Trade-off: O(N_tags) inference calls per post; slower than a single LLM prompt with all tags.

https://arxiv.org/abs/2312.17543

---

### Using Zero-shot Prompting in the Automatic Creation and Expansion of Topic Taxonomies for Tagging
**arxiv: 2401.06790** — Moraes et al., PUC-Rio / BTG Pactual (2024)

Validates the LLM-prompt approach for taxonomy-based tagging in a production setting (retail bank transactions). Key finding: LLM-assigned tags achieved >90% human-rated coherence across two taxonomies. Uses YAKE for initial keyword extraction and LDA for topic modeling, then LLM post-processing to build and expand the hierarchy.

https://arxiv.org/abs/2401.06790
