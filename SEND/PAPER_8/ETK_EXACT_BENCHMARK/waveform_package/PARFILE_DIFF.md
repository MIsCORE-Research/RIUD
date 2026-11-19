# Output-only parfile diff

Compared with the archived dense DH benchmark parfile, the waveform rerun
changes exactly these two settings:

```diff
- IO::out_dir = "/.../qc0-b03-dh-0p5-sigma-dense-ah-20260909/output"
+ IO::out_dir = "/.../qc0-b03-dh-0p5-sigma-dense-ah-20260910-waveform-rerun-20260910/output"
- Multipole::out_every = 0
+ Multipole::out_every = 1
```

No initial-data, gauge, grid, refinement, AHFinderDirect, QLM, evolution,
or physical parameter was changed.
