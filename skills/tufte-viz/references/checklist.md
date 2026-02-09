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

## Typography

- [ ] Font family is serif (Georgia, Palatino, Times New Roman, or generic serif)
- [ ] Title is sentence case (not ALL CAPS, not Title Case)
- [ ] Font sizes are consistent and readable (10-14pt range)
- [ ] No bold text except where emphasis is essential

## Labels and Legends

- [ ] Legend box removed; series are directly labeled on the plot
- [ ] Key data points are annotated (max, min, notable values)
- [ ] Redundant axis labels removed where title or context provides meaning
- [ ] No text overlaps with other text or data

## Color

- [ ] Default palette is grayscale
- [ ] At most one accent color used for emphasis
- [ ] No rainbow, jet, or spectral colormaps
- [ ] If multiple colors needed, using a colorblind-safe palette
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
- [ ] If gridlines present, they are either: thin light gray (#eeeeee) or white-on-bar technique
- [ ] Gridlines do not overlap with data markers

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

## Micro/Macro Readings

- [ ] Individual data points are readable at close inspection
- [ ] Overall patterns and trends are visible at a glance
- [ ] Sparklines are word-sized when used inline
- [ ] Small multiples share axes for valid comparison
