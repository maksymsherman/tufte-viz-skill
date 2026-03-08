---
name: clean-viz
description: >
  Applies data visualization best practices inspired by Edward Tufte's principles
  whenever creating charts, plots, or visualizations. Triggers on any request involving matplotlib, pyplot,
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

# Clean Data Visualization Skill

You are now operating under data visualization best practices inspired by Edward Tufte's principles. Every chart, plot, or figure you produce MUST follow these rules. Deviate only if:

1. The user explicitly overrides a specific rule, **or**
2. The data genuinely requires it (e.g., negative values in a bar chart, diverging colormaps in a heatmap) — but this applies to less than 0.5% of visualizations. Before deviating, seriously consider whether the standard pattern can be adapted instead. If deviation is truly necessary, state which rule is being bent and why.

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
- **Handle label collisions** — centroid-based placement (e.g., placing labels at the endpoint of each line) will collide whenever groups have similar values. When multiple labels cluster together:
  - Use vertical offset stacking: sort labels by y-value and enforce a minimum gap
  - Prefer edge-of-cluster placement (e.g., percentile-based anchors) over centroids
  - As a last resort, use short leader lines connecting displaced labels to their data points
  - Always visually verify that no label overlaps another label or obscures data points
- **Pad axes for end-of-line labels without breaking range frames** — extending `xlim` for label room creates ticks and spines in non-data territory. After any `set_xlim` override: (1) reset `set_xticks` to data-range-only values, (2) re-assert `spines['bottom'].set_bounds(data_min, data_max)`. See the `pad_axis_for_labels` helper in the matplotlib patterns.
- **Annotate data points that tell a story** — label outliers, named entities, inflection points, or turning points. Do NOT annotate min/max with raw coordinate tuples like `(9, 35.0)` — range frame bounds already communicate extremes through axis ticks. Annotations should add context that the axes alone cannot provide (e.g., "2020 lockdown" on a dip, or a company name on a scatter point)
- **Always include units of measurement on axes** — an axis label is redundant only when both its meaning AND its unit are completely obvious from the title or surrounding context. "Revenue" without a currency is unclear; "Income (thousands)" without a unit is ambiguous. When in doubt, keep the label. Omit only truly redundant labels (e.g., an x-axis labeled "Year" when the tick labels are already "2018, 2019, 2020")
- **Match label precision to the data** — if all values are whole numbers, format labels as integers (e.g., `35%` not `35.0%`). Use the minimum number of decimal places needed to distinguish values. Trailing zeros waste ink and imply false precision

### Consistency in Generated Code
- **Never hardcode font sizes or colors in helper functions** — always reference the defined global constants (e.g., `CLEAN_LABEL_SIZE`, `CLEAN_BLACK`)
- **Default all label text to `CLEAN_BLACK`** — reserve gray only for intentionally de-emphasized elements (e.g., non-highlighted series in a slope chart)
- **In multi-panel figures**, inconsistent font sizes and label colors are hard to catch visually — using constants prevents this class of bug entirely

### Multi-Series Differentiation
- **Use line style variation alongside color** — solid, dashed, dash-dot, dotted. At small sizes or in print, color alone is insufficient to distinguish series
- **Dot emphasis degrades for multi-series** — the white-mask-plus-colored-dot technique works for single-series plots but homogenizes multi-series lines since all dots look the same regardless of color. For multi-series, vary line style instead and reserve dot emphasis for single-series or ≤2 series
- **When using markers for multi-series**, vary marker shape (circle, square, triangle, diamond) in addition to color

### Color
- **Default to grayscale** — use black, dark gray (`#333333`), medium gray (`#888888`), light gray (`#cccccc`)
- **Single accent color** — when emphasis is needed, use exactly one color (default: `#c0392b` muted red)
- **Colorblind-safe palette** — when multiple colors are required, use the Paul Tol palette ordered by contrast (high-contrast first):
  - `#332288` (indigo), `#CC6677` (rose), `#117733` (green), `#882255` (wine),
    `#44AA99` (teal), `#AA4499` (purple), `#88CCEE` (cyan), `#999933` (olive)
- **Match color contrast to element type** — not all visual elements need the same contrast level. Tie the palette constraint to what the color is applied to:
  - **Lines, text, and small markers** (high contrast required): use only the first 6 palette colors (indigo through purple). These are legible at 1-2pt line widths and 9-11pt text on white
  - **Bars, filled areas, and large markers** (moderate contrast sufficient): all 8 palette colors are acceptable, including cyan (`#88CCEE`) and olive (`#999933`), because the larger filled area compensates for lower contrast
  - **Legend text and labels** should always use `CLEAN_BLACK` — even when the associated data element uses a low-contrast color. Use a colored swatch, dash, or marker next to the label instead of coloring the text itself
- **Beyond 6 line series, change strategy** — if you need more than 6 distinguishable lines or text-labeled series, do not reach for low-contrast colors. Instead: use small multiples to split series into groups, group related series under a shared color with line style variation, or aggregate. The palette is not infinitely extensible; the design must adapt
- **Never use rainbow/jet colormaps** — use sequential single-hue (grays, blues) or diverging (blue-white-red) instead

### Layout & Density
- **Prefer small multiples** over complex single charts with many series
- **High data density** — aim for at least 50 data points per square inch where appropriate
- **Minimal margins** — `tight_layout()` or equivalent; remove excessive whitespace

---

## 3. Mandatory Rules — Never Do

### Banned Chart Types
Do NOT generate these chart types. If the user requests one, explain the visualization principle being violated and offer the substitute from the table below.

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
| Summary-only categorical (e.g., bar of means, dot plot of medians when n>10/group) | Hides distribution shape, outliers, and sample size; wastes available data | Strip/jitter/beeswarm plot with summary statistic overlaid |

### Banned Visual Elements
- **No background colors or images** — white background only
- **No gradient fills** — solid colors only
- **No drop shadows** — on any element
- **No 3D perspective effects** — ever
- **No heavy gridlines** — if gridlines are needed, use the appropriate technique for the chart context (see reference line rules below)
- **Reference lines by context** — reference lines serve different roles depending on whether they sit on top of colored bars or behind bars on a white background. Use the right color for each context:
  - **On top of colored bars** (vertical bar charts): use white (`#ffffff`) gridlines — the bar fill provides contrast
  - **Behind bars on a white background** (horizontal bar charts, or any chart where reference lines sit against white): use `#d0d0d0` — visible enough to aid position judgment without competing with the data. `#eeeeee` is nearly invisible against white and should not be used in this context
  - **Round intervals** — place reference lines at clean round numbers (every 5, 10, 25, etc.) that align with the data scale
- **No decorative borders or boxes** — around legends, titles, or annotations
- **No ALL CAPS text** — in titles, labels, or annotations
- **No rotated tick labels** — if labels are too long, use a horizontal bar chart or abbreviate

---

## 4. Library-Specific Patterns

When generating code, load the appropriate reference file for concrete code patterns:

### Python — matplotlib / seaborn
Read `references/matplotlib-patterns.md` for:
- Base `rcParams` configuration
- Color palette and typography constants (`CLEAN_FONT_SIZE`, `CLEAN_LABEL_SIZE`, etc.)
- Line style cycle (`CLEAN_LINE_STYLES`) for multi-series differentiation
- `apply_range_frame()` helper function
- `pad_axis_for_labels()` — extend xlim without breaking range frames
- `label_lines_no_overlap()` — collision-aware multi-series labeling
- `clean_multi_line_plot()` — multi-series with line style variation
- Direct labeling patterns (single-series)
- Bar chart (white gridlines)
- Line plot with dot emphasis (single-series only)
- Slope chart implementation
- Sparkline function
- Small multiples template (with scaling notes)
- Seaborn overrides

### Python — Plotly
Read `references/plotly-patterns.md` for:
- `CLEAN_LAYOUT` base template
- Range frame axis configuration
- Direct annotation patterns
- Multi-series line chart with line style variation and collision-aware labels
- Small multiples with `make_subplots`
- Sparkline configuration

### Other Libraries (Altair, D3.js, ggplot2, Observable Plot)
Read `references/general-patterns.md` for:
- Altair theme configuration
- D3.js spine removal and serif font patterns
- R/ggplot2 `theme_tufte()` and `geom_rangeframe()`
- Observable Plot styling

---

## 5. Python Environment & Dependency Setup

Before running generated Python visualization code, ensure the required libraries are installed.

### Prefer `uv` over `pip`
1. **Check for `uv`** — run `which uv` to see if it is available
2. If `uv` is found:
   - If no `pyproject.toml` exists, run `uv init --bare` to create a minimal one
   - Then run `uv add <packages>` (e.g., `uv add matplotlib seaborn numpy`) to install dependencies
3. If `uv` is not found, fall back to `pip install <packages>`

### Safety: never run bare `uv init`
**Never run `uv init` without the `--bare` flag** in an existing repository. Plain `uv init` overwrites `.gitignore`, creates a `README.md`, and can disrupt git history. Only `uv init --bare` is safe — it creates a minimal `pyproject.toml` and nothing else.

---

## 6. Sparklines

Sparklines are intense, simple, word-sized graphics. When creating sparklines:

- **No axes, no ticks, no labels** — the sparkline IS the data
- **Size**: approximately the height of surrounding text (~18px or 0.25 inches tall)
- **Highlight only**: optionally mark the first value, last value, min, and max with small dots
- **Use inline** — sparklines belong in tables, paragraphs, or dashboards alongside the numbers they represent
- **Line width**: thin (0.5-1pt)
- **Color**: single color, typically gray or black

---

## 7. Small Multiples

When comparing data across categories, time periods, or groups:

- Use a grid of small, identically-scaled panels (small multiples)
- **Share axes** — all panels must have the same x and y scale
- **Remove redundant labels** — only label the outer edges of the grid
- **Consistent sizing** — each panel should be the same dimensions
- **No more than ~25 panels** — beyond this, consider aggregation
- **Order meaningfully** — alphabetical, chronological, or by a key metric (not random)

### Small-Panel Adaptations

The patterns in this skill are written for single full-size charts. At reduced panel sizes, many techniques degrade silently. When panels shrink, adapt:

| Full-size technique | Problem at small size | Small-panel substitute |
|---|---|---|
| Fine reference lines (0.5-0.8pt) | Become invisible | Increase to 1-1.2pt or omit entirely |
| Dot emphasis (white mask + dot) | Dots overlap; series look identical | Use plain lines with style variation |
| Direct labels on each panel | Overlap; unreadable at small font sizes | Label only the first panel; use a shared legend if needed |
| Font size differences (9pt vs 11pt) | Both render too small to distinguish | Use a single font size (the larger one) |
| Range frames with bounded spines | Visual benefit is imperceptible | Simplify to plain axis removal (no spines) |
| Per-point annotations | Clutter overwhelms the panel | Annotate only in a single "detail" panel |

**General rule**: as panels shrink, remove visual elements rather than scaling them down. A clean, readable small panel is better than a miniaturized version of a full-size chart.

---

## 8. Cohesive Multi-Chart Design

When generating multiple charts in a session (e.g., a set of 5 figures for a report or presentation), they will almost certainly be displayed together. Treat them as a unified visual system:

- **Lock the color palette** — use the same color assignments across all charts. If "Revenue" is indigo in chart 1, it must be indigo in every chart
- **Unify typography** — identical font family, base size, title size, and label size across all figures. Use the global constants (`CLEAN_FONT_SIZE`, `CLEAN_TITLE_SIZE`, etc.)
- **Consistent axis styling** — same spine treatment, tick direction, and range-frame approach on every chart. Do not mix range frames and full axes
- **Match figure dimensions** — use the same `figsize` (or width/height in Plotly) for charts that will sit side by side. Mismatched aspect ratios look accidental
- **Harmonize data-ink weight** — line widths, marker sizes, and bar widths should be the same across charts unless there is a deliberate reason to differ
- **Shared ordering** — if categories appear in multiple charts, keep the same sort order throughout

Inconsistency between charts in a set is more noticeable than inconsistency within a single chart. When in doubt, re-check all previously generated charts in the session before finalizing a new one.

---

## 9. Slope Charts (Slopegraphs)

For before/after or two-point-in-time comparisons:

- Two vertical axes, one on each side
- Lines connecting each entity's values
- Direct labels on both sides (no legend needed)
- Handle label overlap with vertical displacement
- Highlight notable changes with the accent color
- Keep all other lines in light gray

---

## 10. Post-Generation Checklist

After generating any visualization code, you MUST write out the full checklist from `references/checklist.md` as a visible markdown table in your response, with pass/fail for every item. This is not optional. If any item fails, fix the code and re-run the checklist before presenting the final version to the user. A visualization without a written checklist is incomplete.

---

## 11. User Override Protocol

If the user explicitly requests a banned element (e.g., "I need a pie chart for this presentation"):

1. Briefly explain the visualization principle being violated (1-2 sentences)
2. Offer the recommended substitute
3. If the user insists after seeing the alternative, comply but still apply all other clean-viz rules (serif font, no chartjunk, grayscale, etc.)

Never silently comply with a banned element on the first request. Always educate first, then defer.

---

## 12. Response Format

When generating visualization code:

1. State which visualization principles are being applied (brief, 1-2 lines)
2. Provide the complete, runnable code
3. Include a brief note on what was intentionally omitted and why (e.g., "Legend removed: series are directly labeled")
4. **Write out the checklist** — after the code block, include a markdown table with every checklist item and its pass/fail status. If any item fails, fix the code BEFORE presenting it. Do not skip this step or perform it silently. The written checklist is part of the deliverable.
