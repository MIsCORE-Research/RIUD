# Recovered exact dense DH run

STATUS: COMPLETE
REPRODUCTION_VERDICT: EXACT_BENCHMARK_REPRODUCED
RECOVERY_BASIS: original WSL executable and original parfile
RECOVERED_OUTPUT_DIR: `qc0-b03-dh-0p5-sigma-dense-ah-20260909-recovered-exact`
VALID_DH_ANALYSIS_INTERVAL: 0.25M -> 0.50M only
EVOLUTION_INTERVAL: 0.00M -> 0.50M (required because no compatible 0.25M checkpoint was archived)

## Original execution contract

- Original executable: `/home/mickey/riud-cactus-corrected/exe/cactus_cactus_sim`
- Executable SHA256: `9dfd62b8e9cbd057422e13f1e090c55828985079b07f40f18f3a93083760a12a`
- Reported executable version: `Cactus 4.20.0; compiled Sep 09 2026 13:21:38`
- Original working directory: `/home/mickey/riud-cactus-corrected`
- MPI process count: `1`
- Launcher: direct executable invocation, no OpenMPI/MPICH launcher
- Current WSL runtime: GCC 15.2.0, GFortran 15.2.0, MPICH/HYDRA 4.3.2
- Recovery command: `./exe/cactus_cactus_sim <original-parfile> IO::out_dir=<recovered-output-dir>`
- No Docker/OpenMPI runtime is used for the recovery run
- Parfile: `qc0-b03-dh-0p5-sigma-dense-ah.par`
- Parfile SHA256: `32AD449642C8282D6F9E5F8FF8848AA84B3BA34943E9E44E60F51A202C24F547`
- Archived exact QuasiLocalMeasures source SHA256: `66A72F982F322F971EBBC9A1249385C8F17388E71DC3854C35A4531ABB77AC57`
- `Cactus::cctk_final_time = 0.5`
- `TwoPunctures::par_b = 0.3`
- `AHFinderDirect::find_every = 32`
- `AHFinderDirect::find_after_individual_time[3] = 0.0`
- `AHFinderDirect::find_after_individual_time[6] = 0.0`
- `AHFinderDirect::N_horizons = 6`
- canonical common horizon: AHFinderDirect surface 3 / stored surface index 2
- QLM: `num_surfaces = 1`, `surface_index[0] = 2`, `output_vtk_every = 32`
- surface angular grid: `ntheta = 39`, `nphi = 76`, two ghost zones
- interpolation: fourth-order Lagrange
- spatial order: 4
- Carpet time refinement factors: `[1,1,2,4,8,16,32,64,128,256]`
- MoL: RK4, 4 intermediate steps
- grid: CoordBase minmax, dx=dy=dz=2, domain x=[0,120], y=[-120,120], z=[0,120]
- refinement: Carpet max level 10; CarpetRegrid2 levels 7 around each puncture; radii 64,16,8,4,2,1

## Reproduced result

- sigma trapezoid: `72.4946318678449%`
- 2-zeta trapezoid: `26.1709286141522%`
- total trapezoid: `98.6655604819971%`
- total Simpson: `98.5492211880621%`
- total 3-point trapezoid: `99.1929380726778%`
- observed Delta R: `0.0011565307450602802`
- result CSV: `run-output/N16_AK_DENSE_CONVERGENCE.csv`
- result Markdown: `run-output/N16_AK_DENSE_CONVERGENCE.md`
- raw recovered output: `run-output/`

## Required final audit

Use only matched surfaces at `0.25, 0.3125, 0.375, 0.4375, 0.5M`. Do not include t=0 or earlier diagnostic surfaces in the DH balance interval.

Required outputs after completion:

- exact sigma definition and producer field
- exact zeta definition and producer field
- N_R definition
- boost and null-normalization convention
- surface metric and area measure
- quadrature: five-point trapezoid, five-point Simpson, and three-point trapezoid
- source patch hash and executable hash
- compiler, MPI, Cactus/ET release, active thorn list, and full parfile hash
- comparison against the archived benchmark:
  - sigma trapezoid 72.49463187%
  - 2-zeta trapezoid 26.17092861%
  - total trapezoid 98.66556048%
  - total Simpson 98.54922119%
  - total 3-point trapezoid 99.19293807%
  - observed Delta R 0.0011565307450602802
