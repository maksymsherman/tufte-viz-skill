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

## Reference Example Rendering

To render-check the runnable Python reference examples from the markdown docs:

```bash
uv run --with matplotlib --with numpy --with seaborn --with plotly --with kaleido --with pandas --with altair --with vl-convert-python python eval/verify_reference_examples.py
```

This verifier:

- extracts the runnable Python definitions directly from the reference markdown files
- renders matplotlib, seaborn, Plotly, and Altair examples
- writes PNG artifacts to a temporary directory by default
- can target a specific output directory with `--output-dir`

On slim Linux environments, Plotly static export may require common Chrome runtime libraries in addition to `kaleido`. On current Ubuntu releases, this package set is sufficient:

```bash
sudo apt-get install -y libnss3 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2t64
```

## Limits

This harness does not render charts. It checks whether the response follows the house contract. Use local ChartBench runs when you need visual QA.
