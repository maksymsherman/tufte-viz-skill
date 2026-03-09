# clean-viz-skill

A Claude Code plugin that applies clean-viz heuristics and an explicit audit workflow to chart-generation requests. Best support is for matplotlib, seaborn, and Plotly; other libraries are covered with secondary reference patterns.

> **Note**: This project is not affiliated with Edward Tufte. It applies visualization principles described in his published works.

## What it does

This skill activates when you ask Claude to create, restyle, or critique a data visualization. It applies these principles:

- **Maximizes data-ink ratio** — removes non-data elements (extra spines, heavy gridlines, decorative fills)
- **Uses range frames** — axis lines span only the data range
- **Direct labeling** — annotations replace legend boxes
- **Serif typography** — clean, readable text
- **Grayscale default** — with a single accent color for emphasis
- **Bans chartjunk** — no pie charts, 3D effects, dual axes, gradient fills, or rainbow colormaps
- **Offers substitutes** — when a banned chart type is requested, suggests a clean alternative
- **Runs a mandatory audit** — code-level checks are always required; rendered checks are only claimed when the chart was actually viewed

## Supported libraries

| Library tier | Libraries | Support |
|---|---|---|
| Primary | matplotlib, seaborn | Most complete patterns — range frames, direct labels, small multiples, sparklines, slope charts |
| Primary | Plotly | Strong patterns — bounded axis-line approximation, annotations, small multiples, sparklines |
| Secondary | Altair, ggplot2 | Useful starting points for themes, faceting, and direct labels |
| Secondary | D3.js, Observable Plot | Pattern sketches to adapt into an existing chart scaffold |

## Installation

### From the plugin marketplace (recommended)

Inside Claude Code, run:

```
/plugin marketplace add maksymsherman/clean-viz-skill
/plugin install clean-viz@maksymsherman-clean-viz-skill
```

You can scope the installation:

```
/plugin install clean-viz@maksymsherman-clean-viz-skill --scope user      # all your projects (default)
/plugin install clean-viz@maksymsherman-clean-viz-skill --scope project   # shared with collaborators
/plugin install clean-viz@maksymsherman-clean-viz-skill --scope local     # this repo only
```

### From a local clone

```bash
git clone https://github.com/maksymsherman/clean-viz-skill.git
claude --plugin-dir /path/to/clean-viz-skill
```

## How it works

The plugin has three layers:

1. **SKILL.md** — Core principles, mandatory rules, banned chart types with substitutes, and a response protocol. This loads whenever a visualization request is detected.

2. **references/** — Library-specific code patterns loaded on demand:
   - `matplotlib-patterns.md` — matplotlib and seaborn
   - `plotly-patterns.md` — Plotly
   - `general-patterns.md` — Altair, D3.js, ggplot2, Observable Plot
   - `checklist.md` — Mandatory quality gate used before finalizing a chart

3. **eval/** — A tracked verification area with:
   - `check_response.py` for policy-regression smoke tests on saved responses
   - `verify_reference_examples.py` for render-checking the runnable Python reference examples in the markdown docs

## Examples

**Request:** "Create a line chart showing monthly revenue"

**Result:** Serif font, range frames, inward ticks, direct labels, no legend box, grayscale palette.

**Request:** "Make a pie chart of market share"

**Result:** Claude explains why pie charts violate data-ink principles, then generates a horizontal bar chart instead.

**Request:** "Create a 3D bar chart"

**Result:** Claude explains occlusion/perspective problems, generates a clean 2D bar chart.

## Visualization principles

Based on Edward Tufte's *The Visual Display of Quantitative Information*:

- **Data-ink ratio**: Maximize the proportion of ink used to present data
- **Graphical integrity**: Visual representation proportional to numerical values (Lie Factor 0.95-1.05)
- **Chartjunk elimination**: Remove all non-data visual elements
- **Small multiples**: Repeated small charts for comparison instead of complex overlaid graphics
- **Sparklines**: Word-sized graphics for inline data display

## Verification Model

The skill uses a mandatory three-part audit:

- **Code checks** — always required before the final answer
- **Rendered checks** — only marked as passed if the chart was actually rendered or visually inspected
- **Session consistency** — used when multiple related charts are produced together

This is deliberate: the checklist remains a hard gate, but the skill is not allowed to fake visual verification when it has not inspected the output.

## Evaluation

The tracked `eval/` harness is a lightweight smoke test for saved responses. It checks policy compliance for canonical prompts such as:

- banned chart substitution
- audit summary presence
- units and direct-label intent
- multi-series distinguishability cues

For render-level verification of the reference examples themselves, run:

```bash
uv run --with matplotlib --with numpy --with seaborn --with plotly --with kaleido --with pandas --with altair --with vl-convert-python python eval/verify_reference_examples.py
```

The script extracts the runnable Python examples directly from the reference markdown, renders them, and writes artifacts to a temporary directory (or a directory you pass with `--output-dir`).

The heavier ChartBench workflow remains local-only and is documented in [CLAUDE.md](CLAUDE.md).

## License

MIT
