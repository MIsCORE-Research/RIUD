# Known Limitations

- `ENV_A` exact original package versions are not fully proven from contemporaneous exports. The closest compatible lock is bundled from the current base environment lineage, while unresolved items are labeled `UNKNOWN_AT_ORIGINAL_RUN`.
- `ENV_B` is strongly supported by `prismgw_v5` conda history and shell history, but not every transient pip package state is proven at every intermediate step.
- Public GWOSC downloads may be scientifically content-equivalent without being byte-identical to prior local cache files. Those cases are reported as `CONTENT_EQUIVALENCE_NOT_BYTE_IDENTICAL`.
- The smoke tests executed during package assembly are minimal path and runner checks, not full 374-event or 100,000-draw reruns.

