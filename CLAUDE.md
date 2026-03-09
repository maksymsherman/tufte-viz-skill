# clean-viz-skill

A Claude Code skill that applies Edward Tufte's data visualization principles to every chart generated. See `skills/clean-viz/SKILL.md` for the full skill specification.

## Project Structure

```
skills/clean-viz/
  SKILL.md              # Main skill definition (triggers, rules, banned types)
  references/
    checklist.md        # Mandatory quality gate (run every time; summarize in final response)
    matplotlib-patterns.md
    plotly-patterns.md
    general-patterns.md
eval/
  check_response.py     # Tracked smoke-test harness for saved model responses
  verify_reference_examples.py  # Render-check the runnable Python reference examples
  cases/                # Canonical prompt expectations (regex-based)
benchmark/
  chartbench-data/      # .gitignored — 9.7GB dataset, download locally
    test.jsonl           # 10,500 QA pairs across 42 chart subtypes
    data/test/test/      # 2,100 chart images with source data
```

## Tracked Eval Harness

The published repo now includes a small tracked response-check harness in `eval/`.

### What it covers

- banned-type substitution behavior
- presence of the compact audit summary
- units and direct-label intent for standard charts
- multi-series differentiation cues

### How to use it

Save model responses as markdown files, then run:

```bash
python3 eval/check_response.py --case matplotlib-line /path/to/response.md
python3 eval/check_response.py --responses-dir /path/to/saved-responses
```

The harness is intentionally lightweight and regex-based. It is a policy smoke test, not a rendering benchmark.

## Reference Example Verification

The tracked repo now also includes a render verifier for the runnable Python reference examples in `skills/clean-viz/references/`.

Run it with:

```bash
uv run --with matplotlib --with numpy --with seaborn --with plotly --with kaleido --with pandas --with altair --with vl-convert-python python eval/verify_reference_examples.py
```

It extracts the Python definitions directly from the markdown reference files, renders them, and writes artifacts to a temporary directory unless `--output-dir` is provided.

## ChartBench Testing

The `benchmark/` directory contains the ChartBench dataset for systematically testing the clean-viz skill against all 42 chart subtypes. The data is local-only and `.gitignored` due to size; it is not part of the published plugin repo.

### Setup (one-time)

```bash
pip install huggingface_hub
python3 -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='SincereX/ChartBench', repo_type='dataset',
                  local_dir='benchmark/chartbench-data')
"
cd benchmark/chartbench-data/data && unzip -q test.zip -d test
```

### How to test the skill manually

Each chart lives at `benchmark/chartbench-data/data/test/test/{category}/{subtype}/chart_{N}/` and contains:
- `table.json` — source data (title, x_data, y_data, labels, legend)
- `meta.json` — chart type and image subtype
- `image.png` — the reference chart image

**Testing flow for each subtype:**
1. Read `table.json` to get the data
2. Ask Claude to visualize that data as the chart type specified in `meta.json`
3. Verify the skill triggers and produces an audit summary with `Code checks` and `Rendered checks`
4. Verify the output follows clean-viz rules (banned types get substituted, no chartjunk, etc.)
5. For banned types (pie, 3D, radar, dual-axis), verify the skill explains the issue and offers a substitute

### All 42 Chart Subtypes

| # | Category | Subtype | Expected Skill Behavior |
|---|----------|---------|------------------------|
| 1 | area | `area` | Standard — apply clean-viz rules |
| 2 | area | `area_percent` | Standard — apply clean-viz rules |
| 3 | area | `area_stack` | Warn if >3 series (banned); suggest small multiples |
| 4 | bar | `horizontal_multi` | Standard |
| 5 | bar | `horizontal_percent_stacked` | Standard |
| 6 | bar | `horizontal_single` | Standard |
| 7 | bar | `horizontal_single_wi_anno` | Standard — verify annotations use data coordinates |
| 8 | bar | `horizontal_stacked` | Standard |
| 9 | bar | `threeD_bar_multi` | BANNED — must substitute with 2D bar chart |
| 10 | bar | `threeD_percent_stacked` | BANNED — must substitute with 2D bar chart |
| 11 | bar | `threeD_stacked` | BANNED — must substitute with 2D bar chart |
| 12 | bar | `vertical_multi` | Standard |
| 13 | bar | `vertical_percent_stacked` | Standard |
| 14 | bar | `vertical_single` | Standard |
| 15 | bar | `vertical_single_wi_anno` | Standard — verify annotations use data coordinates |
| 16 | bar | `vertical_stacked` | Standard |
| 17 | box | `box_h` | Standard |
| 18 | box | `box_v` | Standard |
| 19 | box | `stock` | Standard (candlestick) |
| 20 | combination | `bar_line` | BANNED (dual-axis) — must substitute with small multiples |
| 21 | combination | `line_line` | BANNED (dual-axis) — must substitute with small multiples |
| 22 | combination | `pie_bar` | BANNED (pie component) — substitute both |
| 23 | combination | `pie_pie` | BANNED (pie) — substitute with horizontal bar charts |
| 24 | line | `line_err` | Standard — error bars/bands are valid data-ink |
| 25 | line | `line_multi` | Standard — verify line style variation + direct labels |
| 26 | line | `line_multi_wi_anno` | Standard — verify annotations in data space |
| 27 | line | `line_single` | Standard — verify dot emphasis + direct labels |
| 28 | line | `line_single_wi_anno` | Standard |
| 29 | node_link | `node_link_dir` | Not a statistical chart — skill may not apply fully |
| 30 | node_link | `node_link_undir` | Not a statistical chart — skill may not apply fully |
| 31 | pie | `InteSun` | BANNED (sunburst/nested pie) — substitute with bar chart or treemap |
| 32 | pie | `pie` | BANNED — substitute with horizontal bar or dot plot |
| 33 | pie | `ring` | BANNED (donut) — substitute with horizontal bar or dot plot |
| 34 | pie | `ring_wi_anno` | BANNED (donut) — substitute with horizontal bar or dot plot |
| 35 | pie | `sector` | BANNED (pie variant) — substitute with horizontal bar or dot plot |
| 36 | radar | `radar_multi` | BANNED — substitute with small multiples of bar/dot plots |
| 37 | radar | `radar_multi_fill` | BANNED — substitute with small multiples of bar/dot plots |
| 38 | radar | `radar_single` | BANNED — substitute with bar or dot plot |
| 39 | radar | `radar_single_wi_anno` | BANNED — substitute with bar or dot plot |
| 40 | scatter | `scatter_2d` | Standard |
| 41 | scatter | `scatter_2d_smooth` | Standard — trend line is valid data-ink |
| 42 | scatter | `scatter_3d` | BANNED — substitute with 2D scatter + size/color encoding |

### Key edge cases to watch for

- **Banned types (17 of 42):** pie (5), radar (4), 3D (4), combination/dual-axis (4) — skill must refuse and substitute
- **Annotation handling:** `_wi_anno` subtypes test whether annotations use data coordinates
- **Multi-series:** `_multi` subtypes test line style variation and label collision avoidance
- **Stacked area >3 series:** should trigger the small multiples substitute
- **Node/link charts:** outside the skill's core scope — acceptable to apply only typography/color rules
