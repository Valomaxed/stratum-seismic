# Architecture

`seismic_frame/server.py` serves the local frontend and accepts bounded JSON requests. `model.py` validates frame/record settings, assembles beam-column and axial-brace stiffness, condenses massless secondary DOFs, computes modes, and recovers engineering response quantities. `dynamics.py` integrates the linear system with Newmark average acceleration.

`web/seismic.js` renders frame playback, drift profiles, ground motion, relative roof displacement and base shear. JSON/CSV exports include provenance and settings. Display histories are downsampled; numerical peak extraction uses every integration step.

`benchmark.py` starts the independent `reference.py` in a separately configured OpenSees interpreter. That worker builds its own connectivity, elements, constraints and damping from physical parameters. It receives no production stiffness matrix or eigenvectors. Saved reports are invalidated when numerical-source or record hashes change.

The model is linear elastic. Floor translation is constrained horizontally, masses are prescribed by floor, and vertical/rotational DOFs are massless. Fixed column bases, pin-ended axial braces and in-plane behavior are assumptions. Yielding, brace buckling, P-delta, soil interaction and design capacity are outside scope.
