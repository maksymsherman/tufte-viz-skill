# Post-Generation Verification Checklist

Run through every item after generating visualization code. Each item is pass/fail. Fix any failures before presenting the code to the user.

---

## Data-Ink Ratio

- [ ] Every visual element encodes data or directly aids interpretation
- [ ] No decorative elements remain (borders, fills, shadows, images)
- [ ] No redundant encoding (same data shown in position AND color AND label without purpose)

## Axes and Frames

- [ ] Top spine removed
- [ ] Right spine removed
- [ ] Bottom spine bounded to data range (range frame)
- [ ] Left spine bounded to data range (range frame)
- [ ] Tick marks face inward
- [ ] Tick density is reduced from library defaults
- [ ] No tick label rotation (if labels are long, use horizontal bar chart)
- [ ] **No tick/spine overshoot**: after any `set_xlim`/`set_ylim` override (e.g., for label padding), verify that tick marks and spine bounds do not extend beyond the data range

## Typography

- [ ] Font family is serif (Georgia, Palatino, Times New Roman, or generic serif)
- [ ] Title is sentence case (not ALL CAPS, not Title Case)
- [ ] Font sizes are consistent and readable (10-14pt range)
- [ ] **Font size consistency**: all manually-placed text (`ax.text`, `ax.annotate`, `add_annotation`) references the global typography constants (`CLEAN_LABEL_SIZE`, `CLEAN_SMALL_SIZE`) — no bare numeric `fontsize` values
- [ ] **Label color consistency**: all label text uses `CLEAN_BLACK` unless intentionally de-emphasized — no bare `color='gray'` or `color='#888888'` except for explicitly muted elements
- [ ] No bold text except where emphasis is essential

## Labels and Legends

- [ ] Legend box removed; series are directly labeled on the plot
- [ ] Key data points annotated where they tell a story (outliers, named entities, inflection points) — NOT raw coordinate tuples for min/max that range frames already communicate
- [ ] Axis labels with units of measurement are present — only omit axis labels when both meaning and unit are obvious from context (e.g., "Year" when ticks are "2018, 2019, 2020")
- [ ] Label precision matches data — no trailing `.0` on whole numbers; minimum decimal places needed
- [ ] **No label-to-label collisions**: check that every direct label has clear space from all other direct labels — especially when series have similar endpoint values
- [ ] **No label-to-data collisions**: check that labels do not overlap with nearby data points, lines, or markers
- [ ] If labels were displaced to avoid collisions, leader lines or offsets make the association clear
- [ ] **Multi-series distinguishability**: series can be told apart without color — verify line style variation (solid/dashed/dash-dot/dotted) or marker shape variation is present. This is essential for accessibility, print, and small panels

## Color

- [ ] Default palette is grayscale
- [ ] At most one accent color used for emphasis
- [ ] No rainbow, jet, or spectral colormaps
- [ ] If multiple colors needed, using a colorblind-safe palette
- [ ] Colors used for lines and text have sufficient contrast on white — no low-contrast colors (cyan `#88CCEE`, olive `#999933`) for thin lines or small text. Low-contrast colors are acceptable for bars and filled areas
- [ ] Legend text and labels use `CLEAN_BLACK`, not the series color, when the series color is low-contrast
- [ ] No gradient fills on bars or areas
- [ ] Background is white

## Chart Type

- [ ] No pie or donut charts
- [ ] No 3D effects or perspective
- [ ] No dual-axis charts
- [ ] No radar/spider charts
- [ ] No gauge/speedometer charts
- [ ] No word clouds
- [ ] If a banned type was requested, a substitute was offered with explanation

## Gridlines

- [ ] No heavy or dark gridlines
- [ ] If gridlines present, they use the correct technique for context: white on top of colored bars; `#d0d0d0` behind bars on white background
- [ ] Gridlines do not overlap with data markers
- [ ] **Reference line visibility**: if reference lines were added, verify they are visually distinguishable from the background at the output resolution — `#eeeeee` lines on a white background fail this check

## Graphical Integrity

- [ ] Axes start at zero where appropriate (bar charts always; line charts when meaningful)
- [ ] No broken or truncated axes without clear notation
- [ ] Scale is consistent across all panels in small multiples
- [ ] Area/radius encodings are proportional to data values (no inflated bubbles)
- [ ] Aspect ratio does not exaggerate or minimize trends

## Data Density

- [ ] Chart uses available space efficiently
- [ ] Margins are tight (tight_layout or equivalent applied)
- [ ] Small multiples used instead of overloaded single chart where appropriate
- [ ] No excessive whitespace within the plot area
- [ ] **No summary-only charts when raw data is available**: if the chart shows only summary statistics (e.g., means, medians) for groups, and the underlying data has >10 points per group, show individual data points instead (strip plot, jitter plot, beeswarm) with the summary statistic overlaid. Summary-only charts hide distribution shape, outliers, and sample size.

## Micro/Macro Readings

- [ ] Individual data points are readable at close inspection
- [ ] Overall patterns and trends are visible at a glance
- [ ] Sparklines are word-sized when used inline
- [ ] Small multiples share axes for valid comparison

## Multi-Chart Cohesion (when generating 2+ charts in a session)

- [ ] Same color palette and color-to-meaning assignments across all charts
- [ ] Same font family, base font size, title size, and label size
- [ ] Same axis styling (spine treatment, tick direction, range frames)
- [ ] Same or compatible figure dimensions / aspect ratios
- [ ] Same line widths, marker sizes, and bar widths
- [ ] Categories that appear in multiple charts use the same sort order

## Small-Panel Scaling (for small multiples and multi-panel layouts)

- [ ] Line widths are thick enough to be visible at panel size
- [ ] Font sizes are readable at panel size (not below 8pt rendered)
- [ ] Dot emphasis is not used for 3+ series at small panel sizes
- [ ] Per-panel annotations are omitted or limited to a single highlighted panel
- [ ] Reference lines are visible or omitted entirely (not invisibly thin)
