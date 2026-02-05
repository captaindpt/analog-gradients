#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="$REPO_DIR/competition/sweeps/nonlinearity/$RUN_TS"
ANALOG_DIR="$OUT_DIR/analog_softmax4"
DIGITAL_DIR="$OUT_DIR/digital_softmax4"
VEC_CSV="$REPO_DIR/competition/data/nonlinearity/softmax_vectors_n4.csv"
MODEL_CLASS="${MODEL_CLASS:-toy}"

mkdir -p "$ANALOG_DIR" "$DIGITAL_DIR"

source "$REPO_DIR/setup_cadence.sh"

if [[ "$MODEL_CLASS" == "pdk" ]]; then
  ANALOG_NETLIST="$REPO_DIR/netlists/softmax4_analog_gpdk180.scs"
  DIGITAL_NETLIST="$REPO_DIR/netlists/softmax4_digital_gpdk180.scs"
  ANALOG_EXTRA="itail=100u,rout=10000,w_exp=2u,l_exp=0.18u"
  DIGITAL_EXTRA="idigital=100u,kexp=2.0"
  ANALOG_OFFSET="1.8"
  ANALOG_SCALE="1.0"
  ANALOG_INVERT="--output-invert"
else
  ANALOG_NETLIST="$REPO_DIR/netlists/softmax4_analog_toy.scs"
  DIGITAL_NETLIST="$REPO_DIR/netlists/softmax4_digital_toy.scs"
  ANALOG_EXTRA="ibias=0.001,rout=1000,kexp=2.0"
  DIGITAL_EXTRA="idigital=0.001,kexp=2.0"
  ANALOG_OFFSET="0.0"
  ANALOG_SCALE="1.0"
  ANALOG_INVERT=""
fi

python3 "$REPO_DIR/scripts/run_nonlinearity_vector_benchmark.py" \
  --netlist "$ANALOG_NETLIST" \
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
  --extra-params "$ANALOG_EXTRA" \
  --output-offset "$ANALOG_OFFSET" \
  --output-scale "$ANALOG_SCALE" \
  $ANALOG_INVERT \
  --accuracy-tol 0.02 \
  --model-class "$MODEL_CLASS"

python3 "$REPO_DIR/scripts/run_nonlinearity_vector_benchmark.py" \
  --netlist "$DIGITAL_NETLIST" \
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
  --extra-params "$DIGITAL_EXTRA" \
  --accuracy-tol 0.02 \
  --model-class "$MODEL_CLASS"

echo "Nonlinearity benchmark complete:"
echo "  analog:  $ANALOG_DIR"
echo "  digital: $DIGITAL_DIR"
