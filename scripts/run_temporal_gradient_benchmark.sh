#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_SWEEP_DIR="$REPO_DIR/competition/sweeps"
OUT_ANALYSIS_DIR="$REPO_DIR/competition/analysis"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$OUT_SWEEP_DIR/temporal_gradient_learning/$RUN_TS"
RUN_MANIFEST="$RUN_DIR/benchmark_manifest.txt"

ITERS="${ITERS:-4}"
TRACE_DELAYS_NS="${TRACE_DELAYS_NS:-}"
TRAIN_TRACE_DELAYS_NS="${TRAIN_TRACE_DELAYS_NS:-5.0,8.0}"
HOLDOUT_TRACE_DELAYS_NS="${HOLDOUT_TRACE_DELAYS_NS:-6.5,9.5}"
TARGET_MODE="${TARGET_MODE:-absolute}"
TARGET_SPIKES_NS="${TARGET_SPIKES_NS:-9.388,11.896,12.985,13.640}"
TARGET_SHIFT_NS="${TARGET_SHIFT_NS:-1.0,1.0,1.0,1.0}"
TARGET_SPIKE_COUNTS="${TARGET_SPIKE_COUNTS:-15,15,15,15}"
USE_ANCHOR_COUNTS="${USE_ANCHOR_COUNTS:-1}"
ANCHOR_PROBE_SPLIT="${ANCHOR_PROBE_SPLIT:-train}"
ENERGY_WEIGHT="${ENERGY_WEIGHT:-0.03}"
ENERGY_WEIGHT_START="${ENERGY_WEIGHT_START:-}"
ENERGY_WEIGHT_END="${ENERGY_WEIGHT_END:-}"

mkdir -p "$RUN_DIR" "$OUT_SWEEP_DIR" "$OUT_ANALYSIS_DIR"

source "$REPO_DIR/setup_cadence.sh"

{
  echo "run_id=$RUN_TS"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "iters=$ITERS"
  echo "trace_delays_ns=${TRACE_DELAYS_NS:-<unset>}"
  echo "train_trace_delays_ns=$TRAIN_TRACE_DELAYS_NS"
  echo "holdout_trace_delays_ns=$HOLDOUT_TRACE_DELAYS_NS"
  echo "target_mode=$TARGET_MODE"
  echo "target_spikes_ns=$TARGET_SPIKES_NS"
  echo "target_shift_ns=$TARGET_SHIFT_NS"
  echo "target_spike_counts=$TARGET_SPIKE_COUNTS"
  echo "use_anchor_counts=$USE_ANCHOR_COUNTS"
  echo "anchor_probe_split=$ANCHOR_PROBE_SPLIT"
  echo "energy_weight=$ENERGY_WEIGHT"
  echo "energy_weight_start=${ENERGY_WEIGHT_START:-<unset>}"
  echo "energy_weight_end=${ENERGY_WEIGHT_END:-<unset>}"
} > "$RUN_MANIFEST"

extra_args=()
if [[ "$USE_ANCHOR_COUNTS" == "1" ]]; then
  extra_args+=(--use-anchor-counts)
fi
if [[ -n "$ENERGY_WEIGHT_START" || -n "$ENERGY_WEIGHT_END" ]]; then
  if [[ -z "$ENERGY_WEIGHT_START" || -z "$ENERGY_WEIGHT_END" ]]; then
    echo "Set both ENERGY_WEIGHT_START and ENERGY_WEIGHT_END, or neither." >&2
    exit 1
  fi
  extra_args+=(--energy-weight-start "$ENERGY_WEIGHT_START" --energy-weight-end "$ENERGY_WEIGHT_END")
fi

if [[ -n "$TRACE_DELAYS_NS" ]]; then
  python3 "$REPO_DIR/scripts/train_temporal_gradient_loop.py" \
    --netlist-source "$REPO_DIR/netlists/neuro_tile4_coupled.scs" \
    --out-dir "$RUN_DIR" \
    --iters "$ITERS" \
    --trace-delays-ns "$TRACE_DELAYS_NS" \
    --target-first-spikes-ns "$TARGET_SPIKES_NS" \
    --target-mode "$TARGET_MODE" \
    --target-shift-ns "$TARGET_SHIFT_NS" \
    --target-spike-counts "$TARGET_SPIKE_COUNTS" \
    --anchor-probe-split "$ANCHOR_PROBE_SPLIT" \
    --energy-weight "$ENERGY_WEIGHT" \
    "${extra_args[@]}"
else
  python3 "$REPO_DIR/scripts/train_temporal_gradient_loop.py" \
    --netlist-source "$REPO_DIR/netlists/neuro_tile4_coupled.scs" \
    --out-dir "$RUN_DIR" \
    --iters "$ITERS" \
    --train-trace-delays-ns "$TRAIN_TRACE_DELAYS_NS" \
    --holdout-trace-delays-ns "$HOLDOUT_TRACE_DELAYS_NS" \
    --target-first-spikes-ns "$TARGET_SPIKES_NS" \
    --target-mode "$TARGET_MODE" \
    --target-shift-ns "$TARGET_SHIFT_NS" \
    --target-spike-counts "$TARGET_SPIKE_COUNTS" \
    --anchor-probe-split "$ANCHOR_PROBE_SPLIT" \
    --energy-weight "$ENERGY_WEIGHT" \
    "${extra_args[@]}"
fi
cp -f "$RUN_DIR/temporal_gradient_learning.csv" "$OUT_ANALYSIS_DIR/temporal_gradient_learning.csv"
cp -f "$RUN_DIR/temporal_gradient_trace.csv" "$OUT_ANALYSIS_DIR/temporal_gradient_trace.csv"
cp -f "$RUN_DIR/temporal_gradient_learning_summary.md" "$OUT_ANALYSIS_DIR/temporal_gradient_learning_summary.md"
cp -f "$RUN_DIR/temporal_gradient_learning_loss.svg" "$OUT_ANALYSIS_DIR/temporal_gradient_learning_loss.svg"
cp -f "$RUN_DIR/temporal_gradient_learning.csv" "$OUT_SWEEP_DIR/temporal_gradient_learning.csv"

{
  echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "run_dir=$RUN_DIR"
  echo "latest_eval_csv=$OUT_ANALYSIS_DIR/temporal_gradient_learning.csv"
  echo "latest_trace_csv=$OUT_ANALYSIS_DIR/temporal_gradient_trace.csv"
  echo "latest_summary_md=$OUT_ANALYSIS_DIR/temporal_gradient_learning_summary.md"
  echo "latest_loss_svg=$OUT_ANALYSIS_DIR/temporal_gradient_learning_loss.svg"
} >> "$RUN_MANIFEST"

echo "Temporal gradient benchmark complete:"
echo "  latest csv:  $OUT_ANALYSIS_DIR/temporal_gradient_learning.csv"
echo "  latest trace: $OUT_ANALYSIS_DIR/temporal_gradient_trace.csv"
echo "  latest md:   $OUT_ANALYSIS_DIR/temporal_gradient_learning_summary.md"
echo "  latest plot: $OUT_ANALYSIS_DIR/temporal_gradient_learning_loss.svg"
echo "  run dir:     $RUN_DIR"
echo "  manifest:    $RUN_MANIFEST"
