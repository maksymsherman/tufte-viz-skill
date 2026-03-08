# Plotly — Clean-Viz Patterns

Concrete code patterns for producing clean, publication-quality visualizations in Plotly (inspired by Edward Tufte's principles). Copy and adapt these patterns when generating visualization code.

---

## Base Layout Template

Apply this layout to every Plotly figure:

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Typography constants
CLEAN_FONT_SIZE = 11
CLEAN_TITLE_SIZE = 13
CLEAN_LABEL_SIZE = 10
CLEAN_SMALL_SIZE = 9

# Color constants
CLEAN_BLACK = '#333333'
CLEAN_MEDIUM_GRAY = '#888888'
CLEAN_LIGHT_GRAY = '#cccccc'
CLEAN_REF_GRAY = '#d0d0d0'   # reference lines behind bars on white background
CLEAN_ACCENT = '#c0392b'
CLEAN_COLORS = ['#332288', '#CC6677', '#117733', '#882255', '#44AA99', '#AA4499']
CLEAN_LINE_DASHES = ['solid', 'dash', 'dashdot', 'dot']

CLEAN_LAYOUT = dict(
    font=dict(family='Georgia, serif', size=CLEAN_FONT_SIZE, color=CLEAN_BLACK),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=30, t=40, b=50),
    title=dict(
        font=dict(size=CLEAN_TITLE_SIZE, family='Georgia, serif'),
        x=0,
        xanchor='left',
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        ticks='inside',
        tickfont=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE),
        mirror=False,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks='inside',
        tickfont=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE),
        mirror=False,
        zeroline=False,
    ),
)
```

Usage:

```python
fig = go.Figure(layout=CLEAN_LAYOUT)
fig.update_layout(title_text='Descriptive sentence-case title')
```

---

## Range Frames

Bind axis lines to the data range:

```python
def apply_plotly_range_frame(fig, x_data, y_data, x_pad_fraction=0.05, y_pad_fraction=0.05):
    """Approximate range frames with bounded axis-line shapes in data coordinates."""
    x_min, x_max = min(x_data), max(x_data)
    y_min, y_max = min(y_data), max(y_data)
    x_pad = (x_max - x_min) * x_pad_fraction or 1
    y_pad = (y_max - y_min) * y_pad_fraction or 1
    existing_shapes = list(fig.layout.shapes) if fig.layout.shapes else []

    fig.update_xaxes(
        range=[x_min - x_pad, x_max + x_pad],
        showline=False,
    )
    fig.update_yaxes(
        range=[y_min - y_pad, y_max + y_pad],
        showline=False,
    )
    fig.update_layout(shapes=existing_shapes + [
        dict(
            type='line',
            x0=x_min, x1=x_max, y0=y_min, y1=y_min,
            xref='x', yref='y',
            line=dict(color=CLEAN_BLACK, width=1),
        ),
        dict(
            type='line',
            x0=x_min, x1=x_min, y0=y_min, y1=y_max,
            xref='x', yref='y',
            line=dict(color=CLEAN_BLACK, width=1),
        ),
    ])
    return fig
```

---

## Line Chart

```python
def clean_line_chart(x, y, name='', color=CLEAN_BLACK):
    """Create a clean Plotly line chart."""
    fig = go.Figure(layout=CLEAN_LAYOUT)

    # Base line
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines',
        line=dict(color=color, width=1.5),
        showlegend=False,
    ))

    # Data point dots
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        marker=dict(color=color, size=5),
        showlegend=False,
    ))

    apply_plotly_range_frame(fig, x, y)

    # Direct label at end of series
    fig.add_annotation(
        x=x[-1], y=y[-1], text=name,
        showarrow=False, xanchor='left', xshift=8,
        font=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE, color=CLEAN_BLACK),
    )

    return fig
```

---

## Direct Annotations (Replace Legends)

```python
def add_series_label(fig, x_end, y_end, label):
    """Add a direct label at the end of a data series."""
    fig.add_annotation(
        x=x_end, y=y_end,
        text=label,
        showarrow=False,
        xanchor='left',
        xshift=8,
        font=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE, color=CLEAN_BLACK),
    )

def add_point_annotation(fig, x, y, text, color=CLEAN_BLACK):
    """Annotate a specific data point (max, min, notable value)."""
    fig.add_annotation(
        x=x, y=y,
        text=text,
        showarrow=True,
        arrowhead=0,
        arrowwidth=0.8,
        arrowcolor=CLEAN_MEDIUM_GRAY,
        ax=0, ay=-25,
        font=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE, color=color),
    )
```

---

## Bar Chart (White Gridlines)

```python
def clean_bar_chart(categories, values, color=CLEAN_MEDIUM_GRAY):
    """Bar chart with white gridlines."""
    fig = go.Figure(layout=CLEAN_LAYOUT)

    fig.add_trace(go.Bar(
        x=categories, y=values,
        marker_color=color,
        marker_line_width=0,
        text=[str(v) for v in values],
        textposition='outside',
        textfont=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE, color=CLEAN_BLACK),
    ))

    # White gridlines over bars
    fig.update_yaxes(
        showgrid=True,
        gridcolor='white',
        gridwidth=2,
        showline=False,
        ticks='',
        layer='above traces',
    )
    fig.update_xaxes(showline=False, ticks='')

    return fig
```

---

## Scatter Plot

```python
def clean_scatter(x, y, labels=None, color=CLEAN_BLACK):
    """Scatter with range frames and optional point labels."""
    fig = go.Figure(layout=CLEAN_LAYOUT)

    fig.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        marker=dict(color=color, size=6, opacity=0.8),
        showlegend=False,
    ))

    apply_plotly_range_frame(fig, x, y)

    # Direct point labels
    if labels:
        for xi, yi, label in labels:
            fig.add_annotation(
                x=xi, y=yi, text=label,
                showarrow=False, xshift=8, yshift=5,
                font=dict(family='Georgia, serif', size=CLEAN_SMALL_SIZE, color=CLEAN_BLACK),
            )

    return fig
```

---

## Small Multiples

```python
def clean_small_multiples(data_dict, ncols=3, chart_type='line'):
    """Create a grid of small multiples with shared axes."""
    n = len(data_dict)
    nrows = -(-n // ncols)  # ceiling division
    titles = list(data_dict.keys())

    fig = make_subplots(
        rows=nrows, cols=ncols,
        shared_xaxes=True, shared_yaxes=True,
        subplot_titles=titles,
        horizontal_spacing=0.04,
        vertical_spacing=0.08,
    )

    for i, (title, (x, y)) in enumerate(data_dict.items()):
        row = i // ncols + 1
        col = i % ncols + 1

        if chart_type == 'line':
            fig.add_trace(
                go.Scatter(x=x, y=y, mode='lines',
                           line=dict(color=CLEAN_BLACK, width=1.2),
                           showlegend=False),
                row=row, col=col,
            )
        elif chart_type == 'bar':
            fig.add_trace(
                go.Bar(x=x, y=y, marker_color=CLEAN_MEDIUM_GRAY,
                       showlegend=False),
                row=row, col=col,
            )

    # Apply clean-viz styling to all axes
    fig.update_xaxes(showgrid=False, ticks='inside', showline=False, zeroline=False)
    fig.update_yaxes(showgrid=False, ticks='inside', showline=False, zeroline=False)

    fig.update_layout(
        font=dict(family='Georgia, serif', size=CLEAN_SMALL_SIZE),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=50, r=20, t=40, b=40),
    )

    # Style subplot titles
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE, color=CLEAN_BLACK)

    return fig
```

---

## Sparkline

```python
def clean_sparkline(data, width=200, height=30):
    """Create a minimal sparkline figure."""
    x = list(range(len(data)))
    fig = go.Figure(layout=CLEAN_LAYOUT)

    fig.add_trace(go.Scatter(
        x=x, y=data, mode='lines',
        line=dict(color=CLEAN_BLACK, width=1),
        showlegend=False,
    ))

    # Highlight endpoints and extremes
    min_idx = data.index(min(data))
    max_idx = data.index(max(data))
    fig.add_trace(go.Scatter(
        x=[0, len(data) - 1, min_idx, max_idx],
        y=[data[0], data[-1], data[min_idx], data[max_idx]],
        mode='markers',
        marker=dict(
            color=[CLEAN_BLACK, CLEAN_BLACK, CLEAN_ACCENT, CLEAN_ACCENT],
            size=4,
        ),
        showlegend=False,
    ))

    fig.update_layout(
        width=width, height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    return fig
```

---

## Heatmap

```python
def clean_heatmap(z, x_labels, y_labels, colorscale='Greys'):
    """Heatmap with direct cell labels."""
    fig = go.Figure(layout=CLEAN_LAYOUT)

    fig.add_trace(go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale=colorscale,
        showscale=False,
    ))

    # Direct value annotations in cells
    for i, row in enumerate(z):
        for j, val in enumerate(row):
            # Use absolute value so both extremes of diverging colormaps get white text
            abs_max = max(abs(v) for row in z for v in row)
            text_color = 'white' if abs(val) > abs_max * 0.6 else CLEAN_BLACK
            fig.add_annotation(
                x=x_labels[j], y=y_labels[i],
                text=f'{val:.1f}',
                showarrow=False,
                font=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE, color=text_color),
            )

    fig.update_xaxes(showgrid=False, showline=False, ticks='')
    fig.update_yaxes(showgrid=False, showline=False, ticks='')

    return fig
```

---

## Multi-Series Line Chart

When comparing multiple series, use direct labels instead of a legend:

```python
def clean_multi_line(x, y_dict, colors=None):
    """Multiple line series with direct labels, line style variation, and collision-aware labeling."""
    if len(y_dict) > len(CLEAN_COLORS):
        raise ValueError('Use small multiples for more than 6 line series.')

    fig = go.Figure(layout=CLEAN_LAYOUT)
    palette = colors or CLEAN_COLORS

    all_y = []
    endpoints = []  # collect for collision-aware labeling
    for i, (name, y) in enumerate(y_dict.items()):
        color = palette[i % len(palette)]
        dash = CLEAN_LINE_DASHES[i % len(CLEAN_LINE_DASHES)]
        fig.add_trace(go.Scatter(
            x=x, y=y, mode='lines',
            line=dict(color=color, width=1.5, dash=dash),
            showlegend=False,
        ))
        endpoints.append((x[-1], y[-1], name, color))
        all_y.extend(y)

    # Collision-aware label placement: sort by y, enforce minimum gap.
    # Gap is based on the number of labels relative to the y-range,
    # ensuring labels don't overlap regardless of data scale.
    endpoints_sorted = sorted(endpoints, key=lambda e: e[1])
    y_range = max(all_y) - min(all_y)
    n_labels = len(endpoints_sorted)
    # Each label needs ~1.5 line-heights of space; scale to data units.
    # If all labels were stacked, they'd need n_labels * gap units of room.
    # Cap at 5% per label to avoid over-spreading on sparse data.
    min_gap = min((y_range or 1) * 0.05, (y_range or 1) / max(n_labels, 1) * 0.6)
    display_ys = []
    x_min, x_max = min(x), max(x)
    x_pad = (x_max - x_min) * 0.18 or 1
    label_x = x_max + x_pad * 0.35
    for i, (x_end, y_end, name, color) in enumerate(endpoints_sorted):
        pos = y_end
        if i > 0 and pos - display_ys[i - 1] < min_gap:
            pos = display_ys[i - 1] + min_gap
        display_ys.append(pos)
        fig.add_trace(go.Scatter(
            x=[label_x], y=[pos], mode='text',
            text=[name],
            textposition='middle left',
            textfont=dict(family='Georgia, serif', size=CLEAN_LABEL_SIZE, color=CLEAN_BLACK),
            showlegend=False,
            hoverinfo='skip',
        ))
        if pos != y_end:
            fig.add_shape(
                type='line',
                x0=x_end, y0=y_end, x1=label_x, y1=pos,
                xref='x', yref='y',
                line=dict(color=color, width=0.8),
            )

    apply_plotly_range_frame(fig, x, all_y, x_pad_fraction=0.18)
    return fig
```
