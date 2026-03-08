# Matplotlib & Seaborn — Clean-Viz Patterns

Concrete code patterns for producing clean, publication-quality visualizations in matplotlib and seaborn (inspired by Edward Tufte's principles). Copy and adapt these patterns when generating visualization code.

---

## Base rcParams Configuration

Apply this at the top of every matplotlib visualization:

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Clean-viz base configuration
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 13,
    'axes.titleweight': 'normal',
    'axes.labelsize': 11,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.major.size': 4,
    'ytick.major.size': 4,
    'xtick.minor.size': 0,
    'ytick.minor.size': 0,
    'axes.grid': False,
    'grid.alpha': 0,
    'legend.frameon': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.dpi': 150,
    'figure.dpi': 100,
})
```

---

## Color Palette

```python
# Clean-viz grayscale palette (default)
CLEAN_BLACK = '#333333'
CLEAN_DARK_GRAY = '#555555'
CLEAN_MEDIUM_GRAY = '#888888'
CLEAN_LIGHT_GRAY = '#cccccc'
CLEAN_FAINT_GRAY = '#eeeeee'
CLEAN_ACCENT = '#c0392b'  # muted red, for emphasis only

# Typography constants — always reference these instead of hardcoding sizes.
# These must stay in sync with the rcParams values above.
CLEAN_FONT_SIZE = 11       # base text and axis labels (matches rcParams font.size)
CLEAN_TITLE_SIZE = 13      # chart titles (matches rcParams axes.titlesize)
CLEAN_LABEL_SIZE = 10      # direct labels and annotations
CLEAN_SMALL_SIZE = 9       # secondary labels, de-emphasized text, small multiples

# Line style cycle — use alongside color to distinguish multi-series lines.
# Ensures series are distinguishable without color (accessibility, small sizes, print).
CLEAN_LINE_STYLES = ['solid', 'dashed', (0, (4, 2, 1, 2)), 'dotted']
#                    solid    dashed    dash-dot                dotted

# Colorblind-safe palette (Paul Tol) — ordered by contrast on white backgrounds.
# High-contrast colors come first; use these for lines, text, and small elements.
# Lower-contrast colors (cyan, olive) are at the end — use only for fills or large areas.
CLEAN_COLORS = [
    '#332288',  # indigo  (high contrast)
    '#CC6677',  # rose    (high contrast)
    '#117733',  # green   (high contrast)
    '#882255',  # wine    (high contrast)
    '#44AA99',  # teal    (medium contrast)
    '#AA4499',  # purple  (medium contrast)
    '#88CCEE',  # cyan    (low contrast — avoid for lines on white)
    '#999933',  # olive   (low contrast — avoid for lines on white)
]
```

---

## Range Frame Helper

Bind spine extents to the actual data range:

```python
def apply_range_frame(ax, x, y):
    """Apply range frames: spines span only the data range."""
    ax.spines['bottom'].set_bounds(min(x), max(x))
    ax.spines['left'].set_bounds(min(y), max(y))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set ticks to only cover data range
    ax.set_xlim(min(x) - (max(x) - min(x)) * 0.05, max(x) + (max(x) - min(x)) * 0.05)
    ax.set_ylim(min(y) - (max(y) - min(y)) * 0.05, max(y) + (max(y) - min(y)) * 0.05)
```

Usage:

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color=CLEAN_BLACK, linewidth=1.2)
apply_range_frame(ax, x, y)
ax.set_title('Descriptive sentence-case title')
plt.tight_layout()
```

---

## Direct Labeling (Replace Legends)

```python
def label_line(ax, x, y, label, color=CLEAN_BLACK, offset=(5, 0)):
    """Place a text label at the end of a line series."""
    ax.annotate(
        label,
        xy=(x[-1], y[-1]),
        xytext=offset,
        textcoords='offset points',
        fontsize=CLEAN_LABEL_SIZE,
        color=color,
        va='center',
        fontfamily='serif',
    )

# Usage: after plotting each series
ax.plot(x, y1, color=CLEAN_BLACK, linewidth=1.2)
label_line(ax, x, y1, 'Series A')

ax.plot(x, y2, color=CLEAN_MEDIUM_GRAY, linewidth=1.2)
label_line(ax, x, y2, 'Series B')

# Remove the legend entirely
ax.legend().set_visible(False)
# Or better: never call ax.legend() at all
```

### Collision-Aware Multi-Series Labeling

**Warning**: simple endpoint labeling (above) will collide whenever two or more series
have similar final values. For multi-series plots, always use `label_lines_no_overlap`
instead of calling `label_line` in a loop.

```python
def label_lines_no_overlap(ax, series_endpoints, min_gap_pts=12):
    """Place end-of-line labels with vertical collision avoidance.

    Args:
        ax: matplotlib Axes
        series_endpoints: list of (x_end, y_end, label, color) tuples
        min_gap_pts: minimum vertical gap between labels in points
    """
    # Sort by y-value so we can stack from bottom to top
    sorted_items = sorted(series_endpoints, key=lambda s: s[1])

    # Convert min_gap from points to data coordinates
    fig = ax.get_figure()
    fig.canvas.draw()
    inv = ax.transData.inverted()
    _, y0 = inv.transform((0, 0))
    _, y1 = inv.transform((0, min_gap_pts))
    gap_data = abs(y1 - y0)

    # Assign display positions, pushing overlapping labels upward
    display_positions = []
    for i, (x_end, y_end, label, color) in enumerate(sorted_items):
        pos = y_end
        if i > 0 and pos - display_positions[i - 1] < gap_data:
            pos = display_positions[i - 1] + gap_data
        display_positions.append(pos)

    # Draw labels; add a leader line if label was displaced
    for (x_end, y_end, label, color), y_display in zip(sorted_items, display_positions):
        displaced = abs(y_display - y_end) > gap_data * 0.1
        if displaced:
            ax.annotate(
                label, xy=(x_end, y_end), xytext=(8, 0),
                xycoords='data', textcoords=('offset points', ('data', y_display)),
                fontsize=CLEAN_LABEL_SIZE, color=color, va='center', fontfamily='serif',
                arrowprops=dict(arrowstyle='-', color=CLEAN_LIGHT_GRAY, lw=0.6),
            )
        else:
            ax.annotate(
                label, xy=(x_end, y_end), xytext=(8, 0),
                textcoords='offset points',
                fontsize=CLEAN_LABEL_SIZE, color=color, va='center', fontfamily='serif',
            )
```

---

## Axis Padding for End-of-Line Labels

Direct labels at line endpoints require extending `xlim` beyond the data to make room
for text. But this causes matplotlib to auto-generate tick marks in the padding zone,
and the spine visually extends into non-data territory — undermining the range frame
principle.

**Always apply this pattern after extending xlim for label room:**

```python
def pad_axis_for_labels(ax, x_data, y_data, pad_fraction=0.12):
    """Extend xlim for label room while keeping ticks and spines within data range.

    Call this AFTER plotting and BEFORE label_line / label_lines_no_overlap.
    """
    x_min, x_max = min(x_data), max(x_data)
    x_range = x_max - x_min

    # Extend xlim to make room for labels on the right
    ax.set_xlim(x_min - x_range * 0.02, x_max + x_range * pad_fraction)

    # Constrain ticks to data range only (no ticks in padding zone)
    existing_ticks = [t for t in ax.get_xticks() if x_min <= t <= x_max]
    ax.set_xticks(existing_ticks)

    # Re-assert range frame bounds after xlim change
    ax.spines['bottom'].set_bounds(x_min, x_max)
    if y_data is not None:
        ax.spines['left'].set_bounds(min(y_data), max(y_data))
```

Usage:

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y1, color=CLEAN_BLACK, linewidth=1.2)
ax.plot(x, y2, color=CLEAN_MEDIUM_GRAY, linewidth=1.2)
apply_range_frame(ax, x, y1 + y2)  # initial range frame
pad_axis_for_labels(ax, x, y1 + y2)  # extend for labels
label_lines_no_overlap(ax, [(x[-1], y1[-1], 'A', CLEAN_BLACK),
                             (x[-1], y2[-1], 'B', CLEAN_MEDIUM_GRAY)])
```

---

## Line Plot with Dot Emphasis (Single Series Only)

Layer technique: base line, white mask circles, small data dots.

**Important**: This technique works well for single-series plots or at most 2 series.
For 3+ series, the white mask circles homogenize the dots and series become
indistinguishable. Use `clean_multi_line_plot` (below) for multi-series instead.

```python
def clean_line_plot(ax, x, y, color=CLEAN_BLACK, label=None):
    """Line plot with dot emphasis at data points.

    Use only for single-series or 2-series plots. For 3+ series,
    use clean_multi_line_plot which varies line style for differentiation.
    """
    ax.plot(x, y, linestyle='-', color=color, linewidth=1, zorder=1)
    ax.scatter(x, y, color='white', s=80, zorder=2, edgecolors='none')
    ax.scatter(x, y, color=color, s=15, zorder=3, edgecolors='none')
    if label:
        label_line(ax, x, y, label, color=color)
```

---

## Multi-Series Line Plot

For 2+ series, vary line style alongside color to ensure distinguishability
without color (important for accessibility, print, and small panels).

```python
def clean_multi_line_plot(ax, x, series_dict, colors=None):
    """Multi-series line plot with line style variation and collision-aware labels.

    Args:
        ax: matplotlib Axes
        x: shared x-axis data
        series_dict: dict of {label: y_values}
        colors: optional list of colors (defaults to CLEAN_COLORS)
    """
    palette = colors or CLEAN_COLORS
    endpoints = []

    for i, (label, y) in enumerate(series_dict.items()):
        color = palette[i % len(palette)]
        style = CLEAN_LINE_STYLES[i % len(CLEAN_LINE_STYLES)]
        ax.plot(x, y, linestyle=style, color=color, linewidth=1.2)
        endpoints.append((x[-1], y[-1], label, color))

    # Collision-aware labeling (see label_lines_no_overlap)
    label_lines_no_overlap(ax, endpoints)
```

---

## Bar Chart (White Gridlines)

Bars with horizontal white lines replacing traditional gridlines:

```python
def clean_bar_chart(ax, categories, values, color=CLEAN_MEDIUM_GRAY):
    """Bar chart using white gridlines instead of axis spines."""
    bars = ax.bar(categories, values, color=color, edgecolor='none', width=0.6)

    # Remove all spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # White horizontal gridlines on top of bars
    ax.yaxis.grid(color='white', linewidth=1.5)
    ax.set_axisbelow(False)  # grid on top of bars

    # Remove tick marks
    ax.tick_params(bottom=False, left=False)

    # Direct-label bar values
    for bar, val in zip(bars, values):
        height = bar.get_height()
        offset = max(abs(v) for v in values) * 0.02
        label_y = height + offset if height >= 0 else height - offset
        ax.text(
            bar.get_x() + bar.get_width() / 2, label_y,
            f'{val}',
            ha='center', va='bottom' if height >= 0 else 'top',
            fontsize=CLEAN_LABEL_SIZE, fontfamily='serif', color=CLEAN_BLACK,
        )

    return bars
```

---

## Horizontal Bar Chart (with Reference Lines)

For ranked categorical data shown as horizontal bars — the preferred substitute
for pie charts and donut charts:

```python
def clean_horizontal_bar_chart(ax, categories, values, color=CLEAN_MEDIUM_GRAY,
                                highlight_max=True, value_fmt='{:.0f}'):
    """Horizontal bar chart with vertical reference lines for easy reading.

    Args:
        categories: list of category names (will be sorted by value, largest at top)
        values: list of numeric values
        color: default bar color
        highlight_max: if True, accent-color the largest bar
        value_fmt: format string for direct labels (use '{:.0f}' for ints, '{:.1f}%' for %)
    """
    # Sort ascending so largest appears at top
    sorted_pairs = sorted(zip(categories, values), key=lambda p: p[1])
    cats = [p[0] for p in sorted_pairs]
    vals = [p[1] for p in sorted_pairs]

    colors = [CLEAN_ACCENT if (highlight_max and v == max(vals)) else color
              for v in vals]
    bars = ax.barh(cats, vals, color=colors, edgecolor='none', height=0.6)

    # Remove all spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Thin vertical reference lines at round intervals
    ax.xaxis.grid(color=CLEAN_FAINT_GRAY, linewidth=0.8)
    ax.set_axisbelow(True)  # reference lines behind bars

    # Remove tick marks
    ax.tick_params(bottom=False, left=False)

    # Direct-label bar values
    for bar, val in zip(bars, vals):
        width = bar.get_width()
        ax.text(
            width + max(vals) * 0.02, bar.get_y() + bar.get_height() / 2,
            value_fmt.format(val),
            ha='left', va='center',
            fontsize=CLEAN_LABEL_SIZE, fontfamily='serif', color=CLEAN_BLACK,
        )

    return bars
```

---

## Dot Plot (Alternative to Bar Chart)

For ranked categorical data:

```python
def clean_dot_plot(ax, categories, values, color=CLEAN_BLACK):
    """Cleveland dot plot — Preferred alternative to bar charts."""
    y_pos = range(len(categories))
    ax.scatter(values, y_pos, color=color, s=40, zorder=3)
    ax.hlines(y_pos, 0, values, color=CLEAN_LIGHT_GRAY, linewidth=0.8, zorder=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(left=False)
    ax.spines['bottom'].set_bounds(min(values), max(values))
```

---

## Slope Chart (Slopegraph)

For before/after or two-time-point comparisons:

```python
def clean_slope_chart(ax, labels, left_values, right_values,
                      left_label='Before', right_label='After',
                      highlight=None, accent_color=CLEAN_ACCENT):
    """Slope chart for two-point comparisons."""
    # Resolve overlapping labels
    def resolve_overlaps(values, min_gap=0.5):
        indexed = sorted(enumerate(values), key=lambda x: x[1])
        resolved = [0.0] * len(values)
        for i, (orig_idx, val) in enumerate(indexed):
            if i > 0:
                prev_idx, prev_val = indexed[i - 1]
                if val - resolved[prev_idx] < min_gap:
                    val = resolved[prev_idx] + min_gap
            resolved[orig_idx] = val
        return resolved

    left_positions = resolve_overlaps(left_values)
    right_positions = resolve_overlaps(right_values)

    for i, label in enumerate(labels):
        color = accent_color if label == highlight else CLEAN_LIGHT_GRAY
        lw = 1.5 if label == highlight else 0.8
        ax.plot([0, 1], [left_positions[i], right_positions[i]],
                color=color, linewidth=lw)

        # Left label
        ax.text(-0.05, left_positions[i], f'{label} ({left_values[i]})',
                ha='right', va='center', fontsize=CLEAN_SMALL_SIZE, fontfamily='serif',
                color=CLEAN_BLACK if label == highlight else CLEAN_MEDIUM_GRAY)

        # Right label
        ax.text(1.05, right_positions[i], f'{label} ({right_values[i]})',
                ha='left', va='center', fontsize=CLEAN_SMALL_SIZE, fontfamily='serif',
                color=CLEAN_BLACK if label == highlight else CLEAN_MEDIUM_GRAY)

    # Column headers
    ax.text(0, max(left_positions) + 1, left_label,
            ha='center', va='bottom', fontsize=CLEAN_FONT_SIZE, fontfamily='serif',
            fontweight='bold', color=CLEAN_BLACK)
    ax.text(1, max(right_positions) + 1, right_label,
            ha='center', va='bottom', fontsize=CLEAN_FONT_SIZE, fontfamily='serif',
            fontweight='bold', color=CLEAN_BLACK)

    # Remove all axes
    ax.axis('off')
```

---

## Sparkline

Minimal, word-sized graphic:

```python
def clean_sparkline(ax, data, color=CLEAN_BLACK, highlight_endpoints=True):
    """Create a sparkline — a word-sized data graphic."""
    x = range(len(data))
    ax.plot(x, data, color=color, linewidth=0.8)

    if highlight_endpoints:
        # Mark first and last points
        ax.scatter([x[0], x[-1]], [data[0], data[-1]],
                   color=color, s=8, zorder=3)
        # Mark min and max
        min_idx = np.argmin(data)
        max_idx = np.argmax(data)
        ax.scatter([min_idx], [data[min_idx]], color=CLEAN_ACCENT, s=8, zorder=3)
        ax.scatter([max_idx], [data[max_idx]], color='#117733', s=8, zorder=3)

    # Remove everything except the line
    ax.axis('off')
    ax.set_xlim(-0.5, len(data) - 0.5)
    y_margin = (max(data) - min(data)) * 0.1
    ax.set_ylim(min(data) - y_margin, max(data) + y_margin)
```

For inline sparklines in a table or grid:

```python
def sparkline_grid(data_dict, figsize=(10, None)):
    """Create a column of sparklines with labels and values."""
    n = len(data_dict)
    fig_height = n * 0.4 if figsize[1] is None else figsize[1]
    fig, axes = plt.subplots(n, 1, figsize=(figsize[0], fig_height))
    if n == 1:
        axes = [axes]

    for ax, (label, data) in zip(axes, data_dict.items()):
        clean_sparkline(ax, data)
        ax.text(-1, np.mean(data), label, ha='right', va='center',
                fontsize=CLEAN_SMALL_SIZE, fontfamily='serif', color=CLEAN_BLACK)
        ax.text(len(data), data[-1], f' {data[-1]:.1f}',
                ha='left', va='center', fontsize=CLEAN_SMALL_SIZE, fontfamily='serif',
                color=CLEAN_BLACK)

    plt.subplots_adjust(hspace=0.5)
    return fig
```

---

## Small Multiples

**Scaling note**: at reduced panel sizes, simplify rather than miniaturize.
Drop dot emphasis, use a single font size (`CLEAN_SMALL_SIZE`), increase line
widths to 1.2pt, and avoid per-panel direct labels. See SKILL.md § 7 for the
full adaptation table.

```python
def clean_small_multiples(data_dict, ncols=3, figsize=(10, 8),
                          plot_fn=None, sharex=True, sharey=True):
    """Create a grid of small multiples with shared axes."""
    n = len(data_dict)
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize,
                             sharex=sharex, sharey=sharey)
    axes_flat = axes.flatten() if hasattr(axes, 'flatten') else [axes]

    for i, (title, (x, y)) in enumerate(data_dict.items()):
        ax = axes_flat[i]
        if plot_fn:
            plot_fn(ax, x, y)
        else:
            ax.plot(x, y, color=CLEAN_BLACK, linewidth=1)
        ax.set_title(title, fontsize=CLEAN_LABEL_SIZE, fontfamily='serif', pad=4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(direction='in', labelsize=CLEAN_SMALL_SIZE)

    # Remove unused panels
    for j in range(n, len(axes_flat)):
        axes_flat[j].set_visible(False)

    # Only label outer edges
    for ax in axes_flat[:n]:
        if ax.get_subplotspec().is_last_row():
            pass  # keep x labels
        else:
            ax.set_xticklabels([])
        if ax.get_subplotspec().is_first_col():
            pass  # keep y labels
        else:
            ax.set_yticklabels([])

    plt.tight_layout()
    return fig, axes
```

---

## Seaborn Overrides

When seaborn is used, override its defaults to match clean-viz style:

```python
import seaborn as sns

def apply_clean_seaborn():
    """Override seaborn defaults with clean-viz settings."""
    sns.set_style('white')  # not 'whitegrid' — we control gridlines
    sns.set_context('paper', font_scale=1.1)
    sns.set_palette([CLEAN_BLACK, CLEAN_MEDIUM_GRAY, CLEAN_ACCENT])

    # After every seaborn plot, call:
    # sns.despine()  — removes top/right spines
    # Then apply range frames manually if needed

# Post-plot cleanup for seaborn:
def clean_seaborn(ax, x_data=None, y_data=None):
    """Apply clean-viz cleanup after a seaborn plot."""
    sns.despine(ax=ax)
    ax.tick_params(direction='in')
    if x_data is not None and y_data is not None:
        apply_range_frame(ax, x_data, y_data)
    ax.get_legend().remove() if ax.get_legend() else None
```

---

## Scatter Plot

```python
def clean_scatter(ax, x, y, color=CLEAN_BLACK, label_points=None):
    """Scatter plot with range frames."""
    ax.scatter(x, y, color=color, s=20, edgecolors='none', alpha=0.8)
    apply_range_frame(ax, x, y)

    # Optionally label specific points
    if label_points:
        for idx, text in label_points.items():
            ax.annotate(
                text, (x[idx], y[idx]),
                xytext=(5, 5), textcoords='offset points',
                fontsize=CLEAN_SMALL_SIZE, fontfamily='serif', color=CLEAN_BLACK,
            )
```

---

## Histogram

```python
def clean_histogram(ax, data, bins=20, color=CLEAN_MEDIUM_GRAY):
    """Histogram with white gridlines."""
    ax.hist(data, bins=bins, color=color, edgecolor='white', linewidth=0.5)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.yaxis.grid(color='white', linewidth=1.2)
    ax.set_axisbelow(False)
    ax.tick_params(bottom=False, left=False)
```

---

## Heatmap

```python
def clean_heatmap(ax, data, row_labels, col_labels, cmap='Greys'):
    """Heatmap: no gridlines, direct value labels."""
    im = ax.imshow(data, cmap=cmap, aspect='auto')

    ax.set_xticks(range(len(col_labels)))
    ax.set_yticks(range(len(row_labels)))
    ax.set_xticklabels(col_labels, fontsize=CLEAN_SMALL_SIZE, fontfamily='serif')
    ax.set_yticklabels(row_labels, fontsize=CLEAN_SMALL_SIZE, fontfamily='serif')

    # Direct value labels in cells
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = data[i][j]
            # Pick text color based on cell luminance (works for sequential and diverging colormaps)
            norm_val = (val - im.norm.vmin) / (im.norm.vmax - im.norm.vmin)
            r, g, b, _ = im.cmap(norm_val)
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            text_color = 'white' if luminance < 0.5 else CLEAN_BLACK
            ax.text(j, i, f'{val:.1f}', ha='center', va='center',
                    fontsize=CLEAN_SMALL_SIZE, fontfamily='serif', color=text_color)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(bottom=False, left=False)

    return im
```
