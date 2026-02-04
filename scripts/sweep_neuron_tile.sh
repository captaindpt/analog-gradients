#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NETLIST_SRC="$REPO_DIR/netlists/neuron_tile.scs"
TMP_NETLIST="$REPO_DIR/results/neuron_tile/neuron_tile_sweep_tmp.scs"
RESULT_DIR="$REPO_DIR/results/neuron_tile"
OUT_DIR="$REPO_DIR/competition/sweeps"
OUT_CSV="$OUT_DIR/neuron_tile_sweep.csv"
OUT_MD="$OUT_DIR/neuron_tile_sweep_summary.md"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$RESULT_DIR/sweeps/$RUN_TS"
RUN_CSV="$RUN_DIR/neuron_tile_sweep.csv"
RUN_MD="$RUN_DIR/neuron_tile_sweep_summary.md"
RUN_MANIFEST="$RUN_DIR/sweep_manifest.txt"

mkdir -p "$RESULT_DIR" "$OUT_DIR" "$RUN_DIR"

source "$REPO_DIR/setup_cadence.sh"

RCOUPLE_LIST="${RCOUPLE_LIST:-6k,8k,10k}"
RLEAK_LIST="${RLEAK_LIST:-6M,8M,10M}"
TRAN_MAXSTEP="${TRAN_MAXSTEP:-100p}"

# Robustness pass-band defaults.
MIN_SPIKE_COUNT="${MIN_SPIKE_COUNT:-1}"
MIN_MEM_MAX_V="${MIN_MEM_MAX_V:-0.40}"
FIRST_SPIKE_NS_MIN="${FIRST_SPIKE_NS_MIN:-5.0}"
FIRST_SPIKE_NS_MAX="${FIRST_SPIKE_NS_MAX:-220.0}"

IFS=',' read -r -a rcouple_vals <<< "$RCOUPLE_LIST"
IFS=',' read -r -a rleak_vals <<< "$RLEAK_LIST"

{
  echo "run_id=$RUN_TS"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "r_couple_list=$RCOUPLE_LIST"
  echo "rleak_list=$RLEAK_LIST"
  echo "tran_maxstep=$TRAN_MAXSTEP"
  echo "min_spike_count=$MIN_SPIKE_COUNT"
  echo "min_mem_max_v=$MIN_MEM_MAX_V"
  echo "first_spike_ns_min=$FIRST_SPIKE_NS_MIN"
  echo "first_spike_ns_max=$FIRST_SPIKE_NS_MAX"
} > "$RUN_MANIFEST"

echo "run_id,point_id,r_couple,rleak,nominal_pass,band_pass,overall_pass,spike_count,mem_max_v,first_spike_ns,tran_maxstep,raw_dir,result_file,spectre_log,ocean_log" > "$RUN_CSV"

for rcouple in "${rcouple_vals[@]}"; do
  for rleak in "${rleak_vals[@]}"; do
    point_id="rcouple_${rcouple}_rleak_${rleak}"
    point_tag="$(printf '%s' "$point_id" | tr -c 'A-Za-z0-9._-' '_')"
    point_dir="$RUN_DIR/$point_tag"
    point_raw="$point_dir/neuron_tile.raw"
    point_result="$point_dir/neuron_tile_test.txt"
    point_spectre="$point_dir/spectre.log"
    point_ocean="$point_dir/ocean.log"
    mkdir -p "$point_dir"

    sed -E \
      -e "s/^parameters .*/parameters vdd_val=1.8 cpost=200f rdecay=80k r_couple=${rcouple} cmem=500f rleak=${rleak}/" \
      -e "s/^tran_test tran stop=250n.*/tran_test tran stop=250n maxstep=${TRAN_MAXSTEP}/" \
      "$NETLIST_SRC" > "$TMP_NETLIST"

    rm -rf "$RESULT_DIR/neuron_tile.raw"
    rm -f "$RESULT_DIR/spectre.log" "$REPO_DIR/results/neuron_tile_test.txt"

    sim_start_epoch="$(date +%s)"
    if ! (cd "$RESULT_DIR" && spectre "$TMP_NETLIST" -raw neuron_tile.raw +log spectre.log >/dev/null 2>&1); then
      nominal_pass="FAIL"
    elif ! grep -q "completes with 0 errors" "$RESULT_DIR/spectre.log"; then
      nominal_pass="FAIL"
    else
      raw_psfxl="$RESULT_DIR/neuron_tile.raw/tran_test.tran.tran.psfxl"
      if [[ ! -f "$raw_psfxl" ]]; then
        nominal_pass="FAIL"
      elif (( $(stat -c %Y "$raw_psfxl") < sim_start_epoch )); then
        nominal_pass="FAIL"
      else
        if ocean -nograph < "$REPO_DIR/ocean/test_neuron_tile.ocn" >"$RESULT_DIR/ocean.log" 2>&1; then
          if grep -q "=== PASS" "$REPO_DIR/results/neuron_tile_test.txt" 2>/dev/null; then
            nominal_pass="PASS"
          else
            nominal_pass="FAIL"
          fi
        else
          nominal_pass="FAIL"
        fi
      fi
    fi

    cp -a "$RESULT_DIR/neuron_tile.raw" "$point_raw" 2>/dev/null || true
    cp -f "$RESULT_DIR/spectre.log" "$point_spectre" 2>/dev/null || true
    cp -f "$RESULT_DIR/ocean.log" "$point_ocean" 2>/dev/null || true
    cp -f "$REPO_DIR/results/neuron_tile_test.txt" "$point_result" 2>/dev/null || true

    spike_count="$(grep -m1 "Spike node pulses detected" "$point_result" 2>/dev/null | awk -F: '{print $2}' | awk '{print $1}' || true)"
    mem_max_v="$(grep -m1 "Vmem max" "$point_result" 2>/dev/null | awk -F: '{print $2}' | awk '{print $1}' || true)"
    first_spike_ns="$(grep -m1 "First spike time" "$point_result" 2>/dev/null | awk -F: '{print $2}' | awk '{print $1}' || true)"

    band_pass="$(python3 - "$spike_count" "$mem_max_v" "$first_spike_ns" "$MIN_SPIKE_COUNT" "$MIN_MEM_MAX_V" "$FIRST_SPIKE_NS_MIN" "$FIRST_SPIKE_NS_MAX" <<'PY'
import math
import sys

def to_float(v):
    try:
        return float(v)
    except Exception:
        return math.nan

spikes = to_float(sys.argv[1])
mem_max = to_float(sys.argv[2])
first_ns = to_float(sys.argv[3])
min_spikes = to_float(sys.argv[4])
min_mem = to_float(sys.argv[5])
min_first = to_float(sys.argv[6])
max_first = to_float(sys.argv[7])

ok = (
    not math.isnan(spikes) and spikes >= min_spikes and
    not math.isnan(mem_max) and mem_max >= min_mem and
    not math.isnan(first_ns) and min_first <= first_ns <= max_first
)
print("PASS" if ok else "FAIL")
PY
)"

    if [[ "$band_pass" == "PASS" ]]; then
      overall_pass="PASS"
    else
      overall_pass="FAIL"
    fi

    echo "${RUN_TS},${point_id},${rcouple},${rleak},${nominal_pass},${band_pass},${overall_pass},${spike_count},${mem_max_v},${first_spike_ns},${TRAN_MAXSTEP},\"${point_raw}\",\"${point_result}\",\"${point_spectre}\",\"${point_ocean}\"" >> "$RUN_CSV"
  done
done

python3 - "$RUN_CSV" "$RUN_MD" <<'PY'
import csv
import sys
from pathlib import Path

csv_path = Path(sys.argv[1])
md_path = Path(sys.argv[2])
rows = list(csv.DictReader(csv_path.open()))

nominal_pass = [r for r in rows if r["nominal_pass"] == "PASS"]
band_pass = [r for r in rows if r["band_pass"] == "PASS"]
overall_pass = [r for r in rows if r["overall_pass"] == "PASS"]

def fvals(key):
    vals = []
    for row in rows:
        try:
            vals.append(float(row[key]))
        except Exception:
            pass
    return vals

first_vals = fvals("first_spike_ns")
mem_vals = fvals("mem_max_v")

lines = []
lines.append("# Neuron Tile Sweep Summary")
lines.append("")
lines.append(f"Total points: {len(rows)}")
lines.append(f"Nominal PASS points: {len(nominal_pass)}")
lines.append(f"Pass-band PASS points: {len(band_pass)}")
lines.append(f"Overall PASS points: {len(overall_pass)}")
if mem_vals:
    lines.append(f"Membrane max range: {min(mem_vals):.3f} V .. {max(mem_vals):.3f} V")
if first_vals:
    lines.append(f"First spike range: {min(first_vals):.3f} ns .. {max(first_vals):.3f} ns")
lines.append("")
if rows:
    lines.append(f"Run ID: `{rows[0]['run_id']}`")
    lines.append(f"Run artifact root: `{Path(rows[0]['raw_dir']).parent.parent}`")
    lines.append("")
lines.append("| r_couple | rleak | nominal_pass | band_pass | overall_pass | spike_count | mem_max_v | first_spike_ns |")
lines.append("|----------|-------|--------------|-----------|--------------|-------------|-----------|----------------|")
for r in rows:
    lines.append(
        f"| {r['r_couple']} | {r['rleak']} | {r['nominal_pass']} | {r['band_pass']} | {r['overall_pass']} | {r['spike_count']} | {r['mem_max_v']} | {r['first_spike_ns']} |"
    )
lines.append("")
lines.append(f"CSV source: `{csv_path}`")
md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

cp -f "$RUN_CSV" "$OUT_CSV"
cp -f "$RUN_MD" "$OUT_MD"

{
  echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "latest_csv=$OUT_CSV"
  echo "latest_md=$OUT_MD"
  echo "run_csv=$RUN_CSV"
  echo "run_md=$RUN_MD"
} >> "$RUN_MANIFEST"

echo "Sweep complete:"
echo "  latest: $OUT_CSV"
echo "  latest: $OUT_MD"
echo "  run:    $RUN_CSV"
echo "  run:    $RUN_MD"
echo "  manifest: $RUN_MANIFEST"
