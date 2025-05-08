#!/usr/bin/env bash
# run_deploy.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR"/.. && pwd)"
pip install -r "$PROJECT_ROOT/requirements.txt"

python3 "$SCRIPT_DIR/generate_env_file.py"

python3 "$SCRIPT_DIR/deploy_sm.py"

python3 "$SCRIPT_DIR/copy_env.py"
