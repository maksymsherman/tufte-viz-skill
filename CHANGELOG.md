# Changelog

## 1.1.0 (2026-03-08)

### Changed
- Reworked the checklist into a three-part quality gate: code checks, rendered checks, and session consistency checks
- Replaced the mandatory full checklist table with a compact audit summary and an honesty rule for visual verification
- Narrowed skill triggers to visualization-specific requests and added an activation guard
- Repositioned documentation to reflect primary vs. secondary library support

### Added
- Tracked `eval/` smoke-test harness for saved responses
- Verification-model documentation in `README.md`

## 1.0.0 (2026-02-09)

### Added
- Core SKILL.md with Tufte visualization principles and mandatory rules
- Matplotlib/seaborn reference patterns (range frames, direct labeling, sparklines, slope charts)
- Plotly reference patterns (layout templates, annotations, small multiples)
- General reference patterns (Altair, D3.js, ggplot2, Observable Plot)
- Post-generation verification checklist
- Chart type substitution table (pie -> bar, 3D -> 2D, dual-axis -> small multiples)
- Plugin manifest for Claude Code marketplace distribution
