---
name: tufte-viz
description: >
  Enforces Edward Tufte's data visualization principles whenever creating charts,
  plots, or visualizations. Triggers on any request involving matplotlib, pyplot,
  seaborn, plotly, altair, d3, ggplot2, Observable Plot, or general terms like
  "chart", "plot", "graph", "visualization", "figure", "histogram", "scatter",
  "bar chart", "line chart", "heatmap", "sparkline", "dashboard".
triggers:
  - matplotlib
  - pyplot
  - seaborn
  - plotly
  - altair
  - d3
  - ggplot2
  - observable plot
  - chart
  - plot
  - graph
  - visualization
  - figure
  - histogram
  - scatter
  - bar chart
  - line chart
  - heatmap
  - sparkline
  - dashboard
  - data visualization
  - small multiples
  - slopegraph
  - slope chart
  - range frame
---

# Tufte Data Visualization Skill

You are now operating under Edward Tufte's data visualization principles. Every chart, plot, or figure you produce MUST follow these rules. There are no exceptions unless the user explicitly overrides a specific rule.

---

## 1. Core Principles

### Data-Ink Ratio
Maximize the share of ink devoted to data. Every element on the plot must either represent data or aid its interpretation. If an element can be removed without loss of information, remove it.

> "Erase non-data-ink, within reason." — Edward Tufte, *The Visual Display of Quantitative Information*

### Graphical Integrity
The visual representation of data must be directly proportional to the numerical quantities represented. The Lie Factor must stay between 0.95 and 1.05:

```
Lie Factor = (size of effect shown in graphic) / (size of effect in data)
```

Violations include: truncated axes that exaggerate differences, area/volume encodings that distort magnitude, inconsistent scales across panels.

### Chartjunk Elimination
Remove all visual elements that do not convey data: decorative fills, moiré patterns, heavy borders, redundant labels, background images, 3D perspective effects, gradient fills, drop shadows, and excessive gridlines.

---

## 2. Mandatory Rules — Always Do

Apply ALL of the following to every visualization:

### Spine & Axis Treatment
- **Remove top and right spines** — they are non-data-ink
- **Use range frames** — bind left/bottom spine extents to the data range (`ax.spines['left'].set_bounds(min_y, max_y)`)
- **Tick marks face inward** — `tick_params(direction='in')`
- **Reduce tick density** — only label meaningful values; avoid matplotlib/plotly defaults

### Typography
- **Use a serif font** — `'serif'` family (or specify Georgia, Palatino, Times New Roman)
- **Title in sentence case** — not ALL CAPS, not Title Case
- **Annotations in data space** — use `ax.text()` or `ax.annotate()` positioned in data coordinates, not as axis labels when labeling specific points

### Labeling
- **Direct labeling over legends** — place text labels next to data series; remove the legend box entirely when possible
- **Annotate key data points** — label maximums, minimums, inflection points, or notable values directly on the plot
- **Remove redundant axis labels** — if the title or context makes the axis meaning obvious, omit the label

### Color
- **Default to grayscale** — use black, dark gray (`#333333`), medium gray (`#888888`), light gray (`#cccccc`)
- **Single accent color** — when emphasis is needed, use exactly one color (default: `#c0392b` muted red)
- **Colorblind-safe palette** — when multiple colors are required, use:
  - `#332288` (indigo), `#88CCEE` (cyan), `#44AA99` (teal), `#117733` (green),
    `#999933` (olive), `#CC6677` (rose), `#882255` (wine), `#AA4499` (purple)
  - This is the Paul Tol colorblind-safe palette
- **Never use rainbow/jet colormaps** — use sequential single-hue (grays, blues) or diverging (blue-white-red) instead

### Layout & Density
- **Prefer small multiples** over complex single charts with many series
- **High data density** — aim for at least 50 data points per square inch where appropriate
- **Minimal margins** — `tight_layout()` or equivalent; remove excessive whitespace

---

## 3. Mandatory Rules — Never Do

### Banned Chart Types
Do NOT generate these chart types. If the user requests one, explain the Tufte principle being violated and offer the substitute from the table below.

| Requested Type | Problem | Substitute |
|---|---|---|
| Pie chart | Area perception is poor; low data-ink ratio | Horizontal bar chart or dot plot |
| Donut chart | Same as pie with wasted center space | Horizontal bar chart or dot plot |
| 3D bar chart | Perspective distorts values; occlusion | 2D bar chart |
| 3D surface plot | Occlusion; impossible to read values | Heatmap or contour plot |
| 3D scatter | Occlusion; no depth perception on screen | 2D scatter with size/color encoding |
| Dual-axis chart | Implies false correlation; confusing scales | Small multiples (shared x-axis) |
| Exploded pie | All pie problems plus spatial distortion | Horizontal bar chart |
| Gauge/speedometer | Single-value display with enormous chrome | Plain number with sparkline context |
| Word cloud | Area encoding is unreliable; no ordering | Horizontal bar chart of term frequencies |
| Radar/spider chart | Angle encoding is misleading; area distortion | Small multiples of bar charts or dot plots |
| Stacked area (>3 series) | Middle series are impossible to read | Small multiples of line charts |
| Bubble chart | Area perception is poor | Scatter with direct labels |

### Banned Visual Elements
- **No background colors or images** — white background only
- **No gradient fills** — solid colors only
- **No drop shadows** — on any element
- **No 3D perspective effects** — ever
- **No heavy gridlines** — if gridlines are needed, use thin light gray (`#eeeeee`) or white-on-bar technique
- **No decorative borders or boxes** — around legends, titles, or annotations
- **No ALL CAPS text** — in titles, labels, or annotations
- **No rotated tick labels** — if labels are too long, use a horizontal bar chart or abbreviate

---

## 4. Library-Specific Patterns

When generating code, load the appropriate reference file for concrete code patterns:

### Python — matplotlib / seaborn
Read `references/matplotlib-patterns.md` for:
- Base `rcParams` configuration
- `apply_range_frame()` helper function
- Direct labeling patterns
- Tufte bar chart (white gridlines)
- Line plot with dot emphasis
- Slope chart implementation
- Sparkline function
- Small multiples template
- Seaborn overrides
- Color palette definitions

### Python — Plotly
Read `references/plotly-patterns.md` for:
- `TUFTE_LAYOUT` base template
- Range frame axis configuration
- Direct annotation patterns
- Small multiples with `make_subplots`
- Sparkline configuration

### Other Libraries (Altair, D3.js, ggplot2, Observable Plot)
Read `references/general-patterns.md` for:
- Altair theme configuration
- D3.js spine removal and serif font patterns
- R/ggplot2 `theme_tufte()` and `geom_rangeframe()`
- Observable Plot styling

---

## 5. Sparklines

Sparklines are intense, simple, word-sized graphics. When creating sparklines:

- **No axes, no ticks, no labels** — the sparkline IS the data
- **Size**: approximately the height of surrounding text (~18px or 0.25 inches tall)
- **Highlight only**: optionally mark the first value, last value, min, and max with small dots
- **Use inline** — sparklines belong in tables, paragraphs, or dashboards alongside the numbers they represent
- **Line width**: thin (0.5-1pt)
- **Color**: single color, typically gray or black

---

## 6. Small Multiples

When comparing data across categories, time periods, or groups:

- Use a grid of small, identically-scaled panels (small multiples)
- **Share axes** — all panels must have the same x and y scale
- **Remove redundant labels** — only label the outer edges of the grid
- **Consistent sizing** — each panel should be the same dimensions
- **No more than ~25 panels** — beyond this, consider aggregation
- **Order meaningfully** — alphabetical, chronological, or by a key metric (not random)

---

## 7. Slope Charts (Slopegraphs)

For before/after or two-point-in-time comparisons:

- Two vertical axes, one on each side
- Lines connecting each entity's values
- Direct labels on both sides (no legend needed)
- Handle label overlap with vertical displacement
- Highlight notable changes with the accent color
- Keep all other lines in light gray

---

## 8. Post-Generation Checklist

After generating any visualization code, verify it against `references/checklist.md`. Every item must pass. If any item fails, fix the code before presenting it to the user.

---

## 9. User Override Protocol

If the user explicitly requests a banned element (e.g., "I need a pie chart for this presentation"):

1. Briefly explain the Tufte principle being violated (1-2 sentences)
2. Offer the recommended substitute
3. If the user insists after seeing the alternative, comply but still apply all other Tufte rules (serif font, no chartjunk, grayscale, etc.)

Never silently comply with a banned element on the first request. Always educate first, then defer.

---

## 10. Response Format

When generating visualization code:

1. State which Tufte principles are being applied (brief, 1-2 lines)
2. Provide the complete, runnable code
3. Include a brief note on what was intentionally omitted and why (e.g., "Legend removed: series are directly labeled")
4. Run through the checklist mentally; note any items that could not be satisfied and why
