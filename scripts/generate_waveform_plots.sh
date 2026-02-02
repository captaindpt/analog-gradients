#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$REPO_DIR/scripts/generate_waveform_plots.py"
