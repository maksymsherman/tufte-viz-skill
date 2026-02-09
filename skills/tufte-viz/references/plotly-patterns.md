# Plotly — Tufte Patterns

Concrete code patterns for producing Tufte-style visualizations in Plotly. Copy and adapt these patterns when generating visualization code.

---

## Base Layout Template

Apply this layout to every Plotly figure:

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

TUFTE_LAYOUT = dict(
    font=dict(family='Georgia, serif', size=12, color='#333333'),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=30, t=40, b=50),
    title=dict(
        font=dict(size=14, family='Georgia, serif'),
        x=0,
        xanchor='left',
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='#333333',
        linewidth=1,
        ticks='inside',
        tickfont=dict(family='Georgia, serif', size=10),
        mirror=False,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='#333333',
        linewidth=1,
        ticks='inside',
        tickfont=dict(family='Georgia, serif', size=10),
        mirror=False,
        zeroline=False,
    ),
)

# Color constants
TUFTE_BLACK = '#333333'
TUFTE_MEDIUM_GRAY = '#888888'
TUFTE_LIGHT_GRAY = '#cccccc'
TUFTE_ACCENT = '#c0392b'
```

Usage:

```python
fig = go.Figure(layout=TUFTE_LAYOUT)
fig.update_layout(title_text='Descriptive sentence-case title')
```

---

## Range Frames

Bind axis lines to the data range:

```python
def apply_plotly_range_frame(fig, x_data, y_data):
    """Constrain axis lines to span only the data range."""
    x_min, x_max = min(x_data), max(x_data)
    y_min, y_max = min(y_data), max(y_data)
    x_pad = (x_max - x_min) * 0.05
    y_pad = (y_max - y_min) * 0.05

    fig.update_xaxes(
        range=[x_min - x_pad, x_max + x_pad],
        showline=True,
        linecolor=TUFTE_BLACK,
        linewidth=1,
    )
    fig.update_yaxes(
        range=[y_min - y_pad, y_max + y_pad],
        showline=True,
        linecolor=TUFTE_BLACK,
        linewidth=1,
    )
    return fig
```

---

## Line Chart

```python
def tufte_line_chart(x, y, name='', color=TUFTE_BLACK):
    """Create a Tufte-style Plotly line chart."""
    fig = go.Figure(layout=TUFTE_LAYOUT)

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
        font=dict(family='Georgia, serif', size=11, color=color),
    )

    return fig
```

---

## Direct Annotations (Replace Legends)

```python
def add_series_label(fig, x_end, y_end, label, color=TUFTE_BLACK):
    """Add a direct label at the end of a data series."""
    fig.add_annotation(
        x=x_end, y=y_end,
        text=label,
        showarrow=False,
        xanchor='left',
        xshift=8,
        font=dict(family='Georgia, serif', size=11, color=color),
    )

def add_point_annotation(fig, x, y, text, color=TUFTE_BLACK):
    """Annotate a specific data point (max, min, notable value)."""
    fig.add_annotation(
        x=x, y=y,
        text=text,
        showarrow=True,
        arrowhead=0,
        arrowwidth=0.8,
        arrowcolor=TUFTE_MEDIUM_GRAY,
        ax=0, ay=-25,
        font=dict(family='Georgia, serif', size=10, color=color),
    )
```

---

## Bar Chart (White Gridlines)

```python
def tufte_bar_chart(categories, values, color=TUFTE_MEDIUM_GRAY):
    """Tufte-style bar chart with white gridlines."""
    fig = go.Figure(layout=TUFTE_LAYOUT)

    fig.add_trace(go.Bar(
        x=categories, y=values,
        marker_color=color,
        marker_line_width=0,
        text=[str(v) for v in values],
        textposition='outside',
        textfont=dict(family='Georgia, serif', size=10, color=TUFTE_BLACK),
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
def tufte_scatter(x, y, labels=None, color=TUFTE_BLACK):
    """Tufte-style scatter with range frames and optional point labels."""
    fig = go.Figure(layout=TUFTE_LAYOUT)

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
                font=dict(family='Georgia, serif', size=9, color=TUFTE_BLACK),
            )

    return fig
```

---

## Small Multiples

```python
def tufte_small_multiples(data_dict, ncols=3, chart_type='line'):
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
                           line=dict(color=TUFTE_BLACK, width=1.2),
                           showlegend=False),
                row=row, col=col,
            )
        elif chart_type == 'bar':
            fig.add_trace(
                go.Bar(x=x, y=y, marker_color=TUFTE_MEDIUM_GRAY,
                       showlegend=False),
                row=row, col=col,
            )

    # Apply Tufte styling to all axes
    fig.update_xaxes(showgrid=False, ticks='inside', showline=True,
                     linecolor=TUFTE_BLACK, linewidth=1, zeroline=False)
    fig.update_yaxes(showgrid=False, ticks='inside', showline=True,
                     linecolor=TUFTE_BLACK, linewidth=1, zeroline=False)

    fig.update_layout(
        font=dict(family='Georgia, serif', size=10),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=50, r=20, t=40, b=40),
    )

    # Style subplot titles
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family='Georgia, serif', size=11, color=TUFTE_BLACK)

    return fig
```

---

## Sparkline

```python
def tufte_sparkline(data, width=200, height=30):
    """Create a minimal sparkline figure."""
    x = list(range(len(data)))
    fig = go.Figure(layout=TUFTE_LAYOUT)

    fig.add_trace(go.Scatter(
        x=x, y=data, mode='lines',
        line=dict(color=TUFTE_BLACK, width=1),
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
            color=[TUFTE_BLACK, TUFTE_BLACK, TUFTE_ACCENT, '#117733'],
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
def tufte_heatmap(z, x_labels, y_labels, colorscale='Greys'):
    """Tufte-style heatmap with direct cell labels."""
    fig = go.Figure(layout=TUFTE_LAYOUT)

    fig.add_trace(go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale=colorscale,
        showscale=False,
    ))

    # Direct value annotations in cells
    for i, row in enumerate(z):
        for j, val in enumerate(row):
            max_val = max(max(r) for r in z)
            text_color = 'white' if val > max_val * 0.6 else TUFTE_BLACK
            fig.add_annotation(
                x=x_labels[j], y=y_labels[i],
                text=f'{val:.1f}',
                showarrow=False,
                font=dict(family='Georgia, serif', size=10, color=text_color),
            )

    fig.update_xaxes(showgrid=False, showline=False, ticks='')
    fig.update_yaxes(showgrid=False, showline=False, ticks='')

    return fig
```

---

## Multi-Series Line Chart

When comparing multiple series, use direct labels instead of a legend:

```python
def tufte_multi_line(x, y_dict, colors=None):
    """Multiple line series with direct labels, no legend."""
    fig = go.Figure(layout=TUFTE_LAYOUT)
    palette = colors or [TUFTE_BLACK, TUFTE_MEDIUM_GRAY, TUFTE_ACCENT, TUFTE_LIGHT_GRAY]

    all_y = []
    for i, (name, y) in enumerate(y_dict.items()):
        color = palette[i % len(palette)]
        fig.add_trace(go.Scatter(
            x=x, y=y, mode='lines',
            line=dict(color=color, width=1.5),
            showlegend=False,
        ))
        add_series_label(fig, x[-1], y[-1], name, color=color)
        all_y.extend(y)

    apply_plotly_range_frame(fig, x, all_y)
    return fig
```
