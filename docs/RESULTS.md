# Results and interpretation

 ## Controlled elastic example

 Four stories; 3.2 m story height; 6 m bay; 40 t prescribed mass/floor; 5% damping at each system's first two modes; identical frame sections. X and chevron layouts use equal brace steel volume, 0.1088 m³.

 The bundled El Centro 1940 NS Peknold example has 1,559 samples, DT=0.02 s, duration 31.16 s, PGA 0.31882 g and amplitude factor 1.0. [Provenance](../web/records/README.md).

 | System | First period (s) | Peak drift (%) | Peak roof displacement (mm) | Peak base-shear demand (kN) |
 |---|---:|---:|---:|---:|
 | Unbraced | 1.475 | 1.373 | 127.25 | 291.7 |
| X-braced | 0.409 | 0.379 | 42.21 | 993.0 |
| Chevron | 0.339 | 0.270 | 29.24 | 1145.0 |

 ![Controlled frame comparison](../data/seismic-validation/review-summary.png)

 [quick_review.py](../examples/quick_review.py) recomputes these values. [Recorded output](../data/review-example.json). [plot_results.py](../examples/plot_results.py) redraws the overview from the saved verification report.

 ## Interpretation

 Under this record and elastic model, braced systems have shorter first periods and smaller drift, while peak base-shear demand increases. Displacement and force demands therefore need to be interpreted together. This example does not establish a universal ranking: excitation, stiffness distribution, damping and represented physical mechanisms all matter.

 Roof displacement is relative to ground. Shear is generalized demand including stiffness/damping; ground-on-frame reaction uses the opposite sign. Peaks use all integration samples. Browser histories are downsampled. No free-vibration tail is appended after the record.

 ## Independent verification

 [The report](../data/seismic-validation/report.md) passes **9/9 case/system comparisons** and **3/3 time-step studies**. It includes the default record and two synthetic QA motions with 2/8 stories, changed geometry/sections/mass, nonzero initial acceleration and 0/10% damping. Those motions are test fixtures, not a hazard-selected suite.

 [Fixed acceptance limits](../seismic_frame/benchmark.py): relative frequency error at most 1e-7; normalized maximum history/relative peak errors at most 1e-6; force-balance error at most 1e-7; and the documented peak-refinement bounds. Floor-history refinement ratios are approximately four. Same-grid OpenSees agreement and step refinement address different verification questions.

 [Machine report](../data/seismic-validation/report.json) records source hashes, engine/runtime versions, limits and errors. Changes to numerical sources or the record invalidate the fresh PASS. [Reproduction instructions](REPRODUCIBILITY.md).

 ## Scope

 This is a linear elastic in-plane frame with prescribed floor masses and condensed massless vertical/rotation DOFs. Yielding, brace buckling, P-delta, soil interaction, physical experiments, hazard scaling and capacity/code assessment need separate work. Independent agreement does not remove those model limitations.
