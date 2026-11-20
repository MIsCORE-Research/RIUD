# Paper5 reproduction package scope

This is a frozen numerical replay/evidence package, not a raw-to-final recomputation archive.

Included:
- R40 final 101-event characterization outputs.
- SXS source-native node/path/topology outputs and contracts.
- All 17 completed raw path-support audit result folders.
- Existing-input inventory with selected source paths and SHA256.
- Updated claim/evidence matrix and final claim boundary.

Excluded:
- Missing raw source files for 81 PATH_FOUND events.
- The single DEV99 NO_PATH event from path scoring.
- Holdout30 data.
- New code-driven science calculation.

Reproduction semantics:
- R40 and SXS outputs are frozen replay results.
- Raw17 outputs are frozen diagnostic results using existing source files.
- The SXS branch is source-native and must not be described as exact LIGO residual replay.
