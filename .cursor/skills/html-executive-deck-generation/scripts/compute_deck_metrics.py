#!/usr/bin/env python3
"""Compute deck metrics and chart PNGs from CSV/XLSX. Do not invent numbers."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PULSE_MANAGER_ALIASES = {"manager", "people leader", "people_leader"}
ID_HINTS = ("id", "empid", "emp_id", "employee", "uuid")
NAVY = "#1F3864"
TEAL = "#2A6F7F"
GOLD = "#C4A35A"
BONE = "#F4EFE6"


def is_pulse_frame(df: pd.DataFrame) -> bool:
    cols = {str(c).strip().lower() for c in df.columns}
    has_manager = bool(cols & PULSE_MANAGER_ALIASES)
    qcols = [c for c in df.columns if str(c).upper().startswith("Q") and "_" in str(c)]
    return has_manager and len(qcols) >= 10


def load_table(path: Path) -> tuple[pd.DataFrame, str | None]:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        sep = "\t" if suffix == ".tsv" else ","
        return pd.read_csv(path, encoding="utf-8-sig", sep=sep).dropna(how="all"), None
    if suffix in {".xlsx", ".xlsm", ".xls"}:
        book = pd.ExcelFile(path)
        sheet = book.sheet_names[0]
        return pd.read_excel(book, sheet_name=sheet).dropna(how="all"), sheet
    raise SystemExit(f"Unsupported file type: {path.suffix}")


def _is_id_like(name: str) -> bool:
    lowered = name.strip().lower().replace(" ", "")
    return any(hint in lowered for hint in ID_HINTS)


def classify_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric: list[str] = []
    categorical: list[str] = []
    for col in df.columns:
        series = df[col]
        if _is_id_like(str(col)):
            continue
        numeric_series = pd.to_numeric(series, errors="coerce")
        numeric_ratio = numeric_series.notna().mean()
        if numeric_ratio >= 0.8 and numeric_series.nunique(dropna=True) > 1:
            numeric.append(str(col))
            continue
        nunique = series.nunique(dropna=True)
        if 1 < nunique <= 30:
            categorical.append(str(col))
    return numeric, categorical


def _round(value: float) -> float:
    return round(float(value), 4)


def numeric_summary(df: pd.DataFrame, numeric_cols: list[str]) -> dict[str, dict[str, float | int]]:
    out: dict[str, dict[str, float | int]] = {}
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if series.empty:
            continue
        out[col] = {
            "count": int(series.count()),
            "mean": _round(series.mean()),
            "median": _round(series.median()),
            "min": _round(series.min()),
            "max": _round(series.max()),
            "sum": _round(series.sum()),
            "std": _round(series.std(ddof=0)) if len(series) > 1 else 0.0,
        }
    return out


def group_rows(
    df: pd.DataFrame, categorical: list[str], numeric_cols: list[str], limit: int = 12
) -> list[dict]:
    blocks: list[dict] = []
    for by in categorical[:2]:
        for metric in numeric_cols[:6]:
            grouped = (
                pd.to_numeric(df[metric], errors="coerce")
                .groupby(df[by].astype(str), dropna=True)
                .mean()
                .dropna()
                .sort_values(ascending=False)
                .head(limit)
            )
            if grouped.empty:
                continue
            blocks.append(
                {
                    "by": by,
                    "metric": metric,
                    "agg": "mean",
                    "rows": [
                        {"label": str(idx), "value": _round(val)}
                        for idx, val in grouped.items()
                    ],
                }
            )
    return blocks


def write_charts(groupbys: list[dict], out_dir: Path) -> list[dict]:
    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    charts: list[dict] = []
    for idx, block in enumerate(groupbys[:8], start=1):
        labels = [row["label"] for row in block["rows"]]
        values = [row["value"] for row in block["rows"]]
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=BONE)
        ax.set_facecolor(BONE)
        bars = ax.barh(labels[::-1], values[::-1], color=TEAL)
        if bars:
            bars[-1].set_color(GOLD)
        ax.set_title(f"{block['metric']} by {block['by']} (mean)", color=NAVY, loc="left")
        ax.tick_params(colors=NAVY)
        for spine in ax.spines.values():
            spine.set_color(NAVY)
        fig.tight_layout()
        png = charts_dir / f"CH-{idx:02d}.png"
        fig.savefig(png, dpi=160, bbox_inches="tight", facecolor=BONE)
        plt.close(fig)
        charts.append(
            {
                "id": f"CH-{idx:02d}",
                "type": "bar",
                "title": f"{block['metric']} by {block['by']}",
                "png": str(png),
                "rows": block["rows"],
            }
        )
    return charts


def kpis(df: pd.DataFrame, summary: dict[str, dict[str, float | int]]) -> list[dict]:
    items = [
        {"label": "Rows", "value": int(len(df)), "display": str(len(df)), "formula": "COUNT(*)"},
    ]
    for col, stats in list(summary.items())[:3]:
        items.append(
            {
                "label": f"{col} mean",
                "value": stats["mean"],
                "display": f"{stats['mean']:.2f}",
                "formula": f"MEAN({col})",
            }
        )
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description="Python-computed metrics + charts for executive decks.")
    parser.add_argument("input", type=Path, help="CSV or XLSX path")
    parser.add_argument("--out-dir", type=Path, default=None, help="Output directory (default: beside input)")
    parser.add_argument("--force-generic", action="store_true", help="Ignore pulse-survey detection")
    args = parser.parse_args()

    source = args.input.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"File not found: {source}")
    out_dir = (args.out_dir.expanduser().resolve() if args.out_dir else source.parent / f"{source.stem}_python_metrics")
    out_dir.mkdir(parents=True, exist_ok=True)

    mpl_dir = out_dir / ".mplconfig"
    mpl_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(mpl_dir))

    df, sheet = load_table(source)
    if df.empty:
        raise SystemExit("No data rows found.")

    if is_pulse_frame(df) and not args.force_generic:
        hint = {
            "mode": "pulse_detected",
            "source": str(source),
            "sheet": sheet,
            "row_count": int(len(df)),
            "message": "Use pulse-survey-analysis/scripts/pulse_report_runner.py --json-out for this file.",
        }
        hint_path = out_dir / "metrics.json"
        hint_path.write_text(json.dumps(hint, indent=2) + "\n", encoding="utf-8")
        print(hint_path)
        print("PULSE_SURVEY_DETECTED", file=sys.stderr)
        raise SystemExit(2)

    numeric_cols, categorical = classify_columns(df)
    summary = numeric_summary(df, numeric_cols)
    blocks = group_rows(df, categorical, numeric_cols)
    if not blocks and numeric_cols:
        means = [
            {"label": col, "value": summary[col]["mean"]}
            for col in numeric_cols
            if col in summary
        ]
        blocks = [{"by": "metric", "metric": "mean", "agg": "mean", "rows": means}]
    charts = write_charts(blocks, out_dir)
    payload = {
        "mode": "generic",
        "source": str(source),
        "sheet": sheet,
        "row_count": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical,
        "kpiValues": kpis(df, summary),
        "numeric_summary": summary,
        "groupbys": blocks,
        "charts": charts,
    }
    metrics_path = out_dir / "metrics.json"
    metrics_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(metrics_path)
    for chart in charts:
        print(chart["png"])


if __name__ == "__main__":
    main()
