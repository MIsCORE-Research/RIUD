# External reproduction package: QC0 b=0.3 dense DH audit

This package runs the recovered original Einstein Toolkit executable. It is not a new build and it does not use the rejected OpenMPI rerun.

## Run contract

The evolution must run from `t=0` to `t=0.5M`. The scientific DH comparison uses only the matched common-horizon surfaces at:

```text
0.25, 0.3125, 0.375, 0.4375, 0.5 M
```

Run on Linux/WSL with MPICH/HDF5/GSL runtime libraries:

```bash
cd EXTERNAL_REPRO_PACKAGE
chmod +x run_exact.sh
./run_exact.sh
```

The script creates a temporary parfile with a local output directory, so it does not overwrite the supplied parfile or expected result.

## Expected result

Compare `output/N16_AK_DENSE_CONVERGENCE.csv` against `expected/N16_AK_DENSE_CONVERGENCE.csv`.

```text
SIGMA trapezoid       72.4946318678449 %
2 ZETA trapezoid      26.1709286141522 %
TOTAL trapezoid       98.6655604819971 %
TOTAL Simpson          98.5492211880621 %
TOTAL 3-point trap     99.1929380726778 %
observed Delta R       0.0011565307450602802
```

## Exact numerical contract

- Cactus version: 4.20.0
- ET release: ET_2025_05 / Kruskal
- original executable SHA256: `9dfd62b8e9cbd057422e13f1e090c55828985079b07f40f18f3a93083760a12a`
- MPI process count: 1; direct execution, no MPI launcher
- `TwoPunctures::par_b = 0.3`
- `Cactus::cctk_final_time = 0.5`
- AHFinderDirect `find_every = 32`, common AH branch surface 3, stored QLM surface index 2
- QLM `ntheta=39`, `nphi=76`, fourth-order Lagrange interpolation, spatial order 4
- MoL RK4; `dtfac=0.25`; Carpet refinement factors `[1,1,2,4,8,16,32,64,128,256]`
- DH interval: `.25M -> .50M` only

See `../RECOVERY_PROVENANCE.md` and `../SHA256_MANIFEST.txt` for source, parfile, producer, and provenance hashes.

## Rebuild note

The supplied executable is the exact recovered binary used for the benchmark. Rebuilding from source requires the full Einstein Toolkit source snapshot and the archived QuasiLocalMeasures producer; `source/Cactus-source-QuasiLocalMeasures.tar.gz` is the exact producer archive used for the dense fields.
