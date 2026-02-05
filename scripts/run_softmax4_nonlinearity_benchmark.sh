#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="$REPO_DIR/competition/sweeps/nonlinearity/$RUN_TS"
ANALOG_DIR="$OUT_DIR/analog_softmax4"
DIGITAL_DIR="$OUT_DIR/digital_softmax4"
VEC_CSV="$REPO_DIR/competition/data/nonlinearity/softmax_vectors_n4.csv"

mkdir -p "$ANALOG_DIR" "$DIGITAL_DIR"

source "$REPO_DIR/setup_cadence.sh"

python3 "$REPO_DIR/scripts/run_nonlinearity_vector_benchmark.py" \
  --netlist "$REPO_DIR/netlists/softmax4_analog_toy.scs" \
  --vectors-csv "$VEC_CSV" \
  --out-dir "$ANALOG_DIR" \
  --input-params "in0,in1,in2,in3" \
  --output-nodes "out0,out1,out2,out3" \
  --input-cols "in0,in1,in2,in3" \
  --target-cols "soft0,soft1,soft2,soft3" \
  --tstop-ns 50 \
  --eval-time-ns 50 \
  --energy-dt-ps 100 \
  --vdd-val 1.8 \
  --extra-params "ibias=0.001,rout=1000,kexp=2.0" \
  --accuracy-tol 0.02 \
  --model-class toy

python3 "$REPO_DIR/scripts/run_nonlinearity_vector_benchmark.py" \
  --netlist "$REPO_DIR/netlists/softmax4_digital_toy.scs" \
  --vectors-csv "$VEC_CSV" \
  --out-dir "$DIGITAL_DIR" \
  --input-params "in0,in1,in2,in3" \
  --output-nodes "out0,out1,out2,out3" \
  --input-cols "in0,in1,in2,in3" \
  --target-cols "soft0,soft1,soft2,soft3" \
  --tstop-ns 50 \
  --eval-time-ns 50 \
  --energy-dt-ps 100 \
  --vdd-val 1.8 \
  --extra-params "idigital=0.001,kexp=2.0" \
  --accuracy-tol 0.02 \
  --model-class toy

echo "Nonlinearity benchmark complete:"
echo "  analog:  $ANALOG_DIR"
echo "  digital: $DIGITAL_DIR"
