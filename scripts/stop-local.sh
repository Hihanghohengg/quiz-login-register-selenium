#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT_DIR/artifacts/php-server.pid"
if [[ -f "$PID_FILE" ]]; then
  kill "$(cat "$PID_FILE")" 2>/dev/null || true
  rm -f "$PID_FILE"
fi
rm -f "$ROOT_DIR/index.php"
echo "Server lokal dihentikan."
