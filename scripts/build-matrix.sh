#!/usr/bin/env bash
# Delegate to the real matrix builder in tests/harness/.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 ./tests/harness/build-matrix.py "$@"