---
title: "How to Get Blazingly Fast Text Search in Your CLI That Doesn't Suck"
subtitle: "Exact keyword matching is fast in the CLI. When text is spelled differently, or you cannot remember how it was written, you need to upgrade your search tools. This article explains how."
slug: "how-to-get-blazingly-fast-text-search-in-your-cli-that-doesnt-suck"
aliases:
  - /blog/blazingly-fast-lexical-and-semantic-search-in-your-cli/
date: 2026-09-12
draft: false
description: "Finding a file by name is easy. Finding it because you remember what it was about is much harder. qsearch is a small shell pipeline that starts with extremely fast lexical search over ripgrep and ripgrep-all, expands the query linguistically, and only falls back to local semantic search when the cheaper stages do not produce convincing results."
author: "Florian Buetow"
readTime: "11 min read"
categories: []
tags: []
---

I have a lot of information sitting in text files on disk, including Markdown notes, text files, source code, PDFs, Word documents, notebooks, and various other formats spread across local and external drives. Finding a file by name is easy. Finding a file because you remember *what it was about* is a lot harder.

When I started this mini-project I wanted an intelligent search function that wasn't as slow as an LLM and that didn't require the heavy lifting of indexing before searching. I wanted a command that I can run like this:

```bash
qsearch "how are autonomous agents evaluated?" \
  ~/Documents \
  /Volumes/Archive
```

It should return a list of the files most likely to contain the information I am looking for, and it should be fast. There should be no reason to run an embedding model across thousands of documents if a simple lexical search can already answer the question.

The result is `qsearch`: a small shell-based search pipeline that starts with extremely fast lexical search, expands the query linguistically to find files that contain variations of the words in my search query, and that only falls back to semantic search when the cheaper methods don't produce high quality results. But before we get into that, let's start from the beginning ...

## Starting with *find* and *grep*

The Unix CLI already gives us two fundamental tools for finding things. `find` is very good at finding files based on properties of the file itself:

```bash
find ~/Documents -name "*.md"
find ~/Documents -iname "*evaluation*"
```

But this searches filenames and filesystem metadata, not the actual meaning or content of text in files. For finding files with specific content we have `grep`:

```bash
grep -Rni "agent evaluation" ~/Documents
```

Now we are searching for text *inside* files. This lexical search works extremely well when we know the exact wording used in the document. But if the document contains `measuring the performance of autonomous systems`, then searching for `agent evaluation` with find and grep won't show it as a result.

Before we fall back to full-blown semantic search, let's try to make lexical search better. After all, it's the fastest search method without indexing files.

## *ripgrep*: a much better grep

The tool `ripgrep` (via `rg` command) is a modern CLI search tool optimized for recursively searching files[^ripgrep]:

```bash
rg "agent evaluation" ~/Documents
```

It adds several useful defaults and capabilities. `rg -i` performs case-insensitive matching, `rg -S` uses smart-case matching, and `-g` restricts the search to particular files:

```bash
rg -i "agent evaluation" ~/Documents
rg -S "agent evaluation" ~/Documents
rg -g '*.md' -g '*.txt' "agent evaluation" ~/Documents
```

It also understands ignore files (e.g. `.gitignore`), skips binary files by default, supports Unicode, file-type filtering, regular expressions, multiline search, and - if you really need it - PCRE2 expressions. Most importantly, it is still extremely fast. A large part of that comes from Rust's regex implementation based on finite automata with SIMD and other technical shenanigans to optimize literal matching with parallel directory traversal, and built-in parts to automatically choose appropriate filesystem search strategies.

In short: A lot of optimizations that make it worth using it for searching ordinary text files. But what about non-plaintext text files?

## *ripgrep-all*: search PDFs, DOCX files and more

A large part of my information is not stored in `.txt` or `.md` files. Reports I generate using deep research are often PDF, as are papers I download from ArXiv.org. Then there are word documents, EPUBs I bought, Jupyter notebooks and some other formats. This is where `ripgrep-all` with its `rga` command becomes useful.[^rga] Instead of `rg "evaluation" .` we can use:

```bash
rga "evaluation" .
```

`rga` uses `ripgrep` underneath but adds adapters that convert other document formats into searchable text, and then feeds the resulting text into `ripgrep`. Here is an overview of what `rga` uses to perform (a fully transparent) conversion before attempting to match your search query against the text it finds:

```text
PDF               -> pdftotext
DOCX / ODT        -> pandoc
EPUB              -> pandoc
Jupyter notebook  -> pandoc
HTML              -> pandoc
ZIP / TAR         -> archive adapters
SQLite            -> SQLite adapter
```

That's right, it can even search in `.zip` files and `sqlite` databases.

I said in the beginning that I don't want to build an index over the files that I search. On the other hand I don't mind if the tool does that fast and transparent to me as a user.

`rga` caches extracted representations of documents. On macOS this cache normally lives under `~/Library/Caches/ripgrep-all/`, so a PDF does not necessarily have to be converted again for every search, which is nice.

At this point we now have a very fast search mechanism covering a surprisingly large collection of document formats, but we still have the lexical-search problem ...

## The lexical matching problem

Consider the query `evaluating autonomous agents`. A document might instead contain `evaluation of autonomous agents`, or `we evaluated the autonomous agent`, or, in German (bear with me), `Bewertung autonomer Agenten`. Simple text matching treats all of these forms as different strings, which means no search results.

Case is the easy part: `rg -i "evaluation"` lowercases both sides and effectively removes case as a source of mismatch. But we can do more. We can morph words. The following words are all closely related from an information-retrieval perspective:

```text
evaluate
evaluates
evaluated
evaluating
evaluation
evaluations
```

`ripgrep` deliberately does not perform stemming, lemmatization, synonym expansion, or natural-language interpretation, so we need to expand the query ourselves before we give it to `ripgrep`.

## Query expansion

One possibility is stemming. `Snowball`, for example, can reduce related words toward a common stem:

```text
evaluating -> evalu
evaluated  -> evalu
evaluation -> evalu
```

But there is an important subtlety here: we are not stemming the documents, we are searching the original files with `ripgrep`. Searching literally for `evalu` is therefore not quite the same thing as running a traditional information-retrieval system in which both documents and queries have been stemmed to optimize retrieval quality.

Instead, `qsearch` uses the stem to construct a broader regular expression matching possible continuations. Conceptually, a query term can become something resembling:

```regex
\b(?:evaluate|evaluation|evalu\p{L}*)\b
```

That allows `ripgrep` to match several morphological variants of query words while still searching the original documents directly.

`qsearch` uses **Snowball by default** because it is lightweight and fast enough to run for every query.

## Taking it a step further with LAS


LAS (Language Analysis Tool) enables richer linguistic processing.

```bash
qsearch \
  --linguistics las \
  --lang de \
  "bewertete autonome Agenten" \
  ~/Documents
```

`qsearch` uses it specifically for language identification and lemmatization before passing the resulting terms through Snowball stemming. LAS is linguistically more sophisticated, but it has substantially higher startup overhead because some of its language models and transducers are large. LAS' documentation recommends using it in batch processing pipelines rather than repeatedly starting it for very small inputs, as we would do when we run a single `qsearch` query. That's why we use Snowball as the default and offer LAS as a fallback when we need higher-quality linguistic normalization to get good search results from `qsearch`.

`qsearch` also removes common English or German stopwords before constructing the expanded search. A query such as `how are autonomous agents evaluated?` will essentially be reduced to the concepts `autonomous`, `agent` and `evaluated`, which can then be expanded into expressions that include their morphological variants.

## Ranking lexical results instead of merely finding matches

It seems we should be getting to the end of this soon, but there is another issue we have to consider first: the issue of how to rank results when we get them.

Suppose one document contains the word `agent` 50 times, while another document contains `autonomous`, `agent` and `evaluation` once each. For our query, the second document is probably much more relevant, so raw occurrence count is not enough.

`qsearch` treats the meaningful query terms as separate **concepts** and calculates how many of them each file contains. For a query built from the four concepts `autonomous`, `agent`, `evaluate` and `success`, a document matching three of them has a concept coverage of `3 / 4 = 0.75`. An exact phrase match receives an additional boost. While this is not exactly BM25 or TF/IDF it gives us a simple lexical confidence score that works well enough in most cases, and that I am willing to accept as a tradeoff for not having to build an entire index. The default threshold is `0.75` at the time of writing, and can be changed with:

```bash
qsearch \
  --threshold 0.60 \
  "autonomous agent evaluation" \
  ~/Documents
```

This confidence score is what makes the next part possible.

## Semantic and hybrid search

Sometimes lexical search simply cannot find a good match. Consider searching for `how do we determine whether an AI agent completed its task correctly?` while the document says `success criteria are evaluated after execution`. There might be very little lexical overlap even though their meaning is almost identical, or - as we prefer to say - semantically close.

To solve this problem we can use `clawgrep`.[^clawgrep] It combines two retrieval signals, embedding similarity and keyword matching, and fuses their rankings using weighted Reciprocal Rank Fusion. Its default weighting favors semantic similarity while still preserving lexical matches for things embeddings are bad at, such as identifiers, serial numbers and exact strings:

```bash
clawgrep \
  --show-score \
  "how do agents determine task success?" \
  ~/Documents
```

`clawgrep` builds an index and splits documents it sees for the first time into chunks, computes embeddings - with a very small embedding model - locally and caches them on disk. Subsequent searches reuse these embeddings until the files change, in which case it recomputes them. This is much more expensive than `ripgrep`. However, that doesn't mean we need to always run it. We only want to run it when the confidence score from our elaborate lexical search is below the threshold.

## Cascading search with *qsearch*

The following shows the full picture of how `qsearch` combines the tools I've shown you into a cascading retrieval pipeline that only uses semantic search (`clawgrep`) as a fallback mechanism.

```ascii
┌──────────────────────────────────────────┐
│ Natural-language query                   │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Language detection                       │
│ Stopword removal                         │
│ Query expansion                          │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Exact lexical search (rga)               │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Expanded lexical search                  │
│ (Snowball or LAS, then rga)              │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Calculate lexical confidence             │
└───────┬─────────────────────────┬────────┘
        │ high                    │ low
        ▼                         ▼
┌───────────────────┐  ┌────────────────────────┐
│ Return lexical    │  │ Semantic / hybrid      │
│ results           │  │ search (clawgrep)      │
└───────────────────┘  └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │ Combine lexical and    │
                       │ semantic ranking       │
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │ Best matching files    │
                       └────────────────────────┘
```

The important point is (again) that semantic search is a **fallback**, not the default. For an easy query such as `qsearch "PostgreSQL connection timeout" ~/Projects`, `ripgrep` may already produce extremely strong results, and there is no reason to run an embedding model at all. A fuzzy query is a different matter:

```bash
qsearch \
  "notes about why humans struggle to review generated code" \
  ~/Documents
```

Here the lexical confidence may be low, causing `qsearch` to automatically continue into semantic retrieval. Semantic search can also be forced or disabled explicitly:

```bash
qsearch --semantic always "agent evaluation" ~/Documents
qsearch --semantic never "agent evaluation" ~/Documents
```

## Searching multiple locations and file types

Some more useful tips for using `qsearch`. It accepts one or more paths:

```bash
qsearch \
  "software factory evaluation" \
  ~/Documents \
  ~/Projects \
  /Volumes/Archive \
  /Volumes/Research
```

By default it searches common text and source-code formats together with document formats including PDF, DOCX, ODT, EPUB and Jupyter notebooks. The file types can be restricted, and a query language can be specified explicitly instead of relying on the default language detection:

```bash
qsearch --types md,txt,pdf,docx "agent evaluation" ~/Documents
qsearch --lang de "Bewertung autonomer Agenten" ~/Documents
```

## What happens to PDFs and other rich documents?

`ripgrep-all` already handles these formats during lexical search. For semantic search, however, `clawgrep` needs searchable text, so `qsearch` creates a local extracted-text representation when necessary:

```text
PDF                           -> pdftotext -> local text
DOCX / ODT / EPUB / notebook  -> pandoc    -> local text
```

Normal text files are not copied at all. `qsearch` creates stable symbolic links to them in its semantic corpus. This is particularly useful when searching through external drives: the original files can stay on `/Volumes/Archive/` or `/Volumes/Research/` while the expensive derived information lives on the internal disk (hopefully an SSD).

## The cache and semantic index

On macOS, `qsearch` keeps its working data under `~/Library/Caches/qsearch/`, and on Linux under `~/.cache/qsearch/`. The structure is roughly:

```text
qsearch/
  runs/        results of individual searches
  extracted/   cached text from PDFs and other rich documents
  corpus/      stable paths for the semantic-search corpus
  clawgrep/    embedding model and semantic embedding cache
```

Indexed as well as extracted documents are associated with their source paths, modification time and file size. If a document has not changed, its extracted representation can be reused; if it changes, it is extracted again. Similarly, `clawgrep` automatically reuses embeddings for unchanged files and re-embeds changed ones, so normally there is no explicit indexing workflow to maintain. It also provides `clawgrep --reindex "query" PATH` for when you want the semantic embeddings deliberately to be rebuilt, and you can use `clawgrep --no-cache "query" PATH` if you want completely uncached operation.

The cache uses paths to identify documents, and `qsearch` canonicalizes its input paths before searching, which keeps searches through `/Volumes/Archive/Documents` consistent across runs.

The cached data does **not**, however, turn files on disconnected drives into an offline search index. If `/Volumes/Archive` is unavailable, those original files are simply not part of the current search. Once the drive is mounted again under the same path, the existing cached extraction and embeddings can be reused wherever the files have not changed.

## Inspecting what the search actually did

One property I wanted from `qsearch` was that the cascade should not become a black box, so every search keeps the output of every retrieval stage. A run contains files such as:

```text
00-query.txt
01-exact.txt
02-expanded.txt
03-semantic.txt
lexical-ranking.tsv
ranking.tsv
final.txt
```

So even if the final result is just a single line naming the best match, the cascade stays open to inspection. The run directory shows what the exact search found, what query expansion added, why semantic search was triggered, what `clawgrep` returned, and how the results were ranked.

This turns out to be useful both for debugging the search and for understanding why a particular document surfaced, especially when giving my local agents access to `qsearch`.

## Putting it all together

I will find that for many searches the cascade never reaches the expensive semantic stage. The more you know what you are looking for the less likely it is that `qsearch` needs to fall back to semantic retrieval. But if it does it is automatically available. That gives us the advantages of both worlds: `ripgrep` speed, linguistic query expansion, semantic similarity, and hybrid ranking, without requiring every query to pay the cost of semantic retrieval.

```ascii
                         COST
                          ▲
semantic/hybrid search    │                           ● clawgrep
expanded lexical search   │                 ● Snowball/LAS + rga
exact lexical search      │         ● rga
filename search           │   ● find / rg --files
                          └─────────────────────────────────────▶
                                      RETRIEVAL POWER
```

## Conclusion

Building a surprisingly capable local search engine for your own documents does not require Elasticsearch, a vector database, a search server, or a large application. Most of the difficult pieces already exist. `ripgrep` gives you extremely fast lexical search, `ripgrep-all` extends that search to PDFs, Office documents and many other formats, Snowball and LAS give us linguistic normalization and query expansion, and `clawgrep` adds local semantic and hybrid retrieval as a fallback.

A relatively small shell script can then orchestrate these tools as a cascade. This is what `qsearch` is. It starts with the fastest and cheapest search, measures whether its results are convincing, and only escalates when necessary. The result is fast for easy queries, considerably smarter for difficult ones, completely local, inspectable, and requires little or no index maintenance.

That is what `qsearch` does. You can get it from GitHub [here](https://github.com/florianbuetow/qsearch-bash).[^qsearch]

---

## References

[^ripgrep]: ripgrep, a line-oriented search tool that recursively searches directories with Rust's regex engine, cited as the fast exact-match stage of the cascade. https://github.com/BurntSushi/ripgrep
[^rga]: ripgrep-all (rga), a ripgrep wrapper whose adapters extract searchable text from PDF, DOCX, EPUB, notebooks and archives, cited for extending lexical search beyond plain text. https://github.com/phiresky/ripgrep-all
[^clawgrep]: clawgrep, a local hybrid retrieval tool that fuses embedding similarity with keyword matching using weighted Reciprocal Rank Fusion, cited as the semantic fallback stage. https://github.com/Schonhoffer/clawgrep
[^qsearch]: qsearch, the cascading lexical and semantic file search described in this article. https://github.com/florianbuetow/qsearch-bash
