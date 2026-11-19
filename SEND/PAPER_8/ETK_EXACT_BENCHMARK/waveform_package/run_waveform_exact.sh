#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${WAVEFORM_OUTPUT_DIR:-$ROOT/output}"
TMP="$ROOT/.run-waveform.par"

DEFAULT_EXE="$ROOT/../gw150914-einstein-toolkit/qc0-b03-dh-0p5-sigma-dense-ah-20260909-recovered-exact/EXTERNAL_REPRO_PACKAGE/bin/cactus_cactus_sim"
EXE="${WAVEFORM_EXECUTABLE:-$DEFAULT_EXE}"
EXPECTED_SHA="9dfd62b8e9cbd057422e13f1e090c55828985079b07f40f18f3a93083760a12a"

if [[ ! -x "$EXE" ]]; then
  echo "missing executable: $EXE" >&2
  echo "Set WAVEFORM_EXECUTABLE to the exact recovered cactus_sim binary." >&2
  exit 2
fi

ACTUAL_SHA="$(sha256sum "$EXE" | awk '{print tolower($1)}')"
if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "executable SHA256 mismatch" >&2
  echo "expected=$EXPECTED_SHA" >&2
  echo "actual=$ACTUAL_SHA" >&2
  exit 3
fi

mkdir -p "$OUT"
sed "s#^IO::out_dir[[:space:]]*=.*#IO::out_dir = \"$OUT\"#" \
  "$ROOT/par/qc0-b03-dh-0p5-sigma-dense-ah.par" > "$TMP"

export OMP_NUM_THREADS="${OMP_NUM_THREADS:-16}"
export HDF5_USE_FILE_LOCKING="FALSE"
export LD_LIBRARY_PATH="$ROOT/../gw150914-einstein-toolkit/qc0-b03-dh-0p5-sigma-dense-ah-20260909-recovered-exact/EXTERNAL_REPRO_PACKAGE/lib:${LD_LIBRARY_PATH:-}"

echo "EXECUTABLE=$EXE"
echo "EXECUTABLE_SHA256=$ACTUAL_SHA"
echo "PARFILE=$TMP"
echo "OUTPUT=$OUT"
exec "$EXE" "$TMP"
