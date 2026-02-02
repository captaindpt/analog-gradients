#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[1/5] Refreshing analog verification artifacts..."
"$REPO_DIR/build.sh" synapse
"$REPO_DIR/build.sh" lif_neuron
"$REPO_DIR/build.sh" neuron_tile
"$REPO_DIR/build.sh" neuro_tile4
"$REPO_DIR/build.sh" neuro_tile4_coupled

echo "[2/5] Building metrics summary..."
"$REPO_DIR/scripts/collect_competition_metrics.sh"

echo "[3/5] Building architecture/timing diagrams..."
"$REPO_DIR/scripts/generate_competition_diagrams.sh"

echo "[4/5] Exporting sampled waveform CSV data..."
"$REPO_DIR/scripts/export_competition_waveforms.sh"

echo "[5/5] Rendering waveform plots..."
"$REPO_DIR/scripts/generate_waveform_plots.sh"

echo "Done. Visual assets ready under competition/diagrams and competition/plots."
