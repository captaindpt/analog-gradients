#!/bin/bash
# Run a Virtuoso SKILL replay script in a headless-friendly way.
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: scripts/virtuoso_replay.sh <skill_script.il> [--] [extra_args...]

Runs: virtuoso -nograph -replay <skill_script.il>
If DISPLAY is not set, it will try xvfb-run when available.
EOF
}

if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Source Cadence env if available.
if [[ -f "${REPO_ROOT}/setup_cadence.sh" ]]; then
    # shellcheck disable=SC1091
    source "${REPO_ROOT}/setup_cadence.sh"
fi

SKILL_PATH="$1"
shift || true

if [[ ! -f "${SKILL_PATH}" ]]; then
    echo "ERROR: SKILL file not found: ${SKILL_PATH}" >&2
    exit 1
fi

# Resolve to absolute path for reliable replay.
SKILL_PATH="$(cd "$(dirname "${SKILL_PATH}")" && pwd)/$(basename "${SKILL_PATH}")"

VIRTUOSO_CMD=(virtuoso -nograph -replay "${SKILL_PATH}")
if [[ $# -gt 0 ]]; then
    VIRTUOSO_CMD+=("$@")
fi

if [[ -n "${DISPLAY:-}" ]]; then
    echo "Using DISPLAY=${DISPLAY}"
    "${VIRTUOSO_CMD[@]}"
    exit $?
fi

if command -v xvfb-run >/dev/null 2>&1; then
    echo "DISPLAY not set; using xvfb-run"
    xvfb-run -a "${VIRTUOSO_CMD[@]}"
    exit $?
fi

cat <<'EOF' >&2
ERROR: DISPLAY is not set and xvfb-run is not available.
Either:
  - SSH with X11 forwarding (ssh -Y ...) so DISPLAY is set, or
  - Install/run Xvfb and retry.
EOF
exit 1
