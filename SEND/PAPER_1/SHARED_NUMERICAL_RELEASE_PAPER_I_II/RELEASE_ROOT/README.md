# RIUD Papers I-IV Numerical Release R1

This is a paper-oriented numerical companion package. It contains the manuscript text/Paper I-III canonical document, frozen numerical result tables, contracts, provenance records, and a small local verifier.

It is intentionally not a raw-to-final execution package: no detector raw data, PE files, long strain files, HDF5 residual bundle, image/figure bundle, Holdout30 data, or scientific runner is included. `verify_numbers.py` checks the frozen values and table consistency already released by the RIUD lineage; it does not refit, rerun, or discover anything.

Run from this directory:

    python verify_numbers.py

The verifier prints `NUMERICAL_CHECK=PASS` when the bundled frozen numeric records match the locked values. All source archive paths remain provenance only; the verifier uses package-relative files.
