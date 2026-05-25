# TODO

## Review tags for all ticker articles

Add a "Ticker News" tag to every ticker article (in addition to the "Ticker News" category already added). Review all other tags for consistency at the same time. Edit each file individually.

## American English vs British English in spell checking

### The problem

`harper-cli` is configured for the **American English** dialect. Many articles on this blog — particularly interviews with European engineers — are written in or naturally drift toward **British English**. This causes a recurring class of false-positive spell-check failures that are not real errors but dialect differences.

### What harper-cli currently checks for (dialect: American)

Harper flags British spellings as misspelled because they are not in the American dictionary. Common categories:

- **-ise/-ize**: `realise`, `recognise`, `specialise`, `incentivise`, `centralise`, `normalise` → American uses `-ize`
- **-our/-or**: `behaviour`, `colour`, `honour` → American drops the `u`
- **-re/-er**: `centre`, `theatre` → American uses `-er`
- **-wards/-ward**: `afterwards` → American prefers `afterward`
- **Standalone words**: `maths` → American uses `math`

### What we typically find in articles

From the spell-check run on `2026-05-25-interview-from-classical-guitar-to-ruby-on-rails/index.md`:

- 28 spelling issues, of which the majority are British spellings, not actual errors
- Proper nouns not in the dictionary: `ScoreBase`, `MusicXML`, `FernUni`, `Magdeburg`, `moguls753`, `LeetCode`
- A small number of genuine issues mixed in (typos, split words, missing prepositions)

### Pending replacements for `2026-05-25-interview-from-classical-guitar-to-ruby-on-rails/index.md`

Apply these to convert to American English:

| Find | Replace |
|------|---------|
| `realised` | `realized` |
| `recognise` | `recognize` |
| `afterwards` | `afterward` |
| `theatre` | `theater` |
| `incentivised` | `incentivized` |
| `specialise` | `specialize` |
| `behaviour` | `behavior` |
| `normalised` | `normalized` |
| `centralising` | `centralizing` |
| `maths` | `math` |
| `centre` | `center` |
| `realise` | `realize` |

### Options to consider

1. **Apply replacements per article** — manually convert British spellings to American as part of the editing workflow. Most consistent with the checker's dialect setting.
2. **Add British spellings to `config/harper/dictionary.txt`** — suppresses the false positives but does not enforce a consistent dialect across articles.
3. **Switch harper-cli dialect to British English** — eliminates the false positives entirely but then American spellings would be flagged instead. Not recommended if American English is the intended house style.
4. **Document house style** — pick American English as the explicit standard and add a note to the article authoring docs so authors know to use American spellings from the start.

## Lighthouse CI hard-failure ratchet

### The current state

Lighthouse CI is integrated as local tooling and CI validation through `just run-lighthouse-checks`. It audits the built `public/` site through an LHCI-managed temporary static server, so it does not conflict with the normal Hugo dev server.

The first baseline run surfaced existing issues that are currently configured as warnings so the tool can be adopted without immediately blocking unrelated work:

- Color contrast
- Browser console errors
- Image delivery and responsive image sizing
- Missing explicit image dimensions
- Missing meta descriptions
- Render-blocking requests
- Touch target size
- LCP discovery on the projects page

### Recommendation

Once the known baseline issues are fixed, ratchet the Lighthouse config from warnings to hard failures. The target policy should be: if Lighthouse surfaces an issue, the build fails until the issue is addressed or there is a deliberate documented exception.

This should happen in stages:

1. Fix the known baseline issues while they are still warnings.
2. Change the warning assertions in `lighthouserc.js` to `error`.
3. Keep category thresholds as hard gates for performance, accessibility, best practices, and SEO.
4. Require any future exception to be explicit in `lighthouserc.js`, with a short comment explaining why it is tolerated.

The end state should be strict: Lighthouse should stop regressions before publishing, not just generate reports after the fact.

## Human visual QA screenshots

### The idea

Add a tooling target that captures screenshots of the built blog across common device classes so a human can inspect visual regressions after CI or local validation.

The screenshot set should cover at least:

- Desktop
- Tablet
- Mobile

Use a browser automation tool such as Playwright CLI to load representative routes and save screenshots for later inspection.

### Requirements to design

- The screenshot command needs a running local service. Prefer a temporary server for the built `public/` output so it does not conflict with `just dev`.
- The command should capture representative pages, likely matching the Lighthouse route set: `/`, `/blog/`, `/ticker/`, `/projects/`, and `/resources/`.
- The command should use explicit viewport sizes for each device class.
- Screenshots should be written to a predictable local artifact directory.
- The artifact directory must be ignored by git so generated screenshots are never committed accidentally.
- The output should be easy to inspect manually, with filenames that include the route and device class.

### Suggested shape

Add future `just` targets along these lines:

1. `run-screenshot-checks` — build the site, start a temporary local static server, capture screenshots, then stop the server.
2. `screenshots-clean` — remove generated screenshot artifacts.
3. `screenshots-open` — open the generated screenshot directory or representative screenshots for review.

Suggested ignored artifact path:

```text
reports/screenshots/
```

The end state should be a lightweight human quality-control workflow: automated capture, no git noise, and clear screenshot artifacts that can be inspected before publishing.
