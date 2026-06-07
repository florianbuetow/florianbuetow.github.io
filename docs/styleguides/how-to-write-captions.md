# Caption Style Guide

## Purpose

This guide defines how captions should sound once captionable content has already been identified. It controls tone, density, sentence structure, opening strategy, and publication-like style.

It is intentionally separate from `SKILL.md`, which determines what belongs in the caption.

## Non-goals

Do not use this guide to decide:

- Whether a visual is captionable.
- What facts should be extracted from a visual.
- Whether a chart, table, diagram, or photograph contains enough information to caption.
- What metadata is missing.

Those decisions belong to the content discovery skill.

## Core style principle

A strong caption does not merely describe what the reader can already see. It adds context, names the subject, clarifies the point, defines visual conventions, and helps the reader understand why the visual matters.

## Universal style rules

- Put the main point early.
- Add non-obvious context.
- Use specific nouns, names, places, units, dates, species, instruments, or datasets when relevant.
- Avoid empty openings such as “This image shows,” “The above figure shows,” or “Here we see.”
- Do not repeat the headline, chart title, or visible axis labels unless needed for clarity.
- Do not describe every visible element mechanically.
- Do not overstate causality, certainty, or scope.
- Do not use promotional language.
- Define symbols, colors, lines, markers, abbreviations, scale bars, and statistical marks when they are needed for interpretation.
- Prefer concise captions, but make research figures self-contained when required.

## Style profiles

### 1. Magazine / editorial

Use this profile for Scientific American-inspired science writing, feature journalism, public-facing articles, newsletters, and general-interest explainers.

Style:

- Concrete, concise, readable, and lightly narrative.
- Curious but not sensational.
- Specific rather than generic.
- Contextual rather than procedural.

Rules:

- Lead with the interesting part, not the obvious visible inventory.
- Use a familiar reference or metaphor only when it clarifies the science.
- Add context outside the frame.
- Prefer plain language over specialist jargon.
- Usually use 1 to 3 sentences.
- Avoid self-referential phrasing about the writer, photographer, or article unless necessary.
- Avoid duplicating the article headline or summary.

Preferred openings:

- `[Specific subject] at/in [setting], where [non-obvious significance].`
- `[Event or subject], captured [time/circumstance], illustrates [broader context].`
- `[Familiar reference or hook]. [Scientific subject] does/means [specific point].`

### 2. Journal / research

Use this profile for Nature-like figure legends, formal scientific articles, technical reports, lab reports, and research papers.

Style:

- Precise, neutral, self-contained, and information-dense.
- Declarative when the figure supports a finding.
- Structured rather than narrative.
- Focused on interpretation rather than atmosphere.

Rules:

- Begin with a brief whole-figure title sentence.
- State the main finding early when the figure supports a result.
- Describe panels in order when panels are present.
- Define abbreviations, symbols, colors, shading, line styles, markers, scales, units, and statistical notation.
- Define error bars and statistical tests when shown.
- Use scale bars rather than magnification factors for microscopy and similar images when possible.
- If the manuscript has a Methods section, avoid method details in the caption except what is essential for interpretation.
- If no Methods section exists, include only minimal method detail needed to understand the figure.
- Use a 300-word ceiling for strict Nature-style figure legends unless the target journal allows more.
- Use a 350-word ceiling for Nature Communications-style legends when that target is explicitly requested.
- Avoid decorative, dramatic, humorous, or promotional phrasing.

Preferred opening:

- `Figure X. [Whole-figure finding or purpose].`

Preferred panel structure:

- `(a) [Panel a contribution]. (b) [Panel b contribution]. (c) [Panel c contribution].`

### 3. Educational / explainer

Use this profile for textbooks, museum labels, learning materials, onboarding documents, and public technical explainers.

Style:

- Plain-language, explanatory, and patient.
- More explicit than editorial style.
- Less dense than journal style.

Rules:

- Name the system, process, or relationship clearly.
- Define unfamiliar terms when needed.
- Explain arrows, colors, icons, panels, or sequences.
- Use analogy sparingly and only when it reduces confusion.
- Keep the reading burden low.
- Prefer 1 to 3 sentences.

Preferred openings:

- `Diagram of [process], showing how [input] becomes [output].`
- `Illustration of [system], highlighting [relationship or mechanism].`

### 4. Internal / product / operations

Use this profile for internal documentation, dashboards, analytics summaries, product specs, and operational reports.

Style:

- Direct, functional, and decision-oriented.
- Low flourish.
- Optimized for fast interpretation.

Rules:

- Start with the operational takeaway.
- Identify the metric, segment, timeframe, or system state.
- Define thresholds, baselines, cohorts, and caveats.
- Avoid editorial hooks.
- Prefer 1 to 2 sentences.

Preferred openings:

- `[Metric] changed by [amount] during [timeframe], mainly due to [driver].`
- `[Dashboard/table] compares [groups] across [metric] for [scope].`

## Style dimensions

Teams may customize these knobs without changing the content discovery skill.

### Voice

- `neutral`: restrained, factual, low-flourish.
- `editorial`: vivid, concrete, inviting.
- `pedagogical`: explanatory, clarifying, accessible.
- `formal`: technical, dense, journal-like.
- `operational`: direct, metric-driven, action-oriented.

### Opening strategy

- `context_hook`: best for editorial photos and feature illustrations.
- `declarative_takeaway`: best for graphs, charts, tables, and research figures.
- `system_identification`: best for diagrams and technical illustrations.
- `comparison_summary`: best for tables and grouped charts.

### Density

- `light`: minimal context, usually one sentence.
- `standard`: enough context for confident interpretation.
- `dense`: includes conventions, methods, scales, units, and statistics.

### Sentence count

- `short`: 1 sentence.
- `standard`: 1 to 2 sentences.
- `extended`: 2 to 4 sentences.
- `legend`: as long as needed for self-contained research interpretation, within the target publication limit.

## Style by visual type

### Photographs

The caption should read like contextualized observation, not inventory.

Do:

- Name the subject.
- Add setting, timing, or circumstance when relevant.
- Explain why the moment matters.
- Add context outside the frame.
- Use vivid but restrained language for editorial contexts.

Avoid:

- “A scientist looks at a machine.”
- “The photo shows…”
- Unsupported emotional description.
- Photographer-centered commentary unless relevant.

Pattern:

- `[Subject] at/in [setting], where [specific scientific, historical, or narrative significance].`

### Technical photographs, microscopy images, and scans

The caption should be precise and grounded.

Do:

- Name the sample, instrument, tissue, organism, or material.
- Define color channels, stains, annotations, and scale bars.
- State the visible evidence or technical relevance.
- Mention false color or processed imaging when needed.

Pattern:

- `[Image type] of [sample/system], highlighting [feature]. [Scale/channel/annotation definitions].`

### Graphs, charts, and plots

The caption should open with the key pattern, not the chart type.

Do:

- State the main trend or comparison first.
- Identify what is plotted.
- Define units, groups, time range, and uncertainty marks as needed.
- Keep editorial captions readable and research captions self-contained.

Avoid:

- “This chart shows X versus Y.”
- Repeating every axis label.
- Hiding the takeaway in the final sentence.

Patterns:

- `[Main finding]. [Variables and conditions]. [Units, uncertainty, or statistical notes].`
- `[Outcome] increases/decreases with [predictor] across [condition]. [Error bars/intervals] indicate [definition].`

### Tables

The caption should state the table's purpose or main comparison. It should not narrate every cell.

Do:

- Use a short title-style opening.
- Identify the comparison, scope, or dataset.
- Define units, abbreviations, symbols, footnotes, and formatting conventions.
- Define statistical ranges or error-analysis standards when present.
- Mention source or timeframe when needed.

Avoid:

- Repeating all rows and columns in prose.
- Leaving bold, italics, symbols, or ranges undefined when they encode meaning.
- Using a vague title such as “Results table.”

Patterns:

- `Table X. [Main comparison or purpose]. Values are [unit/scope]; [symbols/ranges] indicate [definition].`
- `Table X. [Dataset or cohort] by [main grouping]. [Notes define abbreviations, units, and statistical conventions].`

### Illustrations and conceptual artwork

The caption should explain the concept, not pretend the illustration is literal evidence.

Do:

- Name the depicted system or phenomenon.
- State the relationship or mechanism the reader should notice.
- Explain simplification when it matters.
- Define labels, arrows, colors, or spatial conventions.

Pattern:

- `Illustration of [system/process], showing how [mechanism or relationship] leads to [effect].`

### Diagrams and process flows

The caption should clarify structure, sequence, or flow.

Do:

- Name the process or architecture.
- Identify inputs, outputs, stages, and relationships.
- Define arrows, colors, boxes, icons, and groupings.
- Distinguish data flow, causality, hierarchy, and time sequence.

Pattern:

- `Diagram of [process], with arrows indicating [flow/sequence] and colors indicating [grouping/status].`

### Maps

The caption should orient the reader geographically and define the mapped variable.

Do:

- Name the location or geographic scope.
- State what is mapped.
- Include the relevant timeframe.
- Define color ramps, symbols, boundaries, scale, or missing-data treatment.

Pattern:

- `Map of [geography] showing [mapped variable] during [timeframe]. [Colors/symbols/boundaries] indicate [definition].`

### Multi-panel figures

The caption should be ordered and economical.

Do:

- Start with the whole-figure claim or purpose.
- Describe panels in order.
- Define shared conventions once.
- Include scale, units, abbreviations, and statistics where needed.

Pattern:

- `Figure X. [Whole-figure takeaway]. (a) [Panel a]. (b) [Panel b]. (c) [Panel c]. [Shared scale, units, symbols, and statistical notes].`

### Infographics

The caption should summarize the central message and help readers navigate the visual hierarchy.

Do:

- State the main message.
- Identify the scope or data source when relevant.
- Explain icon, color, or section logic only when it aids interpretation.
- Keep the caption shorter than the infographic itself.

Pattern:

- `[Central message]. The infographic organizes [topic] by [sections/categories], with [visual convention] indicating [meaning].`

## Example bank

All examples below are model examples for style calibration, not publication quotations.

### Editorial photograph examples

**Example 1**

Inside a Penning trap at the National Institute of Standards and Technology in Boulder, Colorado, a superconducting magnet helps hold beryllium ions for a quantum-sensing experiment. The setup is sensitive to weak electric-field signals that may help researchers test axion dark-matter candidates.

**Why it works**

It names the instrument, location, and scientific significance rather than merely describing laboratory equipment.

**Example 2**

Field researchers collect ice-core samples in coastal Greenland, where trapped air bubbles preserve traces of past atmospheric conditions. The work looks logistical in the frame, but each core functions as a time capsule for reconstructing climate history.

**Why it works**

It adds context outside the frame and explains why the photographed action matters.

**Example 3**

Web-spinners are insects with an anatomical trick usually reserved for comic-book heroes: they spin silk from swollen segments in their forelegs. This specimen, *Haploembia solieri*, was photographed in Lake County, California.

**Why it works**

It uses a familiar reference, then anchors the caption with a specific species and location.

### Graph and chart examples

**Example 4**

Figure 1. Ammonium sulfate treatment increases tomato plant growth rate. Control plants received no treatment, whereas treated plants received ammonium sulfate at week 1; plotted values show means and error bars represent standard error of the mean.

**Why it works**

It opens with the finding, then gives the minimum experimental framing needed to interpret the chart.

**Example 5**

Figure 2. Model accuracy improves with retrieval depth up to 16 passages, after which gains plateau. Exact-match score is plotted against retrieved passage count across three evaluation sets; shaded bands indicate 95% confidence intervals.

**Why it works**

It states the trend first, defines the plotted relationship, and explains uncertainty marks.

**Example 6**

Battery range climbed quickly from 2016 to 2022, then grew more gradually as mainstream electric vehicles converged on larger packs and more efficient drivetrains. The curve marks the shift from niche city cars to vehicles designed for intercity travel.

**Why it works**

It translates a chart into a reader-facing story without drowning the caption in methods.

### Table examples

**Example 7**

Table 1. Retrieval-augmented models improve accuracy most on fact-heavy questions but add latency. Accuracy is exact match; latency is median wall-clock time in seconds, and ranges indicate bootstrap 95% confidence intervals.

**Why it works**

It gives the table's purpose, defines metrics, and explains the statistical range convention without restating every cell.

**Example 8**

Table 2. Candidate materials ranked by conductivity, cost, and thermal stability. Values are reported at room temperature unless noted; bold entries mark the best value within each column.

**Why it works**

It states the comparison and explains the formatting convention that affects interpretation.

### Illustration and diagram examples

**Example 9**

Illustration of a black hole's accretion disk, with hot gas spiraling inward while light bends around the event horizon. The image simplifies the physics but highlights two ideas that matter most for readers: extreme gravity and distorted light paths.

**Why it works**

It distinguishes conceptual artwork from literal observation and tells the reader what to notice.

**Example 10**

Diagram of retrieval-augmented generation, showing how a user query is embedded, matched against a vector index, and passed with retrieved passages into a language model. Repeated colors indicate components that share state, and arrows show data flow rather than timing.

**Why it works**

It defines the process and clarifies visual conventions.

### Map example

**Example 11**

Map of North Atlantic sea-surface temperature anomalies during July 2025. Warmer colors indicate temperatures above the 1991–2020 average, and gray areas mark regions with insufficient observations.

**Why it works**

It identifies the geography, variable, timeframe, baseline, and missing-data convention.

### Multi-panel figure examples

**Example 12**

Figure 3. Amyloid-beta plaques co-localize with activated microglia in the hippocampus of 12-month-old APP/PS1 mice. (a) Amyloid-beta staining. (b) Iba1-positive microglia. (c) Merged image showing spatial overlap. Scale bar, 50 micrometers; significance assessed by two-tailed t-test.

**Why it works**

It gives the whole-figure claim, maps each panel, and includes scale and statistical context.

**Example 13**

Figure 4. Tool-augmented agents reduce hallucination rate but increase latency relative to direct generation. (a) Hallucination rate across prompting, retrieval-augmented generation, and tool-use conditions. (b) Median task latency by condition. (c) Accuracy-latency frontier. Error bars show bootstrap 95% confidence intervals across 1,000 evaluation tasks.

**Why it works**

It follows a formal figure-legend structure while staying applicable to AI engineering research.

## Before-and-after rewrites

| Weak caption | Better caption | Why it improves |
|---|---|---|
| The graph shows sales over time. | Sales doubled between Q1 and Q4, with the steepest gains after the product launch in June. Monthly revenue is plotted in euros; the dashed line marks the campaign start. | States the pattern first and adds the interpretive marker. |
| Scientists work in a lab. | A cryogenic ion-trap experiment at NIST in Boulder, Colorado, uses a superconducting magnet to detect weak electric-field signals relevant to axion searches. | Adds identity, place, and scientific significance. |
| Diagram of how the model works. | Diagram of a retrieval-augmented generation pipeline, showing query embedding, nearest-neighbor retrieval, and prompt assembly before final model inference. | Replaces vague phrasing with mechanism and sequence. |
| Results table. | Table 1. Treatment outcomes by cohort and dosage group. Values are percentages unless noted; parentheses indicate 95% confidence intervals. | States the table purpose and defines units and ranges. |
| A map of Europe. | Map of European heatwave intensity during July 2025, with darker shading indicating larger departures from the 1991–2020 average. | Replaces generic geography with variable, timeframe, and color meaning. |

## Anti-patterns

Avoid:

- “This image shows …” when a stronger opening is possible.
- “Pictured above …” or “In the above figure …”
- “Interesting,” “important,” or “significant” without saying why.
- Repeating labels already visible in the figure.
- Using unexplained abbreviations or symbols.
- Describing every visible object with no takeaway.
- Hiding the finding at the end of an analytical caption.
- Including full methods in a Nature-like figure legend when a Methods section exists.
- Treating conceptual illustrations as direct evidence.
- Using jokes or metaphors in journal-style captions.
- Overloading editorial captions with statistical detail that belongs in the article body.

## Quality checklist

Before finalizing a caption, confirm:

- The caption matches the selected profile.
- The main point appears early.
- The caption adds value beyond the visual.
- The language is specific and concrete.
- The caption is concise for its context.
- Technical markers are defined where needed.
- Graphs, charts, and tables state the key pattern or purpose.
- Multi-panel figures identify the whole-figure point and panel order.
- Journal-style captions are neutral and self-contained.
- Editorial captions are readable and contextual without becoming promotional.
- The caption does not contain unsupported claims.

## Customization block

Use this block to adapt the guide for a specific team or publication.

```yaml
default_profile: editorial
voice: concrete, readable, restrained
sentence_count: standard
opening_strategy: context_hook_for_photos_declarative_takeaway_for_data
allowed_jargon_level: moderate
metaphor_allowed: true
statistics_detail: standard
caption_length:
  editorial: 1-3 sentences
  educational: 1-3 sentences
  journal: target_publication_limit
nature_like_rules:
  brief_whole_figure_title: true
  panel_descriptions: true
  define_symbols_and_statistics: true
  avoid_methods_when_methods_section_exists: true
  strict_word_limit: 300
```

## Reference rule

A caption-writing workflow should apply this guide only after the content discovery step has already produced a caption payload. The skill determines what the caption should contain; this guide determines how the caption should sound.
