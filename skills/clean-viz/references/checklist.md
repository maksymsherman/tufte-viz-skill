# Visualization Quality Gate

Run this before presenting any visualization. The checklist is mandatory, but not every item can be honestly marked as verified in every environment.

Use these statuses:

- `passed` — verified and acceptable
- `fixed` — was wrong, corrected before finalizing
- `failed` — still wrong; do not finalize
- `not visually verified` — cannot honestly confirm without rendering or inspecting the output
- `n/a` — not relevant to this chart

## 1. Code Checks

These are mandatory for every chart, even if no rendering step is available.

### Chart Type and Integrity

- [ ] No pie or donut charts unless the user insisted after seeing a substitute
- [ ] No 3D effects or perspective
- [ ] No dual-axis charts
- [ ] No radar/spider charts
- [ ] No gauge/speedometer charts
- [ ] No word clouds
- [ ] If a banned type was requested, the response explains the problem and offers a substitute
- [ ] Axes start at zero where appropriate (bar charts always; line charts when meaningful)
- [ ] No broken or truncated axes without clear notation
- [ ] Area or radius encodings are proportional to the data

### Axes, Frames, and Scale

- [ ] Top and right spines removed when the library supports spines
- [ ] Bottom and left axis lines are bounded to the data range, or the closest library-specific approximation is used
- [ ] Tick marks face inward or use the closest library-specific approximation
- [ ] Tick density is reduced from library defaults
- [ ] No rotated tick labels unless the library leaves no reasonable alternative
- [ ] After any axis padding for labels, tick marks and range-frame bounds remain anchored to the data range
- [ ] Small multiples share scales when comparisons depend on shared scale

### Typography and Labeling

- [ ] Font family is serif
- [ ] Title is sentence case
- [ ] Manually placed text uses named typography constants or a single shared style object
- [ ] Label text defaults to `CLEAN_BLACK` or the library's equivalent neutral text color, unless intentionally de-emphasized
- [ ] Legend box is removed when direct labels are viable
- [ ] Axis labels include units unless both the measure and unit are already obvious
- [ ] Label precision matches the data
- [ ] Key annotations add context rather than repeating raw min/max coordinates
- [ ] Multi-series charts are distinguishable without color alone

### Color and Styling

- [ ] Default palette is grayscale
- [ ] At most one accent color is used for emphasis
- [ ] No rainbow, jet, or spectral colormaps
- [ ] If multiple colors are necessary, use a colorblind-safe palette
- [ ] Low-contrast colors are not used for thin lines or small text on white
- [ ] No gradient fills on bars or areas
- [ ] Background is white
- [ ] Gridlines, if present, use the correct context-specific treatment

### Density and Completeness

- [ ] Chart uses space efficiently and avoids excessive whitespace in the plot area
- [ ] Margins are tightened (`tight_layout()` or equivalent)
- [ ] Small multiples are used instead of overloading a single chart when needed
- [ ] Summary-only categorical charts are avoided when raw data is available and distribution matters
- [ ] The response includes complete runnable code
- [ ] The response includes an audit summary with `Code checks`, `Rendered checks`, and `Session consistency`

## 2. Rendered Checks

These may only be marked `passed` after the chart has actually been rendered or visually inspected.

- [ ] No label-to-label collisions
- [ ] No label-to-data collisions
- [ ] Displaced labels remain clearly associated with the correct series or point
- [ ] Reference lines are visible at the actual output resolution
- [ ] Gridlines do not interfere with markers or labels
- [ ] Individual points are readable up close
- [ ] Overall pattern is readable at a glance
- [ ] Aspect ratio does not exaggerate or flatten the trend
- [ ] Small-panel line widths and font sizes remain readable
- [ ] Per-panel annotations are appropriately omitted or reduced in dense multi-panel layouts
- [ ] Sparklines are truly word-sized when used inline

## 3. Session Consistency Checks

Run these when generating 2+ related charts in one response or session.

- [ ] Same color-to-meaning assignments across charts
- [ ] Same font family, base size, title size, and label size
- [ ] Same axis treatment and range-frame policy
- [ ] Same or intentionally compatible figure dimensions
- [ ] Same line widths, marker sizes, and bar widths unless a deliberate exception is called out
- [ ] Shared categories keep the same ordering across charts

## Audit Output

Default to a compact audit block in the final response:

- `Code checks: passed` or `Code checks: fixed issues before finalizing`
- `Rendered checks: passed after rendering` or `Rendered checks: not visually verified`
- `Session consistency: n/a`, `passed`, or `not checked`

Expand the full checklist only when the user asks for it or when specific failures need explanation.
