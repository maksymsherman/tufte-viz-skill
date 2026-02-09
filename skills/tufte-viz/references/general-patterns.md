# General Library Patterns — Altair, D3.js, ggplot2, Observable Plot

Tufte-style patterns for visualization libraries beyond matplotlib and Plotly. Apply the same core principles: maximize data-ink ratio, remove chartjunk, use range frames, direct labeling, and serif typography.

---

## Altair (Python)

### Theme Configuration

```python
import altair as alt

def tufte_theme():
    return {
        'config': {
            'view': {'strokeWidth': 0},
            'axis': {
                'domainColor': '#333333',
                'domainWidth': 1,
                'grid': False,
                'labelFont': 'Georgia, serif',
                'labelFontSize': 10,
                'labelColor': '#333333',
                'tickColor': '#333333',
                'tickSize': 4,
                'titleFont': 'Georgia, serif',
                'titleFontSize': 12,
                'titleFontWeight': 'normal',
                'titleColor': '#333333',
            },
            'header': {
                'labelFont': 'Georgia, serif',
                'titleFont': 'Georgia, serif',
            },
            'legend': {
                'labelFont': 'Georgia, serif',
                'titleFont': 'Georgia, serif',
            },
            'title': {
                'font': 'Georgia, serif',
                'fontSize': 14,
                'fontWeight': 'normal',
                'color': '#333333',
                'anchor': 'start',
            },
            'background': 'white',
        }
    }

alt.themes.register('tufte', tufte_theme)
alt.themes.enable('tufte')
```

### Line Chart with Direct Labels

```python
def tufte_line_chart(df, x_col, y_col, color_col=None):
    """Tufte-style line chart in Altair with direct labels."""
    base = alt.Chart(df).encode(
        x=alt.X(x_col, axis=alt.Axis(grid=False)),
        y=alt.Y(y_col, axis=alt.Axis(grid=False)),
    )

    line = base.mark_line(strokeWidth=1.5, color='#333333')

    if color_col:
        line = base.encode(
            color=alt.Color(color_col, legend=None),
        ).mark_line(strokeWidth=1.5)

        # Direct labels at end of each series
        labels = base.encode(
            color=alt.Color(color_col, legend=None),
            text=color_col,
        ).mark_text(
            align='left', dx=5, font='Georgia',
            fontSize=10,
        ).transform_filter(
            alt.datum[x_col] == df[x_col].max()
        )
        return (line + labels).properties(width=500, height=300)

    return line.properties(width=500, height=300)
```

### Bar Chart

```python
def tufte_bar_chart(df, x_col, y_col):
    """Tufte-style bar chart in Altair."""
    bars = alt.Chart(df).mark_bar(color='#888888').encode(
        x=alt.X(x_col, axis=alt.Axis(grid=False, ticks=False)),
        y=alt.Y(y_col, axis=alt.Axis(grid=False, ticks=False)),
    )

    text = bars.mark_text(
        align='center', dy=-8,
        font='Georgia', fontSize=10, color='#333333',
    ).encode(text=y_col)

    return (bars + text).properties(width=400, height=300).configure_view(
        strokeWidth=0
    )
```

### Small Multiples (Faceting)

```python
def tufte_facet(df, x_col, y_col, facet_col, columns=3):
    """Tufte-style small multiples via Altair faceting."""
    return alt.Chart(df).mark_line(
        strokeWidth=1.2, color='#333333'
    ).encode(
        x=alt.X(x_col, axis=alt.Axis(grid=False)),
        y=alt.Y(y_col, axis=alt.Axis(grid=False)),
    ).facet(
        facet=alt.Facet(facet_col, header=alt.Header(
            labelFont='Georgia', labelFontSize=11,
            titleFont='Georgia',
        )),
        columns=columns,
    ).resolve_scale(
        x='shared', y='shared'
    )
```

---

## D3.js (JavaScript)

### Base Setup

```javascript
// Tufte-style D3 defaults
const TUFTE = {
  fontFamily: 'Georgia, serif',
  fontSize: 12,
  textColor: '#333333',
  lineColor: '#333333',
  mediumGray: '#888888',
  lightGray: '#cccccc',
  accent: '#c0392b',
  margin: { top: 20, right: 80, bottom: 40, left: 50 },
};
```

### Spine Removal and Axis Styling

```javascript
function tufteAxes(svg, xAxis, yAxis, xData, yData) {
  // X axis — bottom only, bounded to data range
  const xAxisGroup = svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(xAxis.tickSizeInner(-4).tickSizeOuter(0));

  // Y axis — left only, bounded to data range
  const yAxisGroup = svg.append('g')
    .call(yAxis.tickSizeInner(-4).tickSizeOuter(0));

  // Remove domain lines beyond data range (range frame effect)
  // Achieved by limiting the scale domain tightly to data
  xAxisGroup.select('.domain')
    .attr('d', `M${xScale(d3.min(xData))},0H${xScale(d3.max(xData))}`);
  yAxisGroup.select('.domain')
    .attr('d', `M0,${yScale(d3.min(yData))}V${yScale(d3.max(yData))}`);

  // Style ticks and labels
  svg.selectAll('.tick text')
    .style('font-family', TUFTE.fontFamily)
    .style('font-size', `${TUFTE.fontSize}px`)
    .style('fill', TUFTE.textColor);

  svg.selectAll('.tick line')
    .style('stroke', TUFTE.lineColor);
}
```

### Direct Labeling

```javascript
function directLabel(svg, x, y, text, color = TUFTE.textColor) {
  svg.append('text')
    .attr('x', x + 8)
    .attr('y', y)
    .attr('dy', '0.35em')
    .attr('font-family', TUFTE.fontFamily)
    .attr('font-size', TUFTE.fontSize)
    .attr('fill', color)
    .text(text);
}
```

### Line Chart with Dot Emphasis

```javascript
function tufteLine(svg, data, xScale, yScale, color = TUFTE.lineColor) {
  const line = d3.line()
    .x(d => xScale(d.x))
    .y(d => yScale(d.y));

  // Base line
  svg.append('path')
    .datum(data)
    .attr('fill', 'none')
    .attr('stroke', color)
    .attr('stroke-width', 1.2)
    .attr('d', line);

  // White mask circles
  svg.selectAll('.mask-dot')
    .data(data)
    .enter().append('circle')
    .attr('cx', d => xScale(d.x))
    .attr('cy', d => yScale(d.y))
    .attr('r', 5)
    .attr('fill', 'white');

  // Data dots
  svg.selectAll('.data-dot')
    .data(data)
    .enter().append('circle')
    .attr('cx', d => xScale(d.x))
    .attr('cy', d => yScale(d.y))
    .attr('r', 2.5)
    .attr('fill', color);
}
```

---

## R / ggplot2

### Using ggthemes::theme_tufte

```r
library(ggplot2)
library(ggthemes)

# Base Tufte-styled plot
p <- ggplot(df, aes(x = x, y = y)) +
  geom_line(color = "#333333", linewidth = 0.8) +
  geom_point(color = "#333333", size = 1.5) +
  theme_tufte(base_family = "serif", base_size = 12) +
  labs(title = "Descriptive sentence-case title")
```

### Range Frames with ggthemes

```r
library(ggthemes)

p <- ggplot(df, aes(x = x, y = y)) +
  geom_rangeframe(color = "#333333") +
  geom_point(color = "#333333", size = 1.5) +
  theme_tufte(base_family = "serif") +
  scale_x_continuous(breaks = extended_range_breaks()(df$x)) +
  scale_y_continuous(breaks = extended_range_breaks()(df$y))
```

### Direct Labels (Replace Legends)

```r
library(ggrepel)

# Label the last point of each series
last_points <- df %>%
  group_by(series) %>%
  filter(x == max(x))

p <- ggplot(df, aes(x = x, y = y, color = series)) +
  geom_line(linewidth = 0.8, show.legend = FALSE) +
  geom_text_repel(
    data = last_points,
    aes(label = series),
    direction = "y", hjust = 0, nudge_x = 0.5,
    segment.color = NA, family = "serif", size = 3.5
  ) +
  scale_color_manual(values = c("#333333", "#888888", "#c0392b")) +
  theme_tufte(base_family = "serif") +
  theme(legend.position = "none")
```

### Small Multiples

```r
p <- ggplot(df, aes(x = x, y = y)) +
  geom_line(color = "#333333", linewidth = 0.8) +
  facet_wrap(~category, scales = "fixed", ncol = 3) +
  theme_tufte(base_family = "serif") +
  theme(
    strip.text = element_text(family = "serif", size = 10, hjust = 0),
    panel.spacing = unit(0.8, "lines")
  )
```

### Bar Chart

```r
p <- ggplot(df, aes(x = reorder(category, value), y = value)) +
  geom_bar(stat = "identity", fill = "#888888", width = 0.6) +
  geom_text(aes(label = value), vjust = -0.5, family = "serif", size = 3.5) +
  coord_flip() +
  theme_tufte(base_family = "serif") +
  theme(
    axis.ticks = element_blank(),
    panel.grid.major.x = element_line(color = "white", linewidth = 1)
  )
```

---

## Observable Plot (JavaScript)

### Base Configuration

```javascript
Plot.plot({
  style: {
    fontFamily: "Georgia, serif",
    fontSize: 12,
    background: "white",
  },
  x: { grid: false, tickSize: 4, line: true },
  y: { grid: false, tickSize: 4, line: true },
  marks: [
    Plot.line(data, {
      x: "date",
      y: "value",
      stroke: "#333333",
      strokeWidth: 1.2,
    }),
    Plot.dot(data, {
      x: "date",
      y: "value",
      fill: "#333333",
      r: 2.5,
    }),
    // Direct label at the last point
    Plot.text(
      data.filter((d, i) => i === data.length - 1),
      {
        x: "date",
        y: "value",
        text: () => "Series name",
        dx: 8,
        fontFamily: "Georgia",
        fontSize: 11,
        fill: "#333333",
      }
    ),
  ],
  width: 600,
  height: 350,
  marginRight: 80,
})
```

### Bar Chart

```javascript
Plot.plot({
  style: { fontFamily: "Georgia, serif", background: "white" },
  x: { grid: false, line: false, ticks: false },
  y: { grid: true, gridColor: "white", gridWidth: 2, line: false, ticks: false },
  marks: [
    Plot.barY(data, {
      x: "category",
      y: "value",
      fill: "#888888",
    }),
    Plot.text(data, {
      x: "category",
      y: "value",
      text: "value",
      dy: -8,
      fontFamily: "Georgia",
      fontSize: 10,
      fill: "#333333",
    }),
  ],
})
```

### Small Multiples (Faceting)

```javascript
Plot.plot({
  style: { fontFamily: "Georgia, serif", background: "white" },
  facet: { data: data, x: "category" },
  x: { grid: false, line: true },
  y: { grid: false, line: true },
  marks: [
    Plot.frame({ strokeOpacity: 0 }),
    Plot.line(data, {
      x: "date",
      y: "value",
      stroke: "#333333",
      strokeWidth: 1.2,
    }),
  ],
})
```

---

## Universal Checklist for Any Library

Regardless of which library you use, verify these after generating code:

1. **Spines**: Only bottom and left remain; top and right removed
2. **Range frames**: Spine bounds match data extent (not axis extent)
3. **Font**: Serif family specified explicitly
4. **Ticks**: Inward direction, reduced density
5. **Grid**: Removed or white-on-bar only
6. **Legend**: Removed; replaced with direct labels
7. **Colors**: Grayscale default, single accent if needed
8. **Background**: Pure white, no fills or images
9. **Title**: Sentence case, positioned at left
10. **Chart type**: No pie, 3D, dual-axis, or other banned types
