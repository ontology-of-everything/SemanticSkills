#!/usr/bin/env bash
# Publish huawei-cloud-billing-scout to ClawHub.
# Registry license is MIT-0 (ClawHub policy). GitHub repo may stay Apache-2.0.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/../../../skills/huawei-cloud-billing-scout" && pwd)"
VERSION="${1:-2.0.0}"
CHANGELOG="${2:-Read-only Huawei Cloud BSS billing scout with semantic layer.}"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    printf 'Install clawhub: npm i -g clawhub\n' >&2
    exit 1
  }
}

need_cmd clawhub

if ! clawhub whoami >/dev/null 2>&1; then
  printf '%s\n' \
    'Not logged in to ClawHub.' \
    '  clawhub login              # browser' \
    '  clawhub login --device      # headless: approve at clawhub.ai/cli/device' \
    'Then re-run this script.' >&2
  exit 1
fi

clawhub skill publish "$SKILL_DIR" \
  --slug huawei-cloud-billing-scout \
  --name "Huawei Cloud Billing Scout" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --clawscan-note "Read-only BSS via hcloud; user installs KooCLI manually; AK/SK via hcloud configure or optional HUAWEICLOUD_SDK_* env vars; refuses payment/delete/refund/write ops."

printf 'OK: published huawei-cloud-billing-scout@%s to ClawHub\n' "$VERSION"
