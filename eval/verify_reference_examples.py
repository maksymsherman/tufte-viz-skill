#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import os
import re
import tempfile
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
MATPLOTLIB_PATTERNS = ROOT / "skills/clean-viz/references/matplotlib-patterns.md"
PLOTLY_PATTERNS = ROOT / "skills/clean-viz/references/plotly-patterns.md"
GENERAL_PATTERNS = ROOT / "skills/clean-viz/references/general-patterns.md"

ALLOWED_SETUP_CALLS = (
    "plt.rcParams.update",
    "alt.themes.register",
    "alt.themes.enable",
)


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    artifact: Path | None = None


def expr_name(expr: ast.AST) -> str:
    if isinstance(expr, ast.Attribute):
        base = expr_name(expr.value)
        return f"{base}.{expr.attr}" if base else expr.attr
    if isinstance(expr, ast.Call):
        return expr_name(expr.func)
    if isinstance(expr, ast.Name):
        return expr.id
    return ""


def load_python_reference_module(path: Path) -> ast.Module:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)```", text, re.S)
    module = ast.Module(body=[], type_ignores=[])

    for code in blocks:
        tree = ast.parse(code, filename=str(path))
        for node in tree.body:
            if isinstance(
                node,
                (
                    ast.Import,
                    ast.ImportFrom,
                    ast.Assign,
                    ast.AnnAssign,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                module.body.append(node)
                continue

            if isinstance(node, ast.Expr):
                call_name = expr_name(node.value)
                if any(call_name.startswith(prefix) for prefix in ALLOWED_SETUP_CALLS):
                    module.body.append(node)

    ast.fix_missing_locations(module)
    return module


def load_namespace(markdown_path: Path, preamble: str = "") -> dict:
    module = load_python_reference_module(markdown_path)
    if preamble:
        preamble_module = ast.parse(preamble, filename="<preamble>")
        module = ast.Module(body=preamble_module.body + module.body, type_ignores=[])
        ast.fix_missing_locations(module)

    namespace: dict = {}
    exec(compile(module, str(markdown_path), "exec"), namespace)
    return namespace


def resolve_output_dir(output_dir: Path | None) -> Path:
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    return Path(tempfile.mkdtemp(prefix="clean-viz-reference-verify-"))


def ensure_plotly_browser() -> None:
    if os.environ.get("BROWSER_PATH"):
        return

    import plotly.io as pio

    chrome_path = pio.get_chrome()
    os.environ["BROWSER_PATH"] = str(chrome_path)


def save_matplotlib_figure(fig, output_path: Path) -> Path:
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    fig.clf()
    return output_path


def save_plotly_figure(fig, output_path: Path) -> Path:
    ensure_plotly_browser()
    fig.write_image(str(output_path), width=900, height=500)
    return output_path


def run_check(name: str, fn: Callable[[], Path | None]) -> CheckResult:
    try:
        artifact = fn()
        return CheckResult(name=name, ok=True, detail="ok", artifact=artifact)
    except Exception as exc:
        detail = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        return CheckResult(name=name, ok=False, detail=detail)


def build_matplotlib_checks(namespace: dict, output_dir: Path) -> list[tuple[str, Callable[[], Path | None]]]:
    plt = namespace["plt"]
    x = [2019, 2020, 2021, 2022, 2023]
    y = [12, 18, 16, 22, 27]

    def clean_line_plot() -> Path:
        fig, ax = plt.subplots(figsize=(6, 4))
        namespace["clean_line_plot"](ax, x, y, label="Revenue")
        assert len(ax.texts) == 1, "expected one direct label"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-line.png")

    def clean_multi_line_plot() -> Path:
        fig, ax = plt.subplots(figsize=(6, 4))
        series = {
            "North": [12, 18, 16, 22, 27],
            "South": [10, 11, 15, 17, 20],
            "West": [9, 13, 14, 19, 19.5],
        }
        namespace["clean_multi_line_plot"](ax, x, series)
        assert len(ax.texts) >= len(series), "expected direct labels for each series"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-multi-line.png")

    def clean_bar_chart() -> Path:
        fig, ax = plt.subplots(figsize=(6, 4))
        namespace["clean_bar_chart"](ax, ["A", "B", "C"], [14, 9, 17])
        assert all(not spine.get_visible() for spine in ax.spines.values()), "bar chart should hide spines"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-bar.png")

    def clean_horizontal_bar_chart() -> Path:
        fig, ax = plt.subplots(figsize=(6, 4))
        namespace["clean_horizontal_bar_chart"](ax, ["Alpha", "Beta", "Gamma"], [43, 65, 52])
        assert all(not spine.get_visible() for spine in ax.spines.values()), "horizontal bars should hide spines"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-horizontal-bar.png")

    def clean_dot_plot() -> Path:
        fig, ax = plt.subplots(figsize=(6, 4))
        namespace["clean_dot_plot"](ax, ["Alpha", "Beta", "Gamma"], [43, 65, 52])
        assert not ax.spines["left"].get_visible(), "dot plot should hide left spine"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-dot-plot.png")

    def clean_slope_chart() -> Path:
        fig, ax = plt.subplots(figsize=(6, 4))
        namespace["clean_slope_chart"](
            ax,
            ["A", "B", "C"],
            [10, 15, 22],
            [12, 18, 20],
            highlight="B",
        )
        assert not ax.axison, "slope chart should hide axes"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-slope-chart.png")

    def clean_sparkline() -> Path:
        fig, ax = plt.subplots(figsize=(3, 0.6))
        namespace["clean_sparkline"](ax, [4, 6, 5, 7, 9, 8, 10])
        assert not ax.axison, "sparkline should hide axes"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-sparkline.png")

    def sparkline_grid() -> Path:
        fig = namespace["sparkline_grid"](
            {"North": [4, 6, 5, 7, 9], "South": [3, 3.5, 4, 4.5, 5]}
        )
        return save_matplotlib_figure(fig, output_dir / "matplotlib-sparkline-grid.png")

    def clean_small_multiples() -> Path:
        fig, axes = namespace["clean_small_multiples"](
            {
                "North": (x, [12, 18, 16, 22, 27]),
                "South": (x, [10, 11, 15, 17, 20]),
                "West": (x, [9, 13, 14, 19, 19.5]),
                "East": (x, [8, 10, 13, 15, 18]),
            },
            ncols=2,
        )
        assert len(axes.flatten()) == 4, "expected 2x2 small-multiples grid"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-small-multiples.png")

    def clean_seaborn() -> Path:
        fig, ax = plt.subplots(figsize=(6, 4))
        namespace["apply_clean_seaborn"]()
        namespace["sns"].lineplot(x=x, y=y, ax=ax)
        namespace["clean_seaborn"](ax, x, y)
        assert ax.get_legend() is None, "seaborn cleanup should remove legend"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-seaborn.png")

    def clean_scatter() -> Path:
        fig, ax = plt.subplots(figsize=(5, 4))
        namespace["clean_scatter"](ax, [1, 2, 3, 4], [4, 1, 3, 5], label_points={3: "Outlier"})
        assert len(ax.texts) >= 1, "scatter should include requested annotation"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-scatter.png")

    def clean_histogram() -> Path:
        fig, ax = plt.subplots(figsize=(5, 4))
        namespace["clean_histogram"](ax, [1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6])
        assert all(not spine.get_visible() for spine in ax.spines.values()), "histogram should hide spines"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-histogram.png")

    def clean_heatmap() -> Path:
        fig, ax = plt.subplots(figsize=(5, 3))
        namespace["clean_heatmap"](
            ax,
            [[1.0, 2.0, 3.5], [4.1, 5.4, 6.2]],
            ["Row 1", "Row 2"],
            ["A", "B", "C"],
        )
        assert len(ax.texts) == 6, "heatmap should label each cell"
        return save_matplotlib_figure(fig, output_dir / "matplotlib-heatmap.png")

    return [
        ("matplotlib.clean_line_plot", clean_line_plot),
        ("matplotlib.clean_multi_line_plot", clean_multi_line_plot),
        ("matplotlib.clean_bar_chart", clean_bar_chart),
        ("matplotlib.clean_horizontal_bar_chart", clean_horizontal_bar_chart),
        ("matplotlib.clean_dot_plot", clean_dot_plot),
        ("matplotlib.clean_slope_chart", clean_slope_chart),
        ("matplotlib.clean_sparkline", clean_sparkline),
        ("matplotlib.sparkline_grid", sparkline_grid),
        ("matplotlib.clean_small_multiples", clean_small_multiples),
        ("matplotlib.clean_seaborn", clean_seaborn),
        ("matplotlib.clean_scatter", clean_scatter),
        ("matplotlib.clean_histogram", clean_histogram),
        ("matplotlib.clean_heatmap", clean_heatmap),
    ]


def build_plotly_checks(namespace: dict, output_dir: Path) -> list[tuple[str, Callable[[], Path | None]]]:
    x = [2019, 2020, 2021, 2022, 2023]
    y = [12, 18, 16, 22, 27]

    def clean_line_chart() -> Path:
        fig = namespace["clean_line_chart"](x, y, name="Revenue")
        assert fig.layout.showlegend is False
        assert len(fig.layout.annotations) >= 1, "expected direct label annotation"
        assert len(fig.layout.shapes) >= 2, "expected range-frame shapes"
        return save_plotly_figure(fig, output_dir / "plotly-line.png")

    def clean_bar_chart() -> Path:
        fig = namespace["clean_bar_chart"](["A", "B", "C"], [14, 9, 17])
        assert fig.layout.showlegend is False
        assert fig.layout.yaxis.showgrid, "expected white reference gridlines"
        return save_plotly_figure(fig, output_dir / "plotly-bar.png")

    def clean_scatter() -> Path:
        fig = namespace["clean_scatter"]([1, 2, 3, 4], [4, 1, 3, 5], labels=[(4, 5, "Outlier")])
        assert len(fig.layout.annotations) >= 1, "expected scatter annotation"
        return save_plotly_figure(fig, output_dir / "plotly-scatter.png")

    def clean_small_multiples() -> Path:
        fig = namespace["clean_small_multiples"](
            {
                "North": (x, [12, 18, 16, 22, 27]),
                "South": (x, [10, 11, 15, 17, 20]),
                "West": (x, [9, 13, 14, 19, 19.5]),
                "East": (x, [8, 10, 13, 15, 18]),
            },
            ncols=2,
        )
        assert len(fig.layout.annotations) >= 4, "expected subplot titles"
        return save_plotly_figure(fig, output_dir / "plotly-small-multiples.png")

    def clean_sparkline() -> Path:
        fig = namespace["clean_sparkline"]([4, 6, 5, 7, 9, 8, 10])
        assert len(fig.data) == 2, "expected line trace plus highlight markers"
        return save_plotly_figure(fig, output_dir / "plotly-sparkline.png")

    def clean_heatmap() -> Path:
        fig = namespace["clean_heatmap"](
            [[1.0, 2.0, 3.5], [4.1, 5.4, 6.2]],
            ["A", "B", "C"],
            ["Row 1", "Row 2"],
        )
        assert len(fig.layout.annotations) == 6, "expected one label per heatmap cell"
        return save_plotly_figure(fig, output_dir / "plotly-heatmap.png")

    def clean_multi_line() -> Path:
        series = {
            "North": [12, 18, 16, 22, 27],
            "South": [10, 11, 15, 17, 20],
            "West": [9, 13, 14, 19, 19.5],
        }
        fig = namespace["clean_multi_line"](x, series)
        text_traces = [trace for trace in fig.data if getattr(trace, "mode", "") == "text"]
        assert len(text_traces) == len(series), "expected one label trace per series"
        return save_plotly_figure(fig, output_dir / "plotly-multi-line.png")

    return [
        ("plotly.clean_line_chart", clean_line_chart),
        ("plotly.clean_bar_chart", clean_bar_chart),
        ("plotly.clean_scatter", clean_scatter),
        ("plotly.clean_small_multiples", clean_small_multiples),
        ("plotly.clean_sparkline", clean_sparkline),
        ("plotly.clean_heatmap", clean_heatmap),
        ("plotly.clean_multi_line", clean_multi_line),
    ]


def build_altair_checks(namespace: dict, output_dir: Path) -> list[tuple[str, Callable[[], Path | None]]]:
    import pandas as pd

    x = [2019, 2020, 2021, 2022, 2023]

    line_df = pd.DataFrame(
        {
            "year": x * 2,
            "value": [12, 18, 16, 22, 27, 10, 11, 15, 17, 20],
            "series": ["North"] * len(x) + ["South"] * len(x),
        }
    )
    bar_df = pd.DataFrame({"category": ["A", "B", "C"], "value": [14, 9, 17]})
    facet_df = pd.DataFrame(
        {
            "year": x * 4,
            "value": [
                12,
                18,
                16,
                22,
                27,
                10,
                11,
                15,
                17,
                20,
                9,
                13,
                14,
                19,
                19.5,
                8,
                10,
                13,
                15,
                18,
            ],
            "category": ["North"] * len(x)
            + ["South"] * len(x)
            + ["West"] * len(x)
            + ["East"] * len(x),
        }
    )

    def clean_line_chart() -> Path:
        chart = namespace["clean_line_chart"](line_df, "year:Q", "value:Q", "series:N")
        spec = chart.to_dict()
        assert "layer" in spec, "expected layered line + label chart"
        output_path = output_dir / "altair-line.png"
        chart.save(str(output_path))
        return output_path

    def clean_bar_chart() -> Path:
        chart = namespace["clean_bar_chart"](bar_df, "category:N", "value:Q")
        spec = chart.to_dict()
        assert "layer" in spec, "expected layered bars + text"
        output_path = output_dir / "altair-bar.png"
        chart.save(str(output_path))
        return output_path

    def clean_facet() -> Path:
        chart = namespace["clean_facet"](facet_df, "year:Q", "value:Q", "category:N", columns=2)
        spec = chart.to_dict()
        assert "facet" in spec, "expected faceted chart"
        output_path = output_dir / "altair-facet.png"
        chart.save(str(output_path))
        return output_path

    return [
        ("altair.clean_line_chart", clean_line_chart),
        ("altair.clean_bar_chart", clean_bar_chart),
        ("altair.clean_facet", clean_facet),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render-verify the runnable clean-viz reference examples."
    )
    parser.add_argument(
        "--framework",
        action="append",
        choices=["matplotlib", "plotly", "altair"],
        help="Limit verification to one or more frameworks. Defaults to all.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory where rendered artifacts should be written. Defaults to a temp directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = resolve_output_dir(args.output_dir)
    frameworks = args.framework or ["matplotlib", "plotly", "altair"]

    checks: list[tuple[str, Callable[[], Path | None]]] = []

    if "matplotlib" in frameworks:
        matplotlib_ns = load_namespace(
            MATPLOTLIB_PATTERNS,
            preamble="import matplotlib\nmatplotlib.use('Agg')\n",
        )
        checks.extend(build_matplotlib_checks(matplotlib_ns, output_dir))

    if "plotly" in frameworks:
        plotly_ns = load_namespace(PLOTLY_PATTERNS)
        checks.extend(build_plotly_checks(plotly_ns, output_dir))

    if "altair" in frameworks:
        altair_ns = load_namespace(GENERAL_PATTERNS)
        checks.extend(build_altair_checks(altair_ns, output_dir))

    results = [run_check(name, fn) for name, fn in checks]

    for result in results:
        status = "PASS" if result.ok else "FAIL"
        artifact = f"  {result.artifact}" if result.artifact else ""
        print(f"{status}  {result.name}  {result.detail}{artifact}")

    passed = sum(result.ok for result in results)
    print(f"\nSummary: {passed}/{len(results)} passed")
    print(f"Artifacts: {output_dir}")

    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
