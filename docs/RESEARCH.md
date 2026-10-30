# Numerical scope and verification protocol

## Structural model

One bay, 2–8 stories; elastic Euler–Bernoulli columns/beams and pin-ended axial braces. X diagonals cross without a joint. Chevron braces meet the beam midpoint. Both column bases fix UX/UY/RZ. All floor nodes share horizontal translation; upper vertical and rotational DOFs remain independent before static condensation. The unused middle base joint has no connected member.

Floor masses are prescribed total lateral masses. The massless DOFs satisfy static equilibrium. The production solver retains every finite floor mode. Brace area is adjusted between X and chevron layouts to give equal brace steel volume, while frame geometry, sections and total floor mass remain identical.

## Dynamics and reported quantities

`M u_ddot + C u_dot + K u = -M r a_g` uses Newmark beta=1/4, gamma=1/2. Original record endpoints are retained and input is linearly interpolated onto the integration grid. A nonzero first acceleration is retained through consistent initial relative acceleration. Rayleigh damping targets modes 1 and 2 separately; higher-mode damping can differ.

Drift is the difference between adjacent floor translations divided by story height. Roof displacement is relative to ground. Absolute acceleration adds ground acceleration. Base-shear demand is `1ᵀ(Ku + Cv) = -1ᵀM(a_relative + r a_g)`; support-on-frame reaction has opposite sign. Peaks use every integration sample, while browser histories are sampled for display. No free-vibration tail is appended beyond the supplied record.

## Record handling

The AT2 parser checks NPTS, DT, declared unit consistency, finite acceleration and bounded duration/sample count. Amplitude scaling is explicit. Filtering, baseline correction, detrending and spectrum matching are not performed. Imported data stays in request memory; user measurements are not committed or saved by the service. The bundled El Centro Peknold version has provenance in `web/records/README.md`.

## Verification layers

1. Analytical cantilever bending/axial deformation and stiffness symmetry.
2. Condensation energy, massless equilibrium, fixed bases and modal mass normalization.
3. Independent state-space ODE comparison and second-order time-step convergence.
4. OpenSees: independently assembled beam-column/bracing connectivity, constraints, modal properties, Rayleigh damping and full time histories.
5. Report-integrity checks: missing/corrupt/stale reports and deliberate 1% disagreements cannot pass.
6. HTTP checks: complete analysis, JSON/body guards, static-file boundaries and unavailable endpoints.

The independent benchmark covers the bundled four-story El Centro case and two synthetic QA signals with 2/8 stories, changed sections/geometry/mass, nonzero initial acceleration, 0/10% damping and changed amplitudes. Nine system/case combinations are compared. Three default-record dt/dt2/dt4 studies examine convergence. These synthetic signals are verification fixtures, not an earthquake suite. Matching time grids verify implementation consistency rather than different integration algorithms.

## Reproduction and limits

Run `python -m seismic_frame verify --opensees-python PATH_TO_REFERENCE_PYTHON`. The independent interpreter is isolated; only physical parameters and acceleration samples are passed, never production matrices or eigenvectors. `requirements-verification.txt` records the reference environment. Generated NPZ/CSV histories remain local. Freshness is determined from numerical-source and record hashes; rerun after moving/changing code.

The current family excludes inelasticity, brace buckling, P-delta, soil interaction, local connection behavior, 3D response, hazard scaling and design-code/capacity assessment. Verification does not establish real-structure accuracy.
