#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_ROOT="$REPO_DIR/competition/sweeps/matmul4x4_crossover"
OUT_ANALYSIS="$REPO_DIR/competition/analysis"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$OUT_ROOT/$RUN_TS"
RUN_CSV="$RUN_DIR/matmul4x4_crossover.csv"
RUN_MD="$RUN_DIR/matmul4x4_crossover_summary.md"
MANIFEST="$RUN_DIR/sweep_manifest.txt"

LATEST_CSV="$OUT_ROOT/matmul4x4_crossover.csv"
LATEST_MD="$OUT_ANALYSIS/matmul4x4_crossover_summary.md"

DENSITY_LIST="${DENSITY_LIST:-0.08,0.07,0.06,0.05,0.04,0.03,0.02,0.01}"
SEED_LIST="${SEED_LIST:-1,2,3,4,5,6,7,8,9,10}"

mkdir -p "$RUN_DIR" "$OUT_ROOT" "$OUT_ANALYSIS"

{
  echo "run_id=$RUN_TS"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "density_list=$DENSITY_LIST"
  echo "seed_list=$SEED_LIST"
} > "$MANIFEST"

echo "run_id,density,seed,active_products,digital_pass,neuro_pass,digital_energy_pj,neuro_energy_pj,ratio_neuro_over_digital,digital_latency_ns,neuro_latency_ns,digital_energy_per_active_pj,neuro_energy_per_active_pj,point_dir,metadata_json,digital_result,neuro_result" > "$RUN_CSV"

IFS=',' read -r -a dens_arr <<< "$DENSITY_LIST"
IFS=',' read -r -a seed_arr <<< "$SEED_LIST"

for density in "${dens_arr[@]}"; do
  for seed in "${seed_arr[@]}"; do
    point_tag="p_${density}_s_${seed}"
    point_tag="$(printf '%s' "$point_tag" | tr -c 'A-Za-z0-9._-' '_')"
    point_dir="$RUN_DIR/$point_tag"
    mkdir -p "$point_dir"

    meta_json="$point_dir/matmul4x4_metadata.json"
    python3 "$REPO_DIR/scripts/generate_matmul4x4_checkpoint_assets.py" \
      --density "$density" \
      --seed "$seed" \
      --metadata-out "$meta_json" > "$point_dir/generator.log"

    "$REPO_DIR/build.sh" matmul4x4_binary_digital > "$point_dir/build_digital.log" 2>&1
    cp -f "$REPO_DIR/results/matmul4x4_binary_digital_test.txt" "$point_dir/matmul4x4_binary_digital_test.txt"

    "$REPO_DIR/build.sh" matmul4x4_binary_neuro > "$point_dir/build_neuro.log" 2>&1
    cp -f "$REPO_DIR/results/matmul4x4_binary_neuro_test.txt" "$point_dir/matmul4x4_binary_neuro_test.txt"

    row="$(python3 - "$meta_json" "$point_dir/matmul4x4_binary_digital_test.txt" "$point_dir/matmul4x4_binary_neuro_test.txt" <<'PY'
import json
import re
import sys
from pathlib import Path

meta = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
dig_txt = Path(sys.argv[2]).read_text(encoding="utf-8")
neu_txt = Path(sys.argv[3]).read_text(encoding="utf-8")

def fpat(pat, txt):
    m = re.search(pat, txt)
    return float(m.group(1)) if m else None

def passed(txt):
    return "=== PASS:" in txt and "=== FAIL:" not in txt

dig_energy = fpat(r"Total energy \(0-120ns\):\s*([0-9.+-eE]+)\s*J", dig_txt)
neu_energy = fpat(r"Total energy \(0-120ns\):\s*([0-9.+-eE]+)\s*J", neu_txt)
dig_lat = fpat(r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns", dig_txt)
neu_lat = fpat(r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns", neu_txt)

active = int(meta["active_products"])
dig_pj = dig_energy * 1e12 if dig_energy is not None else None
neu_pj = neu_energy * 1e12 if neu_energy is not None else None
ratio = (neu_pj / dig_pj) if (dig_pj and neu_pj is not None) else None

if active > 0 and dig_pj is not None and neu_pj is not None:
    dig_epa = dig_pj / active
    neu_epa = neu_pj / active
else:
    dig_epa = None
    neu_epa = None

def fmt(v):
    return "" if v is None else "{:.9f}".format(v)

print(",".join([
    str(active),
    "PASS" if passed(dig_txt) else "FAIL",
    "PASS" if passed(neu_txt) else "FAIL",
    fmt(dig_pj),
    fmt(neu_pj),
    fmt(ratio),
    fmt(dig_lat),
    fmt(neu_lat),
    fmt(dig_epa),
    fmt(neu_epa),
]))
PY
)"

    echo "$RUN_TS,$density,$seed,$row,$point_dir,$meta_json,$point_dir/matmul4x4_binary_digital_test.txt,$point_dir/matmul4x4_binary_neuro_test.txt" >> "$RUN_CSV"
  done
done

python3 - "$RUN_CSV" "$RUN_MD" <<'PY'
import csv
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

csv_path = Path(sys.argv[1])
md_path = Path(sys.argv[2])
rows = list(csv.DictReader(csv_path.open("r", encoding="utf-8")))

g = defaultdict(list)
for r in rows:
    p = float(r["density"])
    g[p].append(r)

dens = sorted(g.keys())

lines = []
lines.append("# Matmul4x4 Sparse Crossover Sweep (Measured)")
lines.append("")
lines.append(f"Source CSV: `{csv_path}`")
lines.append("")
lines.append("| density | points | mean ratio (all points) | mean ratio (active>0) | neuro wins (active>0) | mean active products |")
lines.append("|---------|--------|-------------------------|-------------------------|----------------------|----------------------|")

means = []
means_active = []
for p in dens:
    rs_all = []
    rs_active = []
    act = []
    wins_active = 0
    active_count = 0
    for r in g[p]:
        a = float(r["active_products"])
        act.append(a)
        if r["ratio_neuro_over_digital"]:
            rv = float(r["ratio_neuro_over_digital"])
            rs_all.append(rv)
            if a > 0:
                rs_active.append(rv)
                active_count += 1
                if rv < 1.0:
                    wins_active += 1
    m_all = st.mean(rs_all) if rs_all else float("nan")
    m_active = st.mean(rs_active) if rs_active else float("nan")
    a = st.mean(act) if act else 0.0
    means.append((p, m_all))
    means_active.append((p, m_active))
    active_win_txt = f"{wins_active}/{active_count}" if active_count > 0 else "n/a"
    active_mean_txt = f"{m_active:.3f}" if active_count > 0 else "n/a"
    lines.append(f"| {p:.3f} | {len(g[p])} | {m_all:.3f} | {active_mean_txt} | {active_win_txt} | {a:.3f} |")

lines.append("")
lines.append("Crossover estimate (linear interpolation on mean ratio, active-products-only):")
crossover = None
pairs = [(p, r) for p, r in means_active if r == r]
for (p1, r1), (p2, r2) in zip(pairs, pairs[1:]):
    if (r1 - 1.0) * (r2 - 1.0) <= 0 and r1 != r2:
        crossover = p1 + (1.0 - r1) * (p2 - p1) / (r2 - r1)
        break
if crossover is None:
    lines.append("- No crossing within sampled density range.")
else:
    lines.append(f"- Estimated crossover density `p* ≈ {crossover:.4f}` (`{crossover*100:.2f}%` density, `{(1-crossover)*100:.2f}%` sparsity).")

lines.append("")
lines.append("Notes:")
lines.append("- This sweep is transistor-measured at `N=4` for both architectures.")
lines.append("- `ratio<1` means neuro consumes less total energy than digital for that point.")
lines.append("- Active-products-only statistics exclude trivial `Y=0` points (no useful multiply events).")

md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

cp -f "$RUN_CSV" "$LATEST_CSV"
cp -f "$RUN_MD" "$LATEST_MD"

# Restore default checkpoint assets for deterministic repo baseline behavior.
python3 "$REPO_DIR/scripts/generate_matmul4x4_checkpoint_assets.py" > "$RUN_DIR/restore_default.log"
"$REPO_DIR/build.sh" matmul4x4_binary_digital > "$RUN_DIR/restore_build_digital.log" 2>&1
"$REPO_DIR/build.sh" matmul4x4_binary_neuro > "$RUN_DIR/restore_build_neuro.log" 2>&1

{
  echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "run_csv=$RUN_CSV"
  echo "run_md=$RUN_MD"
  echo "latest_csv=$LATEST_CSV"
  echo "latest_md=$LATEST_MD"
} >> "$MANIFEST"

echo "Matmul4x4 crossover sweep complete:"
echo "  latest csv: $LATEST_CSV"
echo "  latest md:  $LATEST_MD"
echo "  run dir:    $RUN_DIR"
