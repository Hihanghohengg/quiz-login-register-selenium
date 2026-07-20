#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
cp tests/stubs/index.php index.php
mkdir -p artifacts
php -d display_errors=0 -S 127.0.0.1:8000 > artifacts/php-server.log 2>&1 &
echo $! > artifacts/php-server.pid
echo "Aplikasi berjalan di http://127.0.0.1:8000/login.php"
