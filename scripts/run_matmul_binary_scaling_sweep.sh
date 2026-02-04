#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_SWEEP_DIR="$REPO_DIR/competition/sweeps"
OUT_ANALYSIS_DIR="$REPO_DIR/competition/analysis"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$OUT_SWEEP_DIR/matmul_binary_scaling/$RUN_TS"
RUN_MANIFEST="$RUN_DIR/sweep_manifest.txt"

DIGITAL_TXT="$REPO_DIR/results/matmul2x2_binary_digital_test.txt"
NEURO_TXT="$REPO_DIR/results/matmul2x2_binary_neuro_test.txt"

N_LIST="${N_LIST:-2,4,8,12,16}"
DENSITY_LIST="${DENSITY_LIST:-0.10,0.30,0.50,0.80}"
SEED_LIST="${SEED_LIST:-1,2,3,4,5}"

mkdir -p "$RUN_DIR" "$OUT_SWEEP_DIR" "$OUT_ANALYSIS_DIR"

{
  echo "run_id=$RUN_TS"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "n_list=$N_LIST"
  echo "density_list=$DENSITY_LIST"
  echo "seed_list=$SEED_LIST"
} > "$RUN_MANIFEST"

# Refresh calibration points from verified transistor runs.
"$REPO_DIR/build.sh" matmul2x2_binary_digital
"$REPO_DIR/build.sh" matmul2x2_binary_neuro

RUN_CSV="$RUN_DIR/matmul_binary_scaling_sweep.csv"
RUN_MD="$RUN_DIR/matmul_binary_scaling_summary.md"
RUN_ENERGY_SVG="$RUN_DIR/matmul_binary_scaling_energy.svg"
RUN_PRESSURE_SVG="$RUN_DIR/matmul_binary_scaling_pressure.svg"

python3 "$REPO_DIR/scripts/analyze_matmul_binary_scaling.py" \
  --digital-report "$DIGITAL_TXT" \
  --neuro-report "$NEURO_TXT" \
  --n-list "$N_LIST" \
  --density-list "$DENSITY_LIST" \
  --seed-list "$SEED_LIST" \
  --out-csv "$RUN_CSV" \
  --out-md "$RUN_MD" \
  --out-energy-svg "$RUN_ENERGY_SVG" \
  --out-pressure-svg "$RUN_PRESSURE_SVG"

cp -f "$RUN_CSV" "$OUT_SWEEP_DIR/matmul_binary_scaling_sweep.csv"
cp -f "$RUN_MD" "$OUT_ANALYSIS_DIR/matmul_binary_scaling_summary.md"
cp -f "$RUN_ENERGY_SVG" "$OUT_ANALYSIS_DIR/matmul_binary_scaling_energy.svg"
cp -f "$RUN_PRESSURE_SVG" "$OUT_ANALYSIS_DIR/matmul_binary_scaling_pressure.svg"

{
  echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "run_csv=$RUN_CSV"
  echo "run_md=$RUN_MD"
  echo "run_energy_svg=$RUN_ENERGY_SVG"
  echo "run_pressure_svg=$RUN_PRESSURE_SVG"
  echo "latest_csv=$OUT_SWEEP_DIR/matmul_binary_scaling_sweep.csv"
  echo "latest_md=$OUT_ANALYSIS_DIR/matmul_binary_scaling_summary.md"
  echo "latest_energy_svg=$OUT_ANALYSIS_DIR/matmul_binary_scaling_energy.svg"
  echo "latest_pressure_svg=$OUT_ANALYSIS_DIR/matmul_binary_scaling_pressure.svg"
} >> "$RUN_MANIFEST"

echo "Matmul binary scaling sweep complete:"
echo "  latest csv:  $OUT_SWEEP_DIR/matmul_binary_scaling_sweep.csv"
echo "  latest md:   $OUT_ANALYSIS_DIR/matmul_binary_scaling_summary.md"
echo "  latest plot: $OUT_ANALYSIS_DIR/matmul_binary_scaling_energy.svg"
echo "  latest plot: $OUT_ANALYSIS_DIR/matmul_binary_scaling_pressure.svg"
echo "  run dir:     $RUN_DIR"
echo "  manifest:    $RUN_MANIFEST"
