#!/usr/bin/env bash
# Serve the Kestrel Works company repo locally so the website can fetch its
# own source files (HISTORY.md, department charters, updates.json).
set -euo pipefail

PORT="${1:-8765}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Kestrel Works — serving ${ROOT}"
echo "Open: http://localhost:${PORT}/website/"
cd "$ROOT"
exec python3 -m http.server "$PORT"
