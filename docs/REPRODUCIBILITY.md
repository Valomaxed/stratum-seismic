# Reproducibility and review levels

## Read

[Results](RESULTS.md) and [independent report](../data/seismic-validation/report.md) need no installation. Repository access must first be arranged with the author.

## Recompute the example

After installing requirements.txt, from the repository root:

```bash
python examples/quick_review.py --output work/review-example.json
```

Compare with [recorded output](../data/review-example.json), allowing floating-point differences. This runs the production solver, not the independent reference.

## Automatic checks

```bash
python -m unittest discover -s tests -v
node --check web/seismic.js
```

CI covers Python 3.12/3.13. OpenSees-dependent tests skip if its separate interpreter is absent; analytical, ODE, HTTP and report-integrity checks still run.

## Independent benchmark

Create a separate Python 3.12 environment and install requirements-verification.txt, following the README. Then run:

```bash
python -m seismic_frame verify --opensees-python PATH_TO_REFERENCE_PYTHON
```

This repeats nine case/system comparisons and three refinement studies and regenerates reports, figures and local NPZ/CSV histories. The worker receives physical parameters and acceleration samples, never production matrices/eigenvectors. Source hashes guard freshness; do not reuse a saved PASS after numerical changes.

## Redraw the overview

```bash
python -m pip install -r requirements-figures.txt
python examples/plot_results.py
```

This redraws saved metrics, separately from numerical verification. Cite the repository commit with results; [CITATION.cff](../CITATION.cff) provides attribution.
