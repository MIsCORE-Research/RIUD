# ETK same-run waveform-output reproduction package

This package reproduces the QC0 `b=0.3`, N16, `0 -> 0.5M` run with the
same evolution, AHFinderDirect, QLM, grid, and gauge contract as the dense
dynamical-horizon benchmark, while enabling Multipole/Psi4 output.

The only scientific parameter changes relative to the archived dense DH
parfile are:

```text
IO::out_dir          output-only relocation
Multipole::out_every 0 -> 1
```

The exact recovered executable is deliberately not duplicated here because
it is approximately 1 GB. The runner locates the sibling exact package and
checks its SHA256 before execution. Override it with `WAVEFORM_EXECUTABLE`
if the package is moved.

## Run

From WSL:

```bash
cd /mnt/e/RIUD_ACTIVE_20260808/PAPER_8/MIsCORE_ETK_DH_RERUN_SOURCE_AUDIT_R0_20260908/ETK_WAVEFORM_REPRO_PACKAGE_20260910
chmod +x run_waveform_exact.sh
./run_waveform_exact.sh
```

## MPI/runtime provenance

This package was run under WSL2 without Docker Desktop and without OpenMPI.
The executable is linked against MPICH:

```text
MPI_IMPLEMENTATION = MPICH
MPI_RUNTIME_LIBRARY = libmpich.so.12
HDF5_MPI_LIBRARY = libhdf5_mpich.so.310
OPENMPI_USED = FALSE
MPI_PROCESSES = 1
OMP_NUM_THREADS = 16
```

The `MPI` thorn being active in the Cactus log identifies Cactus MPI support;
it does not mean that OpenMPI was used.

The run writes to `output/` and uses the included temporary parfile. It does
not alter the archived source run.

## Fixed contract

- `TwoPunctures::par_b = 0.3`
- final time `0.5M`
- `AHFinderDirect::find_every = 32`
- common AH branch: surface 3; QLM stored surface index 2
- DH comparison interval: `0.25M -> 0.50M`
- `Multipole::out_every = 1`
- extraction radii: `15,30,40,50,60,70,80,90M`
- Psi4 multipoles through `l=4`
- observed rerun output: 200 Psi4 ASCII files, 33 samples per file

The baseline DH expected values are in `expected/`. The waveform-output rerun
must reproduce the baseline DH scalar rows and additionally produce
`mp_Psi4_l*_m*_r*.asc` files.

## Exact executable

Expected SHA256:

```text
9dfd62b8e9cbd057422e13f1e090c55828985079b07f40f18f3a93083760a12a
```

The source rerun log, full output, and independent audit are retained in the
archived `qc0-b03-dh-0p5-sigma-dense-ah-20260910-waveform-rerun-20260910`
directory beside this package.
