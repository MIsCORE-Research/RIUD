# MPI runtime provenance

The ETK waveform reproduction package was executed from WSL2. It did not use
OpenMPI.

```text
ENVIRONMENT              = WSL2
MPI_IMPLEMENTATION       = MPICH
MPI_RUNTIME_LIBRARY      = libmpich.so.12
HDF5_MPI_LIBRARY         = libhdf5_mpich.so.310
OPENMPI_USED             = FALSE
MPI_PROCESSES            = 1
OMP_NUM_THREADS          = 16
```

Evidence:

- `ldd cactus_cactus_sim` resolves `libmpich.so.12` and
  `libhdf5_mpich.so.310`.
- The run log reports one MPI process (`MPI process 0 of 1`).
- The Cactus `MPI` thorn was active, but that is the Cactus MPI interface;
  it does not identify OpenMPI as the implementation.
- The 16-way parallel setting refers to OpenMP threads, not 16 MPI ranks.
