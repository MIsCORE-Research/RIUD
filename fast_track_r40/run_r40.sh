#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" "$SCRIPT_DIR/reproduce_r40.py" "$@"
