# Reproduction Modes

## QUICK_REPRO

- Uses existing downloaded data if present under `RIUD_DATA`
- Verifies SHA256 before use
- Runs smoke/full wrappers against frozen inputs and compares outputs to frozen authorities
- Intended for developer or reviewer confirmation

## FULL_CLEAN_REPRO

- Starts from an empty output tree
- Creates `ENV_A` and `ENV_B` separately
- Downloads public raw data described by `05_RAW_DATA_FETCH/RAW_DATA_MANIFEST.csv`
- Runs Paper I, then Paper II stages in dependency order
- Writes new outputs under `RIUD_OUTPUT`
- Never overwrites bundled frozen authorities

Parallel policy:
- default workers: `8`
- all event/control/null loops use isolated worker scratch under `RIUD_OUTPUT/workers`
- final merge is deterministic

