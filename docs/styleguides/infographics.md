# STYLEGUIDE.md — Infographics for Science & AI Engineering

## 1. Purpose and voice
Infographics explain complex scientific and technical systems (biology, climate, AI architectures, algorithms) to an intelligent general audience. [gooddata](https://www.gooddata.ai/blog/5-data-visualization-best-practices/)

- Clarity over cleverness: every visual choice must improve understanding, not just aesthetics. [datylon](https://www.datylon.com/blog/a-guide-to-data-visualization-best-practices)
- Neutral, authoritative tone with a sense of curiosity; no hype or marketing language. [linkedin](https://www.linkedin.com/posts/wenceslas-mbelani4_infographics-datavisualization-promptengineering-activity-7414772826303455232-TnLo)
- Each graphic answers one core question (e.g., “How retrieval-augmented generation works end-to-end?”). [libguides.hull.ac](https://libguides.hull.ac.uk/infographics/making)

Before designing, write a one-sentence thesis for the infographic and use it to decide what stays or goes. [linkedin](https://www.linkedin.com/posts/wenceslas-mbelani4_infographics-datavisualization-promptengineering-activity-7414772826303455232-TnLo)

***
## 2. Layout and structure
Use modular, grid-based layouts that work both for scientific topics (e.g., ecosystems) and technical topics (e.g., C4 diagrams, model pipelines). [medium](https://medium.com/@jancalve/writing-good-software-architecture-diagrams-15c51eca4ce7)

- One hero panel (main story) plus 2–6 supporting panels (mechanism, comparison, zoom-ins, timelines). [storybench](https://www.storybench.org/how-scientific-american-makes-its-infographics/)
- For technical content, consider stacked abstraction: top panel = conceptual overview, lower panels = data flow, components, trade-offs. [kstd.thriving](https://kstd.thriving.dev/guide/architecture-diagrams-best-practices/)
- Align everything to a consistent grid; avoid overlapping elements and decorative diagonals that break hierarchy. [linkedin](https://www.linkedin.com/posts/wenceslas-mbelani4_infographics-datavisualization-promptengineering-activity-7414772826303455232-TnLo)

Reading order should be obvious (top-to-bottom or left-to-right, Z-pattern), optionally reinforced with section numbers or subtle arrows. [m3.material](https://m3.material.io/blog/data-visualization-accessibility)

***
## 3. Typography
Typography is functional and quiet, optimized for long-form reading and annotations. [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)

- Fonts:  
  - Body, labels, axes: clean sans-serif (e.g., Helvetica/Arial equivalents). [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
  - Code snippets / pseudo-code: monospaced. [medium](https://medium.com/@jancalve/writing-good-software-architecture-diagrams-15c51eca4ce7)
- Suggested sizes (print-equivalent):  
  - Title: 16–24 pt  
  - Subtitle/deck: 11–14 pt  
  - Body: 8–10 pt  
  - Labels/axes: 6–8 pt (never below 5 pt) [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
- Use weight and size for hierarchy; reserve all caps for short tags (e.g., “INPUT”, “TRAINING PHASE”). [conceptviz](https://conceptviz.app/blog/scientific-infographic-design-complete-guide)

Text must stay high-contrast on light backgrounds; if over imagery, use a subtle solid or semi-opaque text panel. [m3.material](https://m3.material.io/blog/data-visualization-accessibility)

***
## 4. Color and accessibility
Color encodes structure, flow, and data while remaining accessible. [m3.material](https://m3.material.io/blog/data-visualization-accessibility)

- Palette:  
  - Base: off-white background, neutral grays for structure. [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
  - Core hues: 4–8 colorblind-safe colors for data and categories (e.g., input, model, memory, evaluation). [nature](https://www.nature.com/articles/s41551-017-0079)
- Semantic roles for technical infographics:  
  - Blue/teal: data and information flow  
  - Purple: models/algorithms  
  - Orange/yellow: user interaction, prompts, UI  
  - Red: errors, risks, failure modes  
  - Green: metrics, improvements, “good” outcomes [datylon](https://www.datylon.com/blog/a-guide-to-data-visualization-best-practices)

Maintain WCAG-compliant contrast; use color plus shape/position (e.g., dashed vs solid line) for key distinctions, not color alone. [m3.material](https://m3.material.io/blog/data-visualization-accessibility)

***
## 5. Charts and quantitative graphics
Charts follow scientific best practices but are often annotated for engineering narratives (benchmarks, latency, cost, scaling). [gooddata](https://www.gooddata.ai/blog/5-data-visualization-best-practices/)

- Always label axes with units; show baselines clearly and avoid misleading truncation. [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
- Prefer: line charts (scaling curves, learning curves), dot/bar plots (benchmark comparisons), stacked bar/area for resource breakdown. [datylon](https://www.datylon.com/blog/a-guide-to-data-visualization-best-practices)
- Show data points or distributions when possible (e.g., jittered dots over box/violin) instead of only summary stats. [nature](https://www.nature.com/articles/s41551-017-0079)

Use minimal gridlines and direct labeling where possible. Use consistent scales across related panels (e.g., model sizes in parameters, latency in ms). [datylon](https://www.datylon.com/blog/a-guide-to-data-visualization-best-practices)

***
## 6. Diagrams for systems and architectures
Technical infographics often center on system diagrams (pipelines, agents, services). These should follow a consistent visual language. [medium](https://medium.com/@jancalve/writing-good-software-architecture-diagrams-15c51eca4ce7)

- Levels of abstraction (inspired by C4): [medium](https://medium.com/@jancalve/writing-good-software-architecture-diagrams-15c51eca4ce7)
  - Level 1: Context — user, environment, external systems.  
  - Level 2: Containers — services, applications, data stores (e.g., “Orchestrator”, “Vector DB”).  
  - Level 3: Components — key modules inside containers (e.g., “Retriever”, “Tool Router”).  
- Shape semantics:  
  - Rounded rectangles: active components/services  
  - Rectangles: data stores, indices, files  
  - Capsules/pills: user or external actors  
  - Diamonds (sparingly): decision points or routing logic [kstd.thriving](https://kstd.thriving.dev/guide/architecture-diagrams-best-practices/)

Arrows must indicate direction and type of flow (data, control, feedback). Use arrow styles (solid, dashed, color-coded) and a legend to avoid ambiguity. [reddit](https://www.reddit.com/r/devops/comments/1664mem/are_there_best_practices_and_names_for_cloud/)

***
## 7. Visual patterns for AI/LLM topics
Use repeatable patterns to keep AI diagrams consistent across the blog. [elements.envato](https://elements.envato.com/learn/ai-infographic-design)

- Prompt/response loop:  
  - User bubble → “Prompt & Context Builder” → “Model” → “Post-processor” → User output. [gooddata](https://www.gooddata.ai/blog/5-data-visualization-best-practices/)
- RAG pipeline:  
  - “User query” → “Embed & Retrieve” (vector store) → “Context assembly” → “Model” → “Answer with citations”.  
- Agentic system:  
  - “Agent” modules shown as repeated blocks connected to a central “Orchestrator” or “Planner,” with tools/services as peripheral components. [linkedin](https://www.linkedin.com/posts/wenceslas-mbelani4_infographics-datavisualization-promptengineering-activity-7414772826303455232-TnLo)
- Evaluation & metrics:  
  - Small multiples showing metrics across models/datasets; consistent metric icons/colors (e.g., robustness, latency, cost). [datylon](https://www.datylon.com/blog/a-guide-to-data-visualization-best-practices)

Avoid “sci‑fi” overload; use subtle tech cues (simple circuit lines, node-link diagrams) instead of glowing gradients and random HUD elements. [dribbble](https://dribbble.com/search/ai%20infographic)

***
## 8. Annotation and narrative
Annotations bridge the gap between “what” and “why,” especially for AI engineering trade-offs. [linkedin](https://www.linkedin.com/posts/wenceslas-mbelani4_infographics-datavisualization-promptengineering-activity-7414772826303455232-TnLo)

- Start with a 1–2 sentence deck explaining the key takeaway (e.g., “Adding retrieval reduces hallucinations at the cost of X ms latency.”). [gooddata](https://www.gooddata.ai/blog/5-data-visualization-best-practices/)
- Use concise callouts to annotate:  
  - Key decision points (e.g., “Tool choice based on intent classifier”)  
  - Trade-offs (e.g., “GPU memory bottleneck here”)  
  - Failure modes (e.g., “Unseen schema leads to retrieval miss”) [datylon](https://www.datylon.com/blog/a-guide-to-data-visualization-best-practices)
- Keep figure notes short but honest about assumptions (e.g., test dataset, hardware, model versions). [nature](https://www.nature.com/articles/s41551-017-0079)

Language should be precise but accessible; briefly define core terms (e.g., “vector store: a database that indexes embeddings”) where first introduced. [conceptviz](https://conceptviz.app/blog/how-to-design-infographics-for-scientists)

***
## 9. Data integrity and reproducibility
Technical readers expect repeatability and honest framing. [gooddata](https://www.gooddata.ai/blog/5-data-visualization-best-practices/)

- Always state: dataset/source, model versions, hardware, and date of measurement where relevant. [scientificamerican](https://www.scientificamerican.com/standards-and-ethics/)
- Distinguish:  
  - Measured data (solid lines / opaque bars)  
  - Simulations/estimates (dashed lines / lower opacity)  
  - Hypothetical scenarios (dotted lines, annotated as such). [datylon](https://www.datylon.com/blog/a-guide-to-data-visualization-best-practices)
- Avoid cherry-picking or scale tricks that exaggerate gains; when in doubt, show full range and variability. [nature](https://www.nature.com/articles/s41551-017-0079)

Include a small, consistent “Data & methods” note at the bottom with a link/ID to underlying code or repository when available. [gooddata](https://www.gooddata.ai/blog/5-data-visualization-best-practices/)

***
## 10. Technical production details
Infographics should be tool-agnostic but optimized for a code-first, vector-first workflow. [m3.material](https://m3.material.io/blog/data-visualization-accessibility)

- Workflow: generate base charts/diagrams as SVG (e.g., via Python/JS) → refine layout and annotations in Figma/Illustrator. [beautiful](https://www.beautiful.ai/blog/the-ultimate-guide-to-data-visualization)
- Formats: vector (SVG, PDF) for diagrams and charts; raster (TIFF/PNG) only for photos or complex textures. [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
- Resolution: ≥300 dpi at final size for any raster; avoid exporting whole infographics as flattened bitmaps. [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)

Keep fonts as embedded, live text; maintain a shared component library (colors, arrow styles, shapes) to ensure consistency across the blog. [kstd.thriving](https://kstd.thriving.dev/guide/architecture-diagrams-best-practices/)

***
## 11. Do’s and don’ts (science + AI)
| Aspect          | Do                                                                                  | Avoid                                                                                |
|-----------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Layout          | Modular grids, hero panel + supporting panels, clear abstraction levels  [storybench](https://www.storybench.org/how-scientific-american-makes-its-infographics/) | Single giant “wall” diagram with mixed abstraction levels  [kstd.thriving](https://kstd.thriving.dev/guide/architecture-diagrams-best-practices/)                  |
| Color           | Semantic, accessible palette with roles for data, components, risk  [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/) | Neon gradients, sci-fi glow, red–green-only distinctions  [research-figure-guide.nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)           |
| Diagrams        | Consistent shapes for components/data/users; clear arrows, legends  [medium](https://medium.com/@jancalve/writing-good-software-architecture-diagrams-15c51eca4ce7) | Ad-hoc icons, unlabeled arrows, ambiguous flows  [kstd.thriving](https://kstd.thriving.dev/guide/architecture-diagrams-best-practices/)                    |
| Charts          | Honest scales, labeled units, clear benchmarks  [nature](https://www.nature.com/articles/s41551-017-0079)                     | Axis tricks, cherry-picked ranges, unlabeled baselines  [nature](https://www.nature.com/articles/s41551-017-0079)                      |
| Storytelling    | Explicit takeaways, annotated trade-offs, clear assumptions  [storybench](https://www.storybench.org/how-scientific-american-makes-its-infographics/)        | “Diagram dumps” with no explanation or context  [gooddata](https://www.gooddata.ai/blog/5-data-visualization-best-practices/)                             |
| Production      | Code-generated SVG + manual refinement; shared components  [m3.material](https://m3.material.io/blog/data-visualization-accessibility)         | One-off manually drawn charts, inconsistent styling across posts  [kstd.thriving](https://kstd.thriving.dev/guide/architecture-diagrams-best-practices/)           |

