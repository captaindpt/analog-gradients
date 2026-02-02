#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NETLIST_SRC="$REPO_DIR/netlists/neuro_tile4_coupled.scs"
TMP_NETLIST="$REPO_DIR/results/neuro_tile4_coupled/neuro_tile4_coupled_sweep_tmp.scs"
RESULT_DIR="$REPO_DIR/results/neuro_tile4_coupled"
OUT_DIR="$REPO_DIR/competition/sweeps"
OUT_CSV="$OUT_DIR/neuro_tile4_coupled_sweep.csv"
OUT_MD="$OUT_DIR/neuro_tile4_coupled_sweep_summary.md"

mkdir -p "$RESULT_DIR" "$OUT_DIR"

source "$REPO_DIR/setup_cadence.sh"

rfb_vals=("700" "1k" "1500")
rleak_vals=("6M" "8M" "10M")

echo "r_fb,rleak,pass,membrane_maxima,spike_counts,spike_maxima" > "$OUT_CSV"

for rfb in "${rfb_vals[@]}"; do
  for rleak in "${rleak_vals[@]}"; do
    sed "s/^parameters .*/parameters vdd_val=1.8 cpost=200f rdecay=80k r_couple=8k cmem=500f rleak=${rleak} r_fb=${rfb}/" \
      "$NETLIST_SRC" > "$TMP_NETLIST"

    (cd "$RESULT_DIR" && spectre "$TMP_NETLIST" -raw neuro_tile4_coupled.raw +log spectre.log >/dev/null)
    ocean -nograph < "$REPO_DIR/ocean/test_neuro_tile4_coupled.ocn" >/dev/null

    pass="$(grep -m1 "=== PASS" "$REPO_DIR/results/neuro_tile4_coupled_test.txt" || true)"
    if [[ -n "$pass" ]]; then
      pass="PASS"
    else
      pass="FAIL"
    fi

    mem_line="$(grep -m1 "Membrane maxima" "$REPO_DIR/results/neuro_tile4_coupled_test.txt" | awk -F: '{print $2}' | xargs)"
    cnt_line="$(grep -m1 "spike0=" "$REPO_DIR/results/neuro_tile4_coupled_test.txt" | xargs)"
    max_line="$(grep -m1 "Spike maxima" "$REPO_DIR/results/neuro_tile4_coupled_test.txt" | awk -F: '{print $2}' | xargs)"

    echo "${rfb},${rleak},${pass},\"${mem_line}\",\"${cnt_line}\",\"${max_line}\"" >> "$OUT_CSV"
  done
done

python3 - "$OUT_CSV" "$OUT_MD" <<'PY'
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
lines.append("| r_fb | rleak | pass | spike_counts |")
lines.append("|------|-------|------|--------------|")
for r in rows:
    lines.append(f"| {r['r_fb']} | {r['rleak']} | {r['pass']} | {r['spike_counts']} |")
lines.append("")
lines.append(f"CSV source: `{csv_path}`")
md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

echo "Sweep complete:"
echo "  $OUT_CSV"
echo "  $OUT_MD"
