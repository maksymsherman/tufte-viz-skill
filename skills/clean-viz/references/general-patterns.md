# General Library Patterns — Altair, D3.js, ggplot2, Observable Plot

Clean-viz patterns for visualization libraries beyond matplotlib and Plotly (inspired by Edward Tufte's principles). Apply the same core principles: maximize data-ink ratio, remove chartjunk, use range frames, direct labeling, and serif typography.

Altair and ggplot2 examples below are runnable starting points. D3.js and Observable Plot examples are pattern sketches to adapt into an existing chart scaffold with scales and layout already defined.

---

## Altair (Python)

### Theme Configuration

```python
import altair as alt

CLEAN = {
    'font': 'Georgia, serif',
    'font_size': 11,
    'label_size': 10,
    'title_size': 13,
    'black': '#333333',
    'medium_gray': '#888888',
    'colors': ['#332288', '#CC6677', '#117733', '#882255', '#44AA99', '#AA4499'],
}

def clean_theme():
    return {
        'config': {
            'view': {'strokeWidth': 0},
            'axis': {
                'domainColor': CLEAN['black'],
                'domainWidth': 1,
                'grid': False,
                'labelFont': CLEAN['font'],
                'labelFontSize': CLEAN['label_size'],
                'labelColor': CLEAN['black'],
                'tickColor': CLEAN['black'],
                'tickSize': 4,
                'titleFont': CLEAN['font'],
                'titleFontSize': CLEAN['font_size'],
                'titleFontWeight': 'normal',
                'titleColor': CLEAN['black'],
            },
            'header': {
                'labelFont': CLEAN['font'],
                'titleFont': CLEAN['font'],
            },
            'legend': {
                'labelFont': CLEAN['font'],
                'titleFont': CLEAN['font'],
            },
            'title': {
                'font': CLEAN['font'],
                'fontSize': CLEAN['title_size'],
                'fontWeight': 'normal',
                'color': CLEAN['black'],
                'anchor': 'start',
            },
            'background': 'white',
        }
    }

alt.themes.register('clean', clean_theme)
alt.themes.enable('clean')
```

### Line Chart with Direct Labels

```python
def _field_name(shorthand):
    """Resolve Altair shorthand like 'year:Q' to the raw field name."""
    parsed = alt.utils.parse_shorthand(shorthand)
    return parsed.get('field', shorthand).replace('\\:', ':')

def clean_line_chart(df, x_col, y_col, color_col=None):
    """Line chart in Altair with direct labels.

    Accepts either raw field names or Altair shorthand such as 'year:Q'.
    """
    base = alt.Chart(df).encode(
        x=alt.X(x_col, axis=alt.Axis(grid=False)),
        y=alt.Y(y_col, axis=alt.Axis(grid=False)),
    )

    line = base.mark_line(strokeWidth=1.5, color=CLEAN['black'])

    if color_col:
        x_field = _field_name(x_col)
        color_field = _field_name(color_col)
        line = base.mark_line(strokeWidth=1.5).encode(
            color=alt.Color(color_col, legend=None, scale=alt.Scale(range=CLEAN['colors'])),
        )

        labels = alt.Chart(df).transform_joinaggregate(
            max_x=f'max({x_field})',
            groupby=[color_field],
        ).transform_filter(
            f'datum.{x_field} == datum.max_x'
        ).mark_text(
            align='left', dx=6, font='Georgia',
            fontSize=CLEAN['label_size'], color=CLEAN['black'],
        ).encode(
            x=x_col,
            y=y_col,
            text=color_field,
        )
        return (line + labels).properties(width=500, height=300)

    return line.properties(width=500, height=300)
```

### Bar Chart

```python
def clean_bar_chart(df, x_col, y_col):
    """Bar chart in Altair."""
    bars = alt.Chart(df).mark_bar(color=CLEAN['medium_gray']).encode(
        x=alt.X(x_col, axis=alt.Axis(grid=False, ticks=False)),
        y=alt.Y(y_col, axis=alt.Axis(grid=False, ticks=False)),
    )

    text = bars.mark_text(
        align='center', dy=-8,
        font='Georgia', fontSize=CLEAN['label_size'], color=CLEAN['black'],
    ).encode(text=y_col)

    return (bars + text).properties(width=400, height=300).configure_view(
        strokeWidth=0
    )
```

### Small Multiples (Faceting)

```python
def clean_facet(df, x_col, y_col, facet_col, columns=3):
    """Small multiples via Altair faceting."""
    return alt.Chart(df).mark_line(
        strokeWidth=1.2, color=CLEAN['black']
    ).encode(
        x=alt.X(x_col, axis=alt.Axis(grid=False)),
        y=alt.Y(y_col, axis=alt.Axis(grid=False)),
    ).facet(
        facet=alt.Facet(facet_col, header=alt.Header(
            labelFont='Georgia', labelFontSize=CLEAN['font_size'],
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
// Clean-viz D3 defaults
const CLEAN = {
  fontFamily: 'Georgia, serif',
  fontSize: 12,
  labelSize: 10,
  textColor: '#333333',
  lineColor: '#333333',
  mediumGray: '#888888',
  lightGray: '#cccccc',
  refGray: '#d0d0d0',    // reference lines behind bars on white
  accent: '#c0392b',
  margin: { top: 20, right: 80, bottom: 40, left: 50 },
};
```

### Spine Removal and Axis Styling

```javascript
function cleanAxes(svg, xScale, yScale, width, height) {
  const xAxis = d3.axisBottom(xScale).ticks(5).tickSizeOuter(0);
  const yAxis = d3.axisLeft(yScale).ticks(5).tickSizeOuter(0);

  const xAxisGroup = svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(xAxis);

  const yAxisGroup = svg.append('g')
    .call(yAxis);

  // Trim the visible domain lines to the plotting area.
  xAxisGroup.select('.domain').attr('d', `M0,0H${width}`);
  yAxisGroup.select('.domain').attr('d', `M0,0V${height}`);

  // Style ticks and labels
  svg.selectAll('.tick text')
    .style('font-family', CLEAN.fontFamily)
    .style('font-size', `${CLEAN.labelSize}px`)
    .style('fill', CLEAN.textColor);

  svg.selectAll('.tick line')
    .style('stroke', CLEAN.lineColor);
}
```

### Direct Labeling

```javascript
function directLabel(svg, x, y, text, labelColor = CLEAN.textColor) {
  svg.append('text')
    .attr('x', x + 8)
    .attr('y', y)
    .attr('dy', '0.35em')
    .attr('font-family', CLEAN.fontFamily)
    .attr('font-size', CLEAN.labelSize)
    .attr('fill', labelColor)
    .text(text);
}
```

### Multi-Series Differentiation

For multi-series charts, vary `stroke-dasharray` alongside color:

```javascript
const CLEAN_DASHES = ['', '6,3', '6,3,2,3', '2,3'];  // solid, dash, dash-dot, dot
// Usage: .attr('stroke-dasharray', CLEAN_DASHES[i])
```

The dot-emphasis technique (below) works for single-series only. For multi-series, use
line style variation instead — the white mask circles homogenize dots across series.

### Line Chart with Dot Emphasis (Single Series)

```javascript
function cleanLine(svg, data, xScale, yScale, color = CLEAN.lineColor) {
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
library(dplyr)
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
    segment.color = "#cccccc", family = "serif", size = 3.5, color = "#333333"
  ) +
  scale_color_manual(values = c("#332288", "#CC6677", "#117733", "#882255")) +
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

## Audit Reminder for Any Library

Regardless of which library you use, finish with the same audit contract:

1. **Code checks**: always run them before finalizing
2. **Rendered checks**: only mark them passed after rendering or visually inspecting the chart
3. **Session consistency**: run them when generating 2+ related charts
4. **Audit block**: include `Code checks`, `Rendered checks`, and `Session consistency` in the final response
