#!/usr/bin/env bash
# Offline quality gate for huawei-cloud-billing-scout (delegates to bin/gate.py).
set -euo pipefail
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$QA_DIR/bin/gate.py" full "$@"
