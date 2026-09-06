# Demo session

```bash
source .venv/bin/activate
python -m genfin demo
python -m genfin run
python -m genfin report
head -n 40 reports/RESULTS.md
```

Expected: demo prints E01 texts for four variants with Layer A scores; `run` writes JSON under `artifacts/`; `report` refreshes `reports/RESULTS.md` from those files only.
