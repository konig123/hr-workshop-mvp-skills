# Python metrics (required for CSV / XLSX)

Structured files are **never** totaled, averaged, ranked, or percent-changed by the LLM. Run Python first. Cite only the JSON it writes.

## Setup (once per machine)

From this skill folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Pulse PDFs also need the sibling skill venv:

```bash
cd ../pulse-survey-analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Resolve skill roots with `Path(__file__)` / `pwd`. Do not type a straight `'` into `Desktop - km's MacBook Pro` paths.

## Route the file

Peek at columns (header row is enough):

| If the file has… | Run |
|------------------|-----|
| `Manager` or `People Leader` **and** ≥10 `Q*_…` columns | Pulse runner |
| Any other CSV / XLSX | Generic metrics script |

### Pulse survey

```bash
../pulse-survey-analysis/.venv/bin/python \
  ../pulse-survey-analysis/scripts/pulse_report_runner.py \
  "/absolute/path/to/survey.csv" \
  --team "Company" \
  --period "2026-05" \
  --out-dir "/absolute/path/to/out" \
  --json-out "/absolute/path/to/out/metrics.json" \
  --no-individual
```

Always produces: team PNG chart + `metrics.json` (`mode: "pulse"`). PDF is included unless `--no-pdf`.

If the pulse file is XLSX, convert with pandas first (`read_excel` → `to_csv`) then run the runner. Do not hand-add columns.

### Generic CSV / XLSX

```bash
.venv/bin/python scripts/compute_deck_metrics.py \
  "/absolute/path/to/data.xlsx" \
  --out-dir "/absolute/path/to/out"
```

Always produces: `metrics.json` (`mode: "generic"`) and `charts/CH-*.png`.

Exit code **2** + `PULSE_SURVEY_DETECTED` means stop and use the pulse runner instead.

## Hard rules

1. Insight Brief **Source** column = `metrics.json` path + field (e.g. `kpiValues[1].value`).
2. Step 2 chart JSON **copies** Python `kpiValues` / `charts[].rows`. Do not re-average in prose.
3. HTML / Gamma / Kimi must use the same JSON numbers.
4. If Python fails, fix the environment and rerun. Do **not** substitute LLM math for a file.
5. Free-text decks (no file) stay extract-only: stated numbers only, else `[TBD]`.
