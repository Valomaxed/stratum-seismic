# Academic review guide

**Atharv Sharma · STRATUM Seismic**

## 1. Research question

How do unbraced, X-braced and chevron configurations change elastic drift and base-shear demand under controlled common excitation, and how can the implementation be independently verified?

Geometry, sections and prescribed floor masses are fixed. X and chevron layouts use equal brace steel volume. Read [the results](docs/RESULTS.md) before interpreting the configurations.

## 2. Source review route

| Topic | Entry point | What to inspect |
|---|---|---|
| Frame mechanics | [model.py](seismic_frame/model.py) | Beam-column/brace assembly, supports, floor constraints and condensation |
| Dynamics | [dynamics.py](seismic_frame/dynamics.py) | Newmark average acceleration and equilibrium residual |
| Response definitions | [model.py](seismic_frame/model.py) | Drift, relative/absolute acceleration and shear convention |
| Independent model | [reference.py](seismic_frame/reference.py) | OpenSees assembly and support/damping-force recovery |
| Verification protocol | [benchmark.py](seismic_frame/benchmark.py) | Fixed tolerances, source hashes, history comparison and refinement |
| Automated evidence | [tests](tests/) | Analytical, ODE, service and report-integrity checks |

NumPy/SciPy supply linear algebra. The repository implements assembly, reduction, record handling, response recovery and the comparison workflow. OpenSees supplies a separate reference implementation.

## 3. Run an example

After installing requirements.txt, run from the repository root:

```bash
python examples/quick_review.py
```

This recomputes the four-story comparison using the attributed El Centro example without a web server, ML model or OpenSees installation. Compare [recorded output](data/review-example.json). For the interface, run `python -m seismic_frame serve` and open http://127.0.0.1:8767/.

## 4. Verification and interpretation

[Independent report](data/seismic-validation/report.md): nine case/system comparisons and three time-step studies. [Reproduction instructions](docs/REPRODUCIBILITY.md) explain the isolated OpenSees environment and source-hash freshness checks.

Independent agreement supports implementation consistency. It does not validate physical frame behavior or establish a universal bracing-system ranking.

## 5. Further research

Broader motions, hazard-consistent scaling, nonlinear braces, P-delta, connection/foundation flexibility and physical validation require additional modeling and checks.

[Authorship](AUTHORS.md) · [Private access](docs/REVIEWER_ACCESS.md) · [Architecture](docs/ARCHITECTURE.md)
