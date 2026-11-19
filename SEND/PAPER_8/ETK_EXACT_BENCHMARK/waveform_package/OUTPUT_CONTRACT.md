# Waveform-output result contract

The source rerun is accepted only if all of the following hold:

1. The DH scalar rows at `0.25, 0.3125, 0.375, 0.4375, 0.5M` match the
   archived dense run within the archived numeric tolerance.
2. `mp_Psi4_l*_m*_r*.asc` files exist for the configured radii and contain
   the expected time series.
3. The executable hash is the exact recovered hash in `SHA256_MANIFEST.txt`.
4. The parfile differs from the dense source only in `IO::out_dir` and
   `Multipole::out_every`.

The existing successful rerun produced 200 Psi4 ASCII files at eight radii,
with 33 samples per file. This is source-waveform output only; it is not yet
an eventwise ETK-to-RAW C(t) proof.
