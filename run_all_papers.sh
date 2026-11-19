#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" "$ROOT_DIR/src/run_all_verifications.py" "$@"
