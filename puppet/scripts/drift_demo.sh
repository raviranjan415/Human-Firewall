#!/usr/bin/env bash
# Puppet Configuration Drift Demonstration Runner
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${SCRIPT_DIR}/../../.venv/bin/python"

if [[ -x "${PYTHON_BIN}" ]]; then
    exec "${PYTHON_BIN}" "${SCRIPT_DIR}/drift_demo.py" "$@"
else
    exec python3 "${SCRIPT_DIR}/drift_demo.py" "$@"
fi

