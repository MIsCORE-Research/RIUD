# Existing successful rerun reference

The already completed output is retained at:

```text
../gw150914-einstein-toolkit/qc0-b03-dh-0p5-sigma-dense-ah-20260910-waveform-rerun-20260910/output
```

Observed result:

- 200 `mp_Psi4_l*_m*_r*.asc` files
- extraction radii: 15, 30, 40, 50, 60, 70, 80, 90M
- 33 samples per file
- sample `mp_Psi4_l2_m2_r50.00.asc` SHA256:
  `3FADCA3FC6AC99AF7F0B8EB3334722D4903F5E741A853AF23DA16CC3496D07EA`

The DH scalar rows and AH surface VTK files were numerically/bytewise
compared against the baseline run; they matched under the archived audit.
