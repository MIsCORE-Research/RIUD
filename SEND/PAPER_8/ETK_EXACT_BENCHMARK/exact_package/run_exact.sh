#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/output"
TMP="$ROOT/.run.par"
mkdir -p "$OUT"

if [[ ! -x "$ROOT/bin/cactus_cactus_sim" ]]; then
  echo "missing executable: bin/cactus_cactus_sim" >&2
  exit 2
fi

# The supplied parfile contains the original absolute output path. Generate a
# temporary local copy so external users do not overwrite the source archive.
sed "s#^IO::out_dir[[:space:]]*=.*#IO::out_dir = \"$OUT\"#" \
  "$ROOT/par/qc0-b03-dh-0p5-sigma-dense-ah.par" > "$TMP"

export OMP_NUM_THREADS="${OMP_NUM_THREADS:-16}"
export HDF5_USE_FILE_LOCKING="FALSE"
export LD_LIBRARY_PATH="$ROOT/lib:${LD_LIBRARY_PATH:-}"

exec "$ROOT/bin/cactus_cactus_sim" "$TMP"
