#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "stylometry-python-lib @ git+https://github.com/florianbuetow/stylometry-python-lib",
#   "pandas",
#   "numpy",
#   "scikit-learn",
#   "joblib",
#   "matplotlib",
#   "plotly",
#   "pyarrow",
#   "pyyaml",
# ]
# ///
"""Stylometric feature analysis of published articles.

WHAT: read every non-draft article under content/, extract a stylometric feature
vector per article with the stylometry-python-lib deterministic extractor, reduce
those high-dimensional vectors to a lower-dimensional space with PCA (keeping the
smallest number of components that preserve a configurable share of the variance,
default 85%), then project the reduced vectors onto a 2-D plane with t-SNE and
plot them. Every saved table keeps per-row labels (slug, title, section, date,
category, path) so the vectors remain interpretable.

Pipeline:
  1. discover published (draft != true) articles under the given content dirs
  2. clean each article's Markdown down to prose
  3. extract ~1,500 deterministic stylometric features per article
  4. standardize, then fit PCA to preserve >= the variance threshold
  5. transform every document vector into the PCA space
  6. project to 2-D with t-SNE and render a scatter plot coloured by section

Outputs (default reports/stylometry/):
  features_raw.parquet         full feature matrix, one labelled row per article
  features_pca.csv             PCA-reduced vectors, one labelled row per article
  pca_explained_variance.csv   per-component and cumulative explained variance
  pca_pipeline.joblib          trained StandardScaler + PCA transform
  feature_importance.md        every feature ranked by PCA variance contribution
  tsne_2d.csv                  2-D t-SNE coordinates, one labelled row per article
  tsne_3d.csv                  3-D t-SNE coordinates, one labelled row per article
  stylometry_tsne.png          2-D scatter plot coloured by section
  stylometry_tsne_3d.png       static 3-D scatter as a 2x2 grid of four angles
  stylometry_tsne_3d.html      interactive (rotatable) 3-D scatter, hover labels

    uv run scripts/analyze-stylometry.py                     # all published content
    uv run scripts/analyze-stylometry.py --dir content/blog  # one section
    uv run scripts/analyze-stylometry.py --variance 0.90     # keep 90% of variance
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ANSI_RED = "\033[0;31m"
ANSI_GREEN = "\033[0;32m"
ANSI_BLUE = "\033[0;34m"
ANSI_YELLOW = "\033[0;33m"
ANSI_RESET = "\033[0m"

DEFAULT_DIRS = ["content/blog", "content/ticker", "content/projects"]
DEFAULT_OUTPUT_DIR = "reports/stylometry"
DEFAULT_VARIANCE = 0.85
DEFAULT_SEED = 42

LABEL_COLUMNS = ["label", "title", "section", "date", "category", "path"]

# --- Markdown -> prose cleaning (mirrors scripts/update-read-times.py) -----------
_FRONT_MATTER_RE = re.compile(r"^\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_FENCED_CODE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
_TILDE_CODE_RE = re.compile(r"^~~~.*?^~~~", re.MULTILINE | re.DOTALL)
_SHORTCODE_RE = re.compile(r"\{\{[<%].*?[>%]\}\}", re.DOTALL)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_FRONT_MATTER_STRIP_RE = re.compile(r"^\s*---\n.*?\n---\n", re.DOTALL)


@dataclass
class Article:
    """A single published article and its label metadata."""

    path: Path
    section: str
    label: str
    title: str
    date: str
    category: str
    text: str


def parse_front_matter(raw: str) -> dict | None:
    """Return the YAML front matter as a dict, or None if there is none."""
    import yaml

    match = _FRONT_MATTER_RE.match(raw)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def strip_markdown(text: str) -> str:
    """Reduce a Markdown article to plain prose for stylometric analysis."""
    text = _FRONT_MATTER_STRIP_RE.sub("", text, count=1)
    text = _FENCED_CODE_RE.sub("", text)
    text = _TILDE_CODE_RE.sub("", text)
    text = _SHORTCODE_RE.sub("", text)
    text = _HTML_TAG_RE.sub("", text)
    text = _IMAGE_RE.sub("", text)
    text = _LINK_RE.sub(r"\1", text)
    return text.strip()


def is_draft(front_matter: dict) -> bool:
    """True only when the article is explicitly marked draft (Hugo semantics)."""
    return front_matter.get("draft") is True


def first_category(front_matter: dict) -> str:
    categories = front_matter.get("categories")
    if isinstance(categories, list) and categories:
        return str(categories[0])
    if isinstance(categories, str) and categories:
        return categories
    return "—"


def article_files(content_dir: Path) -> list[Path]:
    """Top-level `*.md` plus one-level `*/index.md` bundles, skipping `_*` pages."""
    files: list[Path] = []
    for md in sorted(content_dir.glob("*.md")):
        if not md.name.startswith("_"):
            files.append(md)
    for index in sorted(content_dir.glob("*/index.md")):
        if not index.name.startswith("_"):
            files.append(index)
    return files


def load_article(path: Path, section: str) -> Article | None:
    """Read, parse, and clean one article; None if draft, malformed, or empty."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{ANSI_RED}  cannot read {path}: {exc}{ANSI_RESET}", file=sys.stderr)
        return None

    front_matter = parse_front_matter(raw)
    if front_matter is None:
        print(f"{ANSI_YELLOW}  skip (no front matter): {path}{ANSI_RESET}")
        return None
    if is_draft(front_matter):
        return None

    text = strip_markdown(raw)
    if not text:
        print(f"{ANSI_YELLOW}  skip (empty prose): {path}{ANSI_RESET}")
        return None

    stem = path.parent.name if path.name == "index.md" else path.stem
    label = str(front_matter.get("slug") or stem)
    return Article(
        path=path,
        section=section,
        label=label,
        title=str(front_matter.get("title", label)),
        date=str(front_matter.get("date", "")),
        category=first_category(front_matter),
        text=text,
    )


def discover_articles(content_dirs: list[Path]) -> list[Article]:
    articles: list[Article] = []
    for content_dir in content_dirs:
        if not content_dir.is_dir():
            print(f"{ANSI_YELLOW}  no such directory: {content_dir}{ANSI_RESET}")
            continue
        section = content_dir.name
        for path in article_files(content_dir):
            article = load_article(path, section)
            if article is not None:
                articles.append(article)
    return articles


def extract_features(articles: list[Article]):
    """Run the deterministic stylometric extractor; return a numeric feature frame."""
    import numpy as np
    import pandas as pd
    from stylometry_python_lib import default_deterministic_extractor

    documents = pd.DataFrame({"text": [a.text for a in articles]})
    extractor = default_deterministic_extractor(text_column="text", output="pandas")
    features = extractor.fit_transform(documents, None)
    features = features.reset_index(drop=True)

    numeric = features.select_dtypes(include=[np.number])
    numeric = numeric.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return numeric


def labels_frame(articles: list[Article]):
    import pandas as pd

    return pd.DataFrame(
        {
            "label": [a.label for a in articles],
            "title": [a.title for a in articles],
            "section": [a.section for a in articles],
            "date": [a.date for a in articles],
            "category": [a.category for a in articles],
            "path": [str(a.path) for a in articles],
        }
    )


def run_pca(numeric, variance: float, seed: int):
    """Fit StandardScaler + PCA preserving >= `variance`; return (pipeline, Z, ratios)."""
    from sklearn.decomposition import PCA
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=variance, svd_solver="full", random_state=seed)),
        ]
    )
    reduced = pipeline.fit_transform(numeric.to_numpy(dtype=float))
    pca = pipeline.named_steps["pca"]
    return pipeline, reduced, pca.explained_variance_ratio_


def resolve_perplexity(n_samples: int, requested: int | None) -> int:
    """t-SNE perplexity must stay below the sample count; auto-scale when unset."""
    perplexity = requested if requested is not None else max(2, min(30, (n_samples - 1) // 3))
    return min(perplexity, n_samples - 1)


def run_tsne(reduced, perplexity: int, seed: int, n_components: int):
    import numpy as np
    from sklearn.manifold import TSNE

    tsne = TSNE(
        n_components=n_components,
        perplexity=float(perplexity),
        init="pca",
        learning_rate="auto",
        random_state=seed,
    )
    return tsne.fit_transform(np.asarray(reduced, dtype=float))


def feature_importance(pipeline, feature_names, ratios):
    """Rank features by their contribution to the variance retained by PCA.

    For feature j the contribution is sum_i (explained_variance_ratio_i *
    loading_{i,j}^2) over the retained components i, where the loadings are the
    PCA eigenvector entries on the standardized features. Because each eigenvector
    has unit norm, these contributions sum to the total retained variance, so the
    ranking is exactly how PCA weighs each feature's share of the variance.
    """
    import numpy as np
    import pandas as pd

    pca = pipeline.named_steps["pca"]
    loadings_sq = np.square(pca.components_)  # (k_components, n_features)
    contribution = (np.asarray(ratios)[:, None] * loadings_sq).sum(axis=0)
    total = contribution.sum()

    frame = pd.DataFrame(
        {
            "feature": list(feature_names),
            "variance_contribution": contribution,
            "relative_importance_pct": 100.0 * contribution / total,
        }
    )
    frame = frame.sort_values(
        "variance_contribution", ascending=False
    ).reset_index(drop=True)
    frame.insert(0, "rank", frame.index + 1)
    frame["cumulative_pct"] = frame["relative_importance_pct"].cumsum()
    return frame


def write_feature_importance_md(
    frame, output_path, n_articles: int, n_components: int, preserved: float
) -> None:
    """Render the ranked feature-importance frame as a Markdown report."""
    lines = [
        "# Stylometric Feature Importance (PCA variance contribution)",
        "",
        "Generated by `scripts/analyze-stylometry.py`. Every stylometric feature is",
        "ranked by how much it contributes to the variance retained by PCA.",
        "",
        "For feature *j* the contribution is "
        "`sum_i (explained_variance_ratio_i x loading_{i,j}^2)` over the retained",
        "components *i*, where loadings are the PCA eigenvector entries on the",
        "standardized features. These contributions sum to the total retained",
        f"variance ({preserved:.1%}), so the ranking is exactly how PCA weighs each",
        "feature's share of the variance.",
        "",
        f"- Articles analyzed: **{n_articles}**",
        f"- Stylometric features: **{len(frame)}**",
        f"- Retained PCA components: **{n_components}** (preserve {preserved:.1%} of variance)",
        "",
        "| Rank | Feature | Variance contribution | Relative importance % | Cumulative % |",
        "|---:|:---|---:|---:|---:|",
    ]
    for row in frame.itertuples(index=False):
        lines.append(
            f"| {row.rank} | `{row.feature}` | {row.variance_contribution:.6e} "
            f"| {row.relative_importance_pct:.4f} | {row.cumulative_pct:.4f} |"
        )
    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def plot_tsne(coords, articles: list[Article], output_path: Path, variance: float) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sections = sorted({a.section for a in articles})
    cmap = plt.get_cmap("tab10")
    color_for = {section: cmap(i % 10) for i, section in enumerate(sections)}

    fig, ax = plt.subplots(figsize=(12, 9))
    for section in sections:
        idx = [i for i, a in enumerate(articles) if a.section == section]
        ax.scatter(
            coords[idx, 0],
            coords[idx, 1],
            color=color_for[section],
            label=f"{section} (n={len(idx)})",
            s=70,
            alpha=0.85,
            edgecolors="white",
            linewidths=0.5,
        )
    for i, article in enumerate(articles):
        short = article.label if len(article.label) <= 28 else article.label[:27] + "…"
        ax.annotate(
            short,
            (coords[i, 0], coords[i, 1]),
            fontsize=6,
            alpha=0.6,
            xytext=(3, 3),
            textcoords="offset points",
        )

    ax.set_title(
        f"Stylometric t-SNE of {len(articles)} published articles "
        f"(PCA preserving {variance:.0%} variance)"
    )
    ax.set_xlabel("t-SNE dimension 1")
    ax.set_ylabel("t-SNE dimension 2")
    ax.legend(title="Section", loc="best")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_tsne_3d_png(coords, articles: list[Article], output_path: Path, variance: float) -> None:
    """Static 3-D scatter as a 2x2 grid of four viewing angles (a turntable)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3-D projection)

    sections = sorted({a.section for a in articles})
    cmap = plt.get_cmap("tab10")
    color_for = {section: cmap(i % 10) for i, section in enumerate(sections)}
    section_idx = {
        section: [i for i, a in enumerate(articles) if a.section == section]
        for section in sections
    }

    views = [(22, 45), (22, 135), (22, 225), (22, 315)]
    fig = plt.figure(figsize=(14, 11))
    axis = None
    for position, (elev, azim) in enumerate(views, start=1):
        axis = fig.add_subplot(2, 2, position, projection="3d")
        for section in sections:
            idx = section_idx[section]
            axis.scatter(
                coords[idx, 0],
                coords[idx, 1],
                coords[idx, 2],
                color=color_for[section],
                label=f"{section} (n={len(idx)})",
                s=40,
                alpha=0.85,
                edgecolors="white",
                linewidths=0.4,
            )
        axis.view_init(elev=elev, azim=azim)
        axis.set_title(f"elev={elev}°, azim={azim}°", fontsize=10)
        axis.set_xlabel("t-SNE 1", fontsize=8)
        axis.set_ylabel("t-SNE 2", fontsize=8)
        axis.set_zlabel("t-SNE 3", fontsize=8)
        axis.tick_params(labelsize=6)

    handles, plot_labels = axis.get_legend_handles_labels()
    fig.legend(handles, plot_labels, title="Section", loc="upper right")
    fig.suptitle(
        f"Stylometric 3-D t-SNE of {len(articles)} published articles — four angles "
        f"(PCA preserving {variance:.0%} variance)",
        fontsize=13,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_tsne_3d_html(coords, articles: list[Article], output_path: Path, variance: float) -> None:
    """Interactive (rotatable) 3-D scatter with per-point hover labels."""
    import plotly.graph_objects as go

    sections = sorted({a.section for a in articles})
    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    ]
    color_for = {section: palette[i % len(palette)] for i, section in enumerate(sections)}

    fig = go.Figure()
    for section in sections:
        idx = [i for i, a in enumerate(articles) if a.section == section]
        fig.add_trace(
            go.Scatter3d(
                x=coords[idx, 0],
                y=coords[idx, 1],
                z=coords[idx, 2],
                mode="markers",
                name=f"{section} (n={len(idx)})",
                marker={"size": 5, "color": color_for[section], "opacity": 0.85},
                text=[
                    f"{articles[i].label}<br>{articles[i].title}"
                    f"<br>{articles[i].section} · {articles[i].category}"
                    for i in idx
                ],
                hovertemplate="%{text}<extra></extra>",
            )
        )
    fig.update_layout(
        title=(
            f"Stylometric 3-D t-SNE of {len(articles)} published articles "
            f"(PCA preserving {variance:.0%} variance)"
        ),
        scene={
            "xaxis_title": "t-SNE dimension 1",
            "yaxis_title": "t-SNE dimension 2",
            "zaxis_title": "t-SNE dimension 3",
        },
        legend_title="Section",
    )
    fig.write_html(str(output_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract stylometric features from published articles, reduce them with "
            "PCA (configurable variance threshold), and visualize with t-SNE."
        )
    )
    parser.add_argument(
        "--dir",
        action="append",
        dest="dirs",
        default=None,
        help=(
            "Content directory to scan (repeatable). "
            f"Default: {', '.join(DEFAULT_DIRS)}."
        ),
    )
    parser.add_argument(
        "--variance",
        type=float,
        default=DEFAULT_VARIANCE,
        help=f"Share of variance PCA must preserve, 0-1 (default {DEFAULT_VARIANCE}).",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for the generated artifacts (default {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--perplexity",
        type=int,
        default=None,
        help="t-SNE perplexity (default: auto from the number of articles).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"Random seed for PCA and t-SNE (default {DEFAULT_SEED}).",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Skip rendering the t-SNE scatter plot.",
    )
    return parser.parse_args()


def main() -> int:
    import pandas as pd
    from joblib import dump

    args = parse_args()
    if not 0.0 < args.variance <= 1.0:
        print(
            f"{ANSI_RED}✗ --variance must be in (0, 1], got {args.variance}{ANSI_RESET}",
            file=sys.stderr,
        )
        return 1

    content_dirs = [Path(d) for d in (args.dirs or DEFAULT_DIRS)]
    output_dir = Path(args.output_dir)

    print()
    print(f"{ANSI_BLUE}=== Stylometric Feature Analysis ==={ANSI_RESET}")
    print(f"  scanning: {', '.join(str(d) for d in content_dirs)}")

    articles = discover_articles(content_dirs)
    if len(articles) < 3:
        print(
            f"{ANSI_RED}✗ need at least 3 published articles, found "
            f"{len(articles)}{ANSI_RESET}",
            file=sys.stderr,
        )
        return 1
    print(f"{ANSI_GREEN}  found {len(articles)} published articles{ANSI_RESET}")

    print(f"{ANSI_BLUE}  extracting stylometric features…{ANSI_RESET}")
    numeric = extract_features(articles)
    print(f"{ANSI_GREEN}  extracted {numeric.shape[1]} numeric features/article{ANSI_RESET}")

    output_dir.mkdir(parents=True, exist_ok=True)
    labels = labels_frame(articles)

    raw = pd.concat([labels, numeric], axis=1)
    raw_path = output_dir / "features_raw.parquet"
    raw.to_parquet(raw_path, index=False)

    print(f"{ANSI_BLUE}  reducing with PCA (preserve {args.variance:.0%} variance)…{ANSI_RESET}")
    pipeline, reduced, ratios = run_pca(numeric, args.variance, args.seed)
    n_components = reduced.shape[1]
    preserved = float(ratios.sum())
    print(
        f"{ANSI_GREEN}  {numeric.shape[1]} → {n_components} components "
        f"(preserve {preserved:.1%} of variance){ANSI_RESET}"
    )

    pca_cols = [f"PC{i + 1}" for i in range(n_components)]
    pca_frame = pd.concat(
        [labels, pd.DataFrame(reduced, columns=pca_cols)], axis=1
    )
    pca_path = output_dir / "features_pca.csv"
    pca_frame.to_csv(pca_path, index=False)

    variance_frame = pd.DataFrame(
        {
            "component": pca_cols,
            "explained_variance_ratio": ratios,
            "cumulative_variance_ratio": ratios.cumsum(),
        }
    )
    variance_path = output_dir / "pca_explained_variance.csv"
    variance_frame.to_csv(variance_path, index=False)

    model_path = output_dir / "pca_pipeline.joblib"
    dump(pipeline, model_path)

    importance = feature_importance(pipeline, numeric.columns, ratios)
    importance_path = output_dir / "feature_importance.md"
    write_feature_importance_md(
        importance, importance_path, len(articles), n_components, preserved
    )
    top = importance.iloc[0]
    print(
        f"{ANSI_GREEN}  ranked {len(importance)} features by variance contribution "
        f"(top: {top.feature}, {top.relative_importance_pct:.2f}%){ANSI_RESET}"
    )

    n_samples = reduced.shape[0]
    perplexity = resolve_perplexity(n_samples, args.perplexity)
    print(
        f"{ANSI_BLUE}  projecting to 2-D and 3-D with t-SNE "
        f"(perplexity={perplexity})…{ANSI_RESET}"
    )

    coords_2d = run_tsne(reduced, perplexity, args.seed, 2)
    tsne_2d_path = output_dir / "tsne_2d.csv"
    pd.concat([labels, pd.DataFrame(coords_2d, columns=["x", "y"])], axis=1).to_csv(
        tsne_2d_path, index=False
    )

    coords_3d = run_tsne(reduced, perplexity, args.seed, 3)
    tsne_3d_path = output_dir / "tsne_3d.csv"
    pd.concat(
        [labels, pd.DataFrame(coords_3d, columns=["x", "y", "z"])], axis=1
    ).to_csv(tsne_3d_path, index=False)
    print(f"{ANSI_GREEN}  t-SNE done{ANSI_RESET}")

    plot_2d_path = output_dir / "stylometry_tsne.png"
    plot_3d_png_path = output_dir / "stylometry_tsne_3d.png"
    plot_3d_html_path = output_dir / "stylometry_tsne_3d.html"
    if args.no_plot:
        plot_2d_path = plot_3d_png_path = plot_3d_html_path = None  # type: ignore[assignment]
    else:
        plot_tsne(coords_2d, articles, plot_2d_path, args.variance)
        plot_tsne_3d_png(coords_3d, articles, plot_3d_png_path, args.variance)
        plot_tsne_3d_html(coords_3d, articles, plot_3d_html_path, args.variance)

    print()
    print(f"{ANSI_GREEN}✓ analyze-stylometry complete{ANSI_RESET}")
    print(f"  raw features     {raw_path}")
    print(f"  pca vectors      {pca_path}")
    print(f"  pca variance     {variance_path}")
    print(f"  pca model        {model_path}")
    print(f"  feature ranking  {importance_path}")
    print(f"  tsne 2-d         {tsne_2d_path}")
    print(f"  tsne 3-d         {tsne_3d_path}")
    if plot_2d_path is not None:
        print(f"  tsne 2-d plot    {plot_2d_path}")
        print(f"  tsne 3-d plot    {plot_3d_png_path}")
        print(f"  tsne 3-d html    {plot_3d_html_path}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
