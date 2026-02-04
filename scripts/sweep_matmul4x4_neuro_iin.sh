#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NETLIST_NEURO="$REPO_DIR/netlists/matmul4x4_binary_neuro.scs"
NETLIST_BAK="$REPO_DIR/netlists/matmul4x4_binary_neuro.scs.bak_iin_sweep"
OUT_DIR="$REPO_DIR/competition/analysis"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$OUT_DIR/matmul4x4_neuro_iin_sweep/$RUN_TS"
RUN_CSV="$RUN_DIR/matmul4x4_neuro_iin_sweep.csv"
RUN_MD="$RUN_DIR/matmul4x4_neuro_iin_sweep_summary.md"
LATEST_CSV="$OUT_DIR/matmul4x4_neuro_iin_sweep.csv"
LATEST_MD="$OUT_DIR/matmul4x4_neuro_iin_sweep_summary.md"

DENSITY="${DENSITY:-0.06}"
SEED="${SEED:-1}"
IIN_LIST="${IIN_LIST:-220u,180u,150u,120u,100u,80u,60u,40u,30u,20u}"

mkdir -p "$RUN_DIR" "$OUT_DIR"

restore_default() {
  if [[ -f "$NETLIST_BAK" ]]; then
    cp -f "$NETLIST_BAK" "$NETLIST_NEURO"
    rm -f "$NETLIST_BAK"
  fi
  python3 "$REPO_DIR/scripts/generate_matmul4x4_checkpoint_assets.py" > "$RUN_DIR/restore_default.log"
  "$REPO_DIR/build.sh" matmul4x4_binary_digital > "$RUN_DIR/restore_build_digital.log" 2>&1 || true
  "$REPO_DIR/build.sh" matmul4x4_binary_neuro > "$RUN_DIR/restore_build_neuro.log" 2>&1 || true
}
trap restore_default EXIT

cp -f "$NETLIST_NEURO" "$NETLIST_BAK"

python3 "$REPO_DIR/scripts/generate_matmul4x4_checkpoint_assets.py" \
  --density "$DENSITY" \
  --seed "$SEED" \
  --metadata-out "$RUN_DIR/metadata.json" > "$RUN_DIR/generator.log"

"$REPO_DIR/build.sh" matmul4x4_binary_digital > "$RUN_DIR/build_digital.log" 2>&1
cp -f "$REPO_DIR/results/matmul4x4_binary_digital_test.txt" "$RUN_DIR/matmul4x4_binary_digital_test.txt"

DIGITAL_ENERGY_PJ="$(python3 - <<'PY'
import re
txt=open('results/matmul4x4_binary_digital_test.txt').read()
m=re.search(r"Total energy \(0-120ns\):\s*([0-9.+-eE]+)\s*J",txt)
print(float(m.group(1))*1e12 if m else '')
PY
)"

echo "iin_amp,neuro_pass,neuro_energy_pj,ratio_neuro_over_digital,latency_ns,total_partial_spikes" > "$RUN_CSV"

IFS=',' read -r -a iin_arr <<< "$IIN_LIST"
for iin in "${iin_arr[@]}"; do
  python3 - "$NETLIST_NEURO" "$iin" <<'PY'
import re,sys
path=sys.argv[1]
iin=sys.argv[2]
txt=open(path).read()
txt2=re.sub(r"iin_amp=[^ ]+", f"iin_amp={iin}", txt, count=1)
open(path,'w').write(txt2)
PY

  if "$REPO_DIR/build.sh" matmul4x4_binary_neuro > "$RUN_DIR/build_neuro_${iin}.log" 2>&1; then
    neuro_pass="PASS"
  else
    neuro_pass="FAIL"
  fi
  cp -f "$REPO_DIR/results/matmul4x4_binary_neuro_test.txt" "$RUN_DIR/matmul4x4_binary_neuro_${iin}_test.txt" 2>/dev/null || true

  row="$(python3 - "$DIGITAL_ENERGY_PJ" "$REPO_DIR/results/matmul4x4_binary_neuro_test.txt" "$neuro_pass" <<'PY'
import re,sys
dig=float(sys.argv[1])
path=sys.argv[2]
status=sys.argv[3]
try:
    txt=open(path).read()
except FileNotFoundError:
    print(f"{status},,,," )
    raise SystemExit
m_e=re.search(r"Total energy \(0-120ns\):\s*([0-9.+-eE]+)\s*J",txt)
m_l=re.search(r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns",txt)
m_s=re.search(r"Total partial spikes:\s*([0-9]+)",txt)
if m_e:
    e=float(m_e.group(1))*1e12
    ratio=e/dig if dig>0 else float('inf')
    e_txt=f"{e:.9f}"
    r_txt=f"{ratio:.9f}"
else:
    e_txt=""
    r_txt=""
l_txt=f"{float(m_l.group(1)):.9f}" if m_l else ""
s_txt=m_s.group(1) if m_s else ""
print(f"{status},{e_txt},{r_txt},{l_txt},{s_txt}")
PY
)"
  echo "$iin,$row" >> "$RUN_CSV"
done

python3 - "$RUN_CSV" "$RUN_MD" "$DIGITAL_ENERGY_PJ" <<'PY'
import csv
import sys
from pathlib import Path

csv_path=Path(sys.argv[1])
md_path=Path(sys.argv[2])
dig=float(sys.argv[3])
rows=list(csv.DictReader(csv_path.open()))
pass_rows=[r for r in rows if r["neuro_pass"]=="PASS" and r["neuro_energy_pj"]]

lines=[]
lines.append("# Matmul4x4 Neuro iin_amp Sweep (Measured)")
lines.append("")
lines.append(f"Digital baseline energy: `{dig:.6f} pJ`")
lines.append("")
lines.append("| iin_amp | pass | neuro energy (pJ) | ratio neuro/digital | latency (ns) | partial spikes |")
lines.append("|---------|------|-------------------|---------------------|--------------|----------------|")
for r in rows:
    lines.append(f"| {r['iin_amp']} | {r['neuro_pass']} | {r['neuro_energy_pj'] or 'n/a'} | {r['ratio_neuro_over_digital'] or 'n/a'} | {r['latency_ns'] or 'n/a'} | {r['total_partial_spikes'] or 'n/a'} |")

lines.append("")
if pass_rows:
    best=min(pass_rows, key=lambda r: float(r["ratio_neuro_over_digital"]))
    lines.append("Best passing point:")
    lines.append(
        f"- `iin_amp={best['iin_amp']}`, ratio=`{float(best['ratio_neuro_over_digital']):.3f}x`, "
        f"energy=`{float(best['neuro_energy_pj']):.6f} pJ`, latency=`{float(best['latency_ns']):.3f} ns`."
    )
else:
    lines.append("No passing neuro points in sweep.")

md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

cp -f "$RUN_CSV" "$LATEST_CSV"
cp -f "$RUN_MD" "$LATEST_MD"

echo "Neuro iin sweep complete:"
echo "  latest csv: $LATEST_CSV"
echo "  latest md:  $LATEST_MD"
echo "  run dir:    $RUN_DIR"
