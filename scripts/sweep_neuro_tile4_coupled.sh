#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NETLIST_SRC="$REPO_DIR/netlists/neuro_tile4_coupled.scs"
TMP_NETLIST="$REPO_DIR/results/neuro_tile4_coupled/neuro_tile4_coupled_sweep_tmp.scs"
RESULT_DIR="$REPO_DIR/results/neuro_tile4_coupled"
OUT_DIR="$REPO_DIR/competition/sweeps"
OUT_CSV="$OUT_DIR/neuro_tile4_coupled_sweep.csv"
OUT_MD="$OUT_DIR/neuro_tile4_coupled_sweep_summary.md"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$RESULT_DIR/sweeps/$RUN_TS"
RUN_CSV="$RUN_DIR/neuro_tile4_coupled_sweep.csv"
RUN_MD="$RUN_DIR/neuro_tile4_coupled_sweep_summary.md"
RUN_MANIFEST="$RUN_DIR/sweep_manifest.txt"

mkdir -p "$RESULT_DIR" "$OUT_DIR" "$RUN_DIR"

source "$REPO_DIR/setup_cadence.sh"

# Higher-resolution defaults for ticket 0013.
RFB_LIST="${RFB_LIST:-600,700,800,900,1000,1100,1200,1300,1500}"
RLEAK_LIST="${RLEAK_LIST:-5M,6M,7M,8M,9M,10M,12M}"
TRAN_MAXSTEP="${TRAN_MAXSTEP:-100p}"

IFS=',' read -r -a rfb_vals <<< "$RFB_LIST"
IFS=',' read -r -a rleak_vals <<< "$RLEAK_LIST"

{
  echo "run_id=$RUN_TS"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "rfb_list=$RFB_LIST"
  echo "rleak_list=$RLEAK_LIST"
  echo "tran_maxstep=$TRAN_MAXSTEP"
} > "$RUN_MANIFEST"

echo "run_id,point_id,r_fb,rleak,pass,tran_maxstep,membrane_maxima,spike_counts,spike_maxima,first_spike_times_ns,raw_dir,result_file,spectre_log,ocean_log" > "$RUN_CSV"

for rfb in "${rfb_vals[@]}"; do
  for rleak in "${rleak_vals[@]}"; do
    point_id="rfb_${rfb}_rleak_${rleak}"
    point_tag="$(printf '%s' "$point_id" | tr -c 'A-Za-z0-9._-' '_')"
    point_dir="$RUN_DIR/$point_tag"
    point_raw="$point_dir/neuro_tile4_coupled.raw"
    point_result="$point_dir/neuro_tile4_coupled_test.txt"
    point_spectre="$point_dir/spectre.log"
    point_ocean="$point_dir/ocean.log"
    mkdir -p "$point_dir"

    sed -e "s/^parameters .*/parameters vdd_val=1.8 cpost=200f rdecay=80k r_couple=8k cmem=500f rleak=${rleak} r_fb=${rfb}/" \
        -e "s/^tran_test tran stop=300n.*/tran_test tran stop=300n maxstep=${TRAN_MAXSTEP}/" \
      "$NETLIST_SRC" > "$TMP_NETLIST"

    rm -rf "$RESULT_DIR/neuro_tile4_coupled.raw"
    rm -f "$RESULT_DIR/spectre.log" "$REPO_DIR/results/neuro_tile4_coupled_test.txt"

    sim_start_epoch="$(date +%s)"
    if ! (cd "$RESULT_DIR" && spectre "$TMP_NETLIST" -raw neuro_tile4_coupled.raw +log spectre.log >/dev/null 2>&1); then
      pass="FAIL"
    elif ! grep -q "completes with 0 errors" "$RESULT_DIR/spectre.log"; then
      pass="FAIL"
    else
      raw_psfxl="$RESULT_DIR/neuro_tile4_coupled.raw/tran_test.tran.tran.psfxl"
      if [[ ! -f "$raw_psfxl" ]]; then
        pass="FAIL"
      elif (( $(stat -c %Y "$raw_psfxl") < sim_start_epoch )); then
        pass="FAIL"
      else
        if ocean -nograph < "$REPO_DIR/ocean/test_neuro_tile4_coupled.ocn" >"$RESULT_DIR/ocean.log" 2>&1; then
          if grep -q "=== PASS" "$REPO_DIR/results/neuro_tile4_coupled_test.txt" 2>/dev/null; then
            pass="PASS"
          else
            pass="FAIL"
          fi
        else
          pass="FAIL"
        fi
      fi
    fi

    cp -a "$RESULT_DIR/neuro_tile4_coupled.raw" "$point_raw" 2>/dev/null || true
    cp -f "$RESULT_DIR/spectre.log" "$point_spectre" 2>/dev/null || true
    cp -f "$RESULT_DIR/ocean.log" "$point_ocean" 2>/dev/null || true
    cp -f "$REPO_DIR/results/neuro_tile4_coupled_test.txt" "$point_result" 2>/dev/null || true

    mem_line="$(grep -m1 "Membrane maxima" "$point_result" 2>/dev/null | awk -F: '{print $2}' | xargs || true)"
    cnt_line="$(grep -m1 "spike0=" "$point_result" 2>/dev/null | xargs || true)"
    max_line="$(grep -m1 "Spike maxima" "$point_result" 2>/dev/null | awk -F: '{print $2}' | xargs || true)"
    first_line="$(grep -m1 "First spike times" "$point_result" 2>/dev/null | awk -F: '{print $2}' | xargs || true)"

    echo "${RUN_TS},${point_id},${rfb},${rleak},${pass},${TRAN_MAXSTEP},\"${mem_line}\",\"${cnt_line}\",\"${max_line}\",\"${first_line}\",\"${point_raw}\",\"${point_result}\",\"${point_spectre}\",\"${point_ocean}\"" >> "$RUN_CSV"
  done
done

python3 - "$RUN_CSV" "$RUN_MD" <<'PY'
import csv
import sys
from pathlib import Path

csv_path = Path(sys.argv[1])
md_path = Path(sys.argv[2])
rows = list(csv.DictReader(csv_path.open()))
pass_rows = [r for r in rows if r["pass"] == "PASS"]
fail_rows = [r for r in rows if r["pass"] == "FAIL"]

lines = []
lines.append("# Neuro Tile4 Coupled Sweep Summary")
lines.append("")
lines.append(f"Total points: {len(rows)}")
lines.append(f"PASS points: {len(pass_rows)}")
lines.append(f"FAIL points: {len(fail_rows)}")
lines.append("")
if rows:
    lines.append(f"Run ID: `{rows[0]['run_id']}`")
    lines.append(f"Run artifact root: `{Path(rows[0]['raw_dir']).parent.parent}`")
    lines.append("")
lines.append("| r_fb | rleak | pass | spike_counts | first_spike_times_ns | raw_dir |")
lines.append("|------|-------|------|--------------|----------------------|---------|")
for r in rows:
    lines.append(
        f"| {r['r_fb']} | {r['rleak']} | {r['pass']} | {r['spike_counts']} | {r.get('first_spike_times_ns', '')} | `{r['raw_dir']}` |"
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
