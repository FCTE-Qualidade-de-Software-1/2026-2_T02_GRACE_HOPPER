#!/usr/bin/env bash
# Invocado pelo executor a partir da raiz da worktree do produto.
set -euo pipefail
M3_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export M3_PRODUCT_DIR="${M3_PRODUCT_DIR:-$PWD}"
exec docker compose -f "$M3_SCRIPT_DIR/compose.yml" exec -T php php "$@"
