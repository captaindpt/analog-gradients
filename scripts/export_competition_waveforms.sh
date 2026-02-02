#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$REPO_DIR/competition/data"
source "$REPO_DIR/setup_cadence.sh"
ocean -nograph < "$REPO_DIR/ocean/export_competition_waveforms.ocn"
