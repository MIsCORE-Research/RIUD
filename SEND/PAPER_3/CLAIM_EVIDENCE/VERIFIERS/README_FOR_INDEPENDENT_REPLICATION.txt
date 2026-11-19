This package is self-contained and relocatable.

Runtime paths are derived from the location of the invoking script and must
remain inside the current package root. The package does not require a
particular drive letter. Run work/VERIFY_PACKAGE_ROOT_SELF_CONTAINMENT.sh (or
the Python equivalent) before running any branch.

The scientific branch is preserved as produced. No fresh long calculation is
started by the default wrapper. Use work/RUN_INDEPENDENT_REPLICATION.sh with
an explicit locked option when a reproducibility run is authorized.
