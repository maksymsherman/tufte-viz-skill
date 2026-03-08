# Eval Harness

This directory contains a small tracked smoke-test harness for saved model responses.

It is intentionally lightweight:

- regex-based, not semantic
- designed for policy regressions, not chart quality benchmarking
- useful in CI or local spot checks when ChartBench is unavailable

## What it checks

- banned-type substitution for canonical prompts
- presence of the compact audit summary
- units and direct-label intent for standard charts
- multi-series differentiation cues

## Usage

Run a single case:

```bash
python3 eval/check_response.py --case matplotlib-line /path/to/response.md
```

Run the whole suite against a directory of saved responses:

```bash
python3 eval/check_response.py --responses-dir /path/to/responses
```

Batch mode expects filenames that match the case names:

- `matplotlib-line.md`
- `pie-substitution.md`
- `plotly-multi-line.md`

## Limits

This harness does not render charts. It checks whether the response follows the house contract. Use local ChartBench runs when you need visual QA.
