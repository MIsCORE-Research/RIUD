# Package execution verification

The package runner was executed successfully from WSL on 2026-09-10.

Runtime provenance:

```text
ENVIRONMENT = WSL2
MPI_IMPLEMENTATION = MPICH
MPI_RUNTIME_LIBRARY = libmpich.so.12
HDF5_MPI_LIBRARY = libhdf5_mpich.so.310
OPENMPI_USED = FALSE
MPI_PROCESSES = 1
OMP_NUM_THREADS = 16
```

The executable dependency audit, not the generic Cactus `MPI` thorn name, is
the authority for the MPI implementation.

```text
RUN_STATUS = PASS
FINAL_LOG_LINE = Done.
PSI4_ASCII_FILE_COUNT = 200
EXPECTED_PSI4_ASCII_FILE_COUNT = 200
```

The five matched AH surface VTK files used by the dense DH audit were
bytewise identical to the archived baseline:

```text
surface01_00000128.vtk
surface01_00000160.vtk
surface01_00000192.vtk
surface01_00000224.vtk
surface01_00000256.vtk
```

```text
VTK_MATCH_COUNT = 5/5
```

The source-waveform sample hash also reproduced:

```text
mp_Psi4_l2_m2_r50.00.asc
SHA256 = 3FADCA3FC6AC99AF7F0B8EB3334722D4903F5E741A853AF23DA16CC3496D07EA
```

The complete execution log is `package_rerun.log`; its SHA256 is:

```text
C69D0D6028F15128CD429ED74620B9530B222661D54E77D8627D899D896D45C3
```

This verifies reproduction of the same DH geometry and the additional Psi4
output. It does not by itself establish an eventwise ETK-to-RAW C(t) law.
