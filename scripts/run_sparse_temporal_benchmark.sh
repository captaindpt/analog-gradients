#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_SWEEP_DIR="$REPO_DIR/competition/sweeps"
OUT_ANALYSIS_DIR="$REPO_DIR/competition/analysis"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$OUT_SWEEP_DIR/sparse_temporal_benchmark/$RUN_TS"
RUN_MANIFEST="$RUN_DIR/benchmark_manifest.txt"

COINCIDENCE_TXT="$REPO_DIR/results/coincidence_detector_test.txt"
CROSSOVER_CSV="$REPO_DIR/competition/sweeps/matmul4x4_crossover/matmul4x4_crossover.csv"

RUN_CSV="$RUN_DIR/sparse_temporal_benchmark.csv"
RUN_MD="$RUN_DIR/sparse_temporal_benchmark_summary.md"
RUN_RATIO_SVG="$RUN_DIR/sparse_temporal_benchmark_ratio.svg"
RUN_EPTP_SVG="$RUN_DIR/sparse_temporal_benchmark_eptp.svg"

LATEST_CSV="$OUT_ANALYSIS_DIR/sparse_temporal_benchmark.csv"
LATEST_MD="$OUT_ANALYSIS_DIR/sparse_temporal_benchmark_summary.md"
LATEST_RATIO_SVG="$OUT_ANALYSIS_DIR/sparse_temporal_benchmark_ratio.svg"
LATEST_EPTP_SVG="$OUT_ANALYSIS_DIR/sparse_temporal_benchmark_eptp.svg"

ACTIVE_FRACTIONS="${ACTIVE_FRACTIONS:-0.00001,0.00003,0.0001,0.0003,0.001,0.003,0.01,0.03,0.10}"
WINDOWS="${WINDOWS:-1000000}"
DIGITAL_TPR="${DIGITAL_TPR:-1.0}"
DIGITAL_FPR="${DIGITAL_FPR:-0.0}"
MAX_LATENCY_NS="${MAX_LATENCY_NS:-15.0}"
MAX_FPR="${MAX_FPR:-0.01}"
MIN_TPR="${MIN_TPR:-0.99}"

mkdir -p "$RUN_DIR" "$OUT_SWEEP_DIR" "$OUT_ANALYSIS_DIR"

if [[ ! -f "$CROSSOVER_CSV" ]]; then
  echo "Missing crossover calibration CSV: $CROSSOVER_CSV" >&2
  echo "Run scripts/run_matmul4x4_crossover_sweep.sh first." >&2
  exit 1
fi

{
  echo "run_id=$RUN_TS"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "crossover_csv=$CROSSOVER_CSV"
  echo "active_fractions=$ACTIVE_FRACTIONS"
  echo "windows=$WINDOWS"
  echo "digital_tpr=$DIGITAL_TPR"
  echo "digital_fpr=$DIGITAL_FPR"
  echo "max_latency_ns=$MAX_LATENCY_NS"
  echo "max_fpr=$MAX_FPR"
  echo "min_tpr=$MIN_TPR"
} > "$RUN_MANIFEST"

"$REPO_DIR/build.sh" coincidence_detector

extra_args=()
if [[ -n "${DIGITAL_LATENCY_NS:-}" ]]; then
  extra_args+=(--digital-latency-ns "$DIGITAL_LATENCY_NS")
fi

python3 "$REPO_DIR/scripts/analyze_sparse_temporal_benchmark.py" \
  --crossover-csv "$CROSSOVER_CSV" \
  --coincidence-report "$COINCIDENCE_TXT" \
  --active-fractions "$ACTIVE_FRACTIONS" \
  --windows "$WINDOWS" \
  --digital-tpr "$DIGITAL_TPR" \
  --digital-fpr "$DIGITAL_FPR" \
  --max-latency-ns "$MAX_LATENCY_NS" \
  --max-fpr "$MAX_FPR" \
  --min-tpr "$MIN_TPR" \
  --out-csv "$RUN_CSV" \
  --out-md "$RUN_MD" \
  --out-ratio-svg "$RUN_RATIO_SVG" \
  --out-eptp-svg "$RUN_EPTP_SVG" \
  "${extra_args[@]}"

cp -f "$RUN_CSV" "$LATEST_CSV"
cp -f "$RUN_MD" "$LATEST_MD"
cp -f "$RUN_RATIO_SVG" "$LATEST_RATIO_SVG"
cp -f "$RUN_EPTP_SVG" "$LATEST_EPTP_SVG"
cp -f "$RUN_CSV" "$OUT_SWEEP_DIR/sparse_temporal_benchmark.csv"

{
  echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "run_csv=$RUN_CSV"
  echo "run_md=$RUN_MD"
  echo "run_ratio_svg=$RUN_RATIO_SVG"
  echo "run_eptp_svg=$RUN_EPTP_SVG"
  echo "latest_csv=$LATEST_CSV"
  echo "latest_md=$LATEST_MD"
  echo "latest_ratio_svg=$LATEST_RATIO_SVG"
  echo "latest_eptp_svg=$LATEST_EPTP_SVG"
} >> "$RUN_MANIFEST"

echo "Sparse temporal benchmark complete:"
echo "  latest csv:  $LATEST_CSV"
echo "  latest md:   $LATEST_MD"
echo "  latest plot: $LATEST_RATIO_SVG"
echo "  latest plot: $LATEST_EPTP_SVG"
echo "  run dir:     $RUN_DIR"
echo "  manifest:    $RUN_MANIFEST"
