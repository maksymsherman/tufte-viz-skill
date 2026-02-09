# Matplotlib & Seaborn — Tufte Patterns

Concrete code patterns for producing Tufte-style visualizations in matplotlib and seaborn. Copy and adapt these patterns when generating visualization code.

---

## Base rcParams Configuration

Apply this at the top of every matplotlib visualization:

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Tufte-style base configuration
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
# Tufte grayscale palette (default)
TUFTE_BLACK = '#333333'
TUFTE_DARK_GRAY = '#555555'
TUFTE_MEDIUM_GRAY = '#888888'
TUFTE_LIGHT_GRAY = '#cccccc'
TUFTE_FAINT_GRAY = '#eeeeee'
TUFTE_ACCENT = '#c0392b'  # muted red, for emphasis only

# Colorblind-safe palette (Paul Tol) — use when multiple colors required
TUFTE_COLORS = [
    '#332288',  # indigo
    '#88CCEE',  # cyan
    '#44AA99',  # teal
    '#117733',  # green
    '#999933',  # olive
    '#CC6677',  # rose
    '#882255',  # wine
    '#AA4499',  # purple
]
```

---

## Range Frame Helper

Bind spine extents to the actual data range:

```python
def apply_range_frame(ax, x, y):
    """Apply Tufte range frames: spines span only the data range."""
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
ax.plot(x, y, color=TUFTE_BLACK, linewidth=1.2)
apply_range_frame(ax, x, y)
ax.set_title('Descriptive sentence-case title')
plt.tight_layout()
```

---

## Direct Labeling (Replace Legends)

```python
def label_line(ax, x, y, label, color=TUFTE_BLACK, offset=(5, 0)):
    """Place a text label at the end of a line series."""
    ax.annotate(
        label,
        xy=(x[-1], y[-1]),
        xytext=offset,
        textcoords='offset points',
        fontsize=10,
        color=color,
        va='center',
        fontfamily='serif',
    )

# Usage: after plotting each series
ax.plot(x, y1, color=TUFTE_BLACK, linewidth=1.2)
label_line(ax, x, y1, 'Series A')

ax.plot(x, y2, color=TUFTE_MEDIUM_GRAY, linewidth=1.2)
label_line(ax, x, y2, 'Series B')

# Remove the legend entirely
ax.legend().set_visible(False)
# Or better: never call ax.legend() at all
```

---

## Line Plot with Dot Emphasis

Layer technique: base line, white mask circles, small data dots.

```python
def tufte_line_plot(ax, x, y, color=TUFTE_BLACK, label=None):
    """Line plot with Tufte-style dot emphasis at data points."""
    ax.plot(x, y, linestyle='-', color=color, linewidth=1, zorder=1)
    ax.scatter(x, y, color='white', s=80, zorder=2, edgecolors='none')
    ax.scatter(x, y, color=color, s=15, zorder=3, edgecolors='none')
    if label:
        label_line(ax, x, y, label, color=color)
```

---

## Tufte Bar Chart (White Gridlines)

Bars with horizontal white lines replacing traditional gridlines:

```python
def tufte_bar_chart(ax, categories, values, color=TUFTE_MEDIUM_GRAY):
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
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.02,
            f'{val}',
            ha='center', va='bottom',
            fontsize=10, fontfamily='serif', color=TUFTE_BLACK,
        )

    return bars
```

---

## Dot Plot (Alternative to Bar Chart)

For ranked categorical data:

```python
def tufte_dot_plot(ax, categories, values, color=TUFTE_BLACK):
    """Cleveland dot plot — Tufte-preferred alternative to bar charts."""
    y_pos = range(len(categories))
    ax.scatter(values, y_pos, color=color, s=40, zorder=3)
    ax.hlines(y_pos, 0, values, color=TUFTE_LIGHT_GRAY, linewidth=0.8, zorder=1)
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
def tufte_slope_chart(ax, labels, left_values, right_values,
                      left_label='Before', right_label='After',
                      highlight=None, accent_color=TUFTE_ACCENT):
    """Tufte-style slope chart for two-point comparisons."""
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
        color = accent_color if label == highlight else TUFTE_LIGHT_GRAY
        lw = 1.5 if label == highlight else 0.8
        ax.plot([0, 1], [left_positions[i], right_positions[i]],
                color=color, linewidth=lw)

        # Left label
        ax.text(-0.05, left_positions[i], f'{label} ({left_values[i]})',
                ha='right', va='center', fontsize=9, fontfamily='serif',
                color=TUFTE_BLACK if label == highlight else TUFTE_MEDIUM_GRAY)

        # Right label
        ax.text(1.05, right_positions[i], f'{label} ({right_values[i]})',
                ha='left', va='center', fontsize=9, fontfamily='serif',
                color=TUFTE_BLACK if label == highlight else TUFTE_MEDIUM_GRAY)

    # Column headers
    ax.text(0, max(left_positions) + 1, left_label,
            ha='center', va='bottom', fontsize=11, fontfamily='serif',
            fontweight='bold', color=TUFTE_BLACK)
    ax.text(1, max(right_positions) + 1, right_label,
            ha='center', va='bottom', fontsize=11, fontfamily='serif',
            fontweight='bold', color=TUFTE_BLACK)

    # Remove all axes
    ax.axis('off')
```

---

## Sparkline

Minimal, word-sized graphic:

```python
def tufte_sparkline(ax, data, color=TUFTE_BLACK, highlight_endpoints=True):
    """Create a Tufte sparkline — a word-sized data graphic."""
    x = range(len(data))
    ax.plot(x, data, color=color, linewidth=0.8)

    if highlight_endpoints:
        # Mark first and last points
        ax.scatter([x[0], x[-1]], [data[0], data[-1]],
                   color=color, s=8, zorder=3)
        # Mark min and max
        min_idx = np.argmin(data)
        max_idx = np.argmax(data)
        ax.scatter([min_idx], [data[min_idx]], color=TUFTE_ACCENT, s=8, zorder=3)
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
        tufte_sparkline(ax, data)
        ax.text(-1, np.mean(data), label, ha='right', va='center',
                fontsize=9, fontfamily='serif', color=TUFTE_BLACK)
        ax.text(len(data), data[-1], f' {data[-1]:.1f}',
                ha='left', va='center', fontsize=9, fontfamily='serif',
                color=TUFTE_BLACK)

    plt.subplots_adjust(hspace=0.5)
    return fig
```

---

## Small Multiples

```python
def tufte_small_multiples(data_dict, ncols=3, figsize=(10, 8),
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
            ax.plot(x, y, color=TUFTE_BLACK, linewidth=1)
        ax.set_title(title, fontsize=10, fontfamily='serif', pad=4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(direction='in', labelsize=8)

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

When seaborn is used, override its defaults to match Tufte style:

```python
import seaborn as sns

def apply_tufte_seaborn():
    """Override seaborn defaults with Tufte-style settings."""
    sns.set_style('white')  # not 'whitegrid' — we control gridlines
    sns.set_context('paper', font_scale=1.1)
    sns.set_palette([TUFTE_BLACK, TUFTE_MEDIUM_GRAY, TUFTE_ACCENT])

    # After every seaborn plot, call:
    # sns.despine()  — removes top/right spines
    # Then apply range frames manually if needed

# Post-plot cleanup for seaborn:
def tufte_cleanup_seaborn(ax, x_data=None, y_data=None):
    """Apply Tufte cleanup after a seaborn plot."""
    sns.despine(ax=ax)
    ax.tick_params(direction='in')
    if x_data is not None and y_data is not None:
        apply_range_frame(ax, x_data, y_data)
    ax.get_legend().remove() if ax.get_legend() else None
```

---

## Scatter Plot

```python
def tufte_scatter(ax, x, y, color=TUFTE_BLACK, label_points=None):
    """Tufte-style scatter plot with range frames."""
    ax.scatter(x, y, color=color, s=20, edgecolors='none', alpha=0.8)
    apply_range_frame(ax, x, y)

    # Optionally label specific points
    if label_points:
        for idx, text in label_points.items():
            ax.annotate(
                text, (x[idx], y[idx]),
                xytext=(5, 5), textcoords='offset points',
                fontsize=9, fontfamily='serif', color=TUFTE_BLACK,
            )
```

---

## Histogram

```python
def tufte_histogram(ax, data, bins=20, color=TUFTE_MEDIUM_GRAY):
    """Tufte-style histogram with white gridlines."""
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
def tufte_heatmap(ax, data, row_labels, col_labels, cmap='Greys'):
    """Tufte-style heatmap: no gridlines, direct value labels."""
    im = ax.imshow(data, cmap=cmap, aspect='auto')

    ax.set_xticks(range(len(col_labels)))
    ax.set_yticks(range(len(row_labels)))
    ax.set_xticklabels(col_labels, fontsize=9, fontfamily='serif')
    ax.set_yticklabels(row_labels, fontsize=9, fontfamily='serif')

    # Direct value labels in cells
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = data[i][j]
            text_color = 'white' if val > (max(map(max, data)) * 0.6) else TUFTE_BLACK
            ax.text(j, i, f'{val:.1f}', ha='center', va='center',
                    fontsize=9, fontfamily='serif', color=text_color)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(bottom=False, left=False)

    return im
```
